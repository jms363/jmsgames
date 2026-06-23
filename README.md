# JMS Games — hub (jmsgames.com)

The landing page / portfolio for Joe Sardo's web games. Each game lives in its
**own** repo and Cloudflare Pages project, served at `gamename.jmsgames.com`.
This hub is the front door at the apex `jmsgames.com` (+ `www`) and just links out.

- **First game:** [Drug BiZ](https://drugbiz.jmsgames.com) — `github.com/jms363/drug-biz`
- **Stack:** plain static HTML/CSS/JS. **No build step.**
- **Hosting:** Cloudflare Pages.

## Project layout

```
index.html      hub page (markup + meta/OG/fonts)
styles.css      arcade / neon dark theme
app.js          fetches games.json and renders the card grid
games.json      the game manifest — THE thing you edit to add a game
404.html        styled not-found page
favicon.svg     JMS GAMES mark
assets/games/   per-game card thumbnails
```

## Add a new game

1. Drop a square thumbnail at `assets/games/<slug>.png` (the game's logo works great).
2. Add an entry to `games.json`:

   ```json
   {
     "slug": "mygame",
     "name": "My Game",
     "tagline": "One-line hook.",
     "tags": ["Puzzle"],
     "url": "https://mygame.jmsgames.com",
     "thumb": "assets/games/mygame.png",
     "accent": "#22d3ee",
     "status": "live"
   }
   ```

   - `status`: `"live"` (clickable card + neon hover) or `"soon"` (dimmed placeholder; `url`/`thumb` can be empty).
   - `accent`: the neon glow color for that card.

3. Commit + push — Cloudflare auto-deploys. No code change needed.

## Run locally

`app.js` uses `fetch("/games.json")`, so it needs a server (not `file://`):

```bash
npx serve .          # or: python -m http.server 8000
```

Then open the printed URL.

## Deploy (Cloudflare Pages)

One-time setup:

1. Push this repo to `github.com/jms363/jmsgames`.
2. Cloudflare dashboard → **Workers & Pages → Create → Pages → Connect to Git** → pick `jmsgames`.
3. Build settings:
   - **Framework preset:** None
   - **Build command:** *(leave empty)*
   - **Build output directory:** `/`
4. After the first deploy, **Custom domains** → add `jmsgames.com` and `www.jmsgames.com`
   (Cloudflare manages the DNS since the zone is on Cloudflare).

Each game subdomain (e.g. `drugbiz.jmsgames.com`) is added the same way **on that
game's own Pages project** — Custom domains → `drugbiz.jmsgames.com`.

## TODO

- [ ] Create a GA4 property for `jmsgames.com` and paste its ID into the (commented) analytics block in `index.html`.
- [ ] Add a real `favicon.ico` and a social `assets/og.png` (1200×630) for link previews.
