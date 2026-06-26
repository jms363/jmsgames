// Cloudflare Worker for the JMS Studios hub.
// Serves the static site (ASSETS binding) and handles POST /api/subscribe —
// creating a beehiiv subscription server-side so the API key never reaches the
// browser. Requires env vars BEEHIIV_API_KEY + BEEHIIV_PUBLICATION_ID (V2 id).
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/subscribe' && request.method === 'POST') {
      return handleSubscribe(request, env);
    }
    // Static assets (incl. games.json + its CORS header via _headers) are served
    // by the assets layer; the Worker only handles the /api routes above.
    return env.ASSETS.fetch(request);
  },
};

async function handleSubscribe(request, env) {
  let email = '';
  try {
    const ct = request.headers.get('content-type') || '';
    email = ct.includes('application/json')
      ? (await request.json())?.email ?? ''
      : (await request.formData()).get('email') ?? '';
  } catch {
    return json({ ok: false, error: 'Could not read your request.' }, 400);
  }

  email = String(email).trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ ok: false, error: 'Please enter a valid email address.' }, 400);
  }

  const apiKey = env.BEEHIIV_API_KEY;
  const pubId = env.BEEHIIV_PUBLICATION_ID;
  if (!apiKey || !pubId) {
    return json({ ok: false, error: 'Subscriptions are not configured yet.' }, 500);
  }

  let resp;
  try {
    resp = await fetch(`https://api.beehiiv.com/v2/publications/${pubId}/subscriptions`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        reactivate_existing: true,
        send_welcome_email: true,
        utm_source: 'jmsgames.com',
        referring_site: 'jmsgames.com',
      }),
    });
  } catch {
    return json({ ok: false, error: 'Could not reach the mail service. Please try again.' }, 502);
  }

  if (!resp.ok) {
    console.error('beehiiv error', resp.status, await resp.text().catch(() => ''));
    return json({ ok: false, error: 'Something went wrong. Please try again.' }, 502);
  }

  return json({ ok: true, message: "You're in — watch your inbox for new game drops." });
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
