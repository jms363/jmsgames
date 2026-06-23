// JMS Games hub — renders the game grid from games.json.
// Add a game = add an entry to games.json. No code change needed.

(function () {
  "use strict";

  var grid = document.getElementById("games");
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  function el(tag, className, html) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (html != null) node.innerHTML = html;
    return node;
  }

  function escapeHtml(str) {
    return String(str == null ? "" : str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function buildCard(game) {
    var isLive = game.status === "live" && game.url;
    var accent = game.accent || "#22d3ee";

    var card = el(isLive ? "a" : "div", "card " + (isLive ? "card--live" : "card--soon"));
    card.style.setProperty("--accent", accent);

    if (isLive) {
      card.href = game.url;
      card.setAttribute("aria-label", "Play " + game.name);
    }

    // Thumbnail
    var thumb = el("div", "card-thumb");
    if (game.thumb) {
      var img = el("img");
      img.src = game.thumb;
      img.alt = game.name;
      img.loading = "lazy";
      thumb.appendChild(img);
    } else {
      thumb.appendChild(el("div", "placeholder", isLive ? escapeHtml(game.name) : "?"));
    }
    thumb.appendChild(
      el("span", "badge " + (isLive ? "badge--live" : "badge--soon"), isLive ? "Play" : "Soon")
    );
    card.appendChild(thumb);

    // Body
    var body = el("div", "card-body");
    body.appendChild(el("h2", "card-title", escapeHtml(game.name)));
    body.appendChild(el("p", "card-tagline", escapeHtml(game.tagline || "")));

    if (Array.isArray(game.tags) && game.tags.length) {
      var tags = el("div", "card-tags");
      game.tags.forEach(function (t) {
        tags.appendChild(el("span", "tag", escapeHtml(t)));
      });
      body.appendChild(tags);
    }

    if (isLive) {
      body.appendChild(el("span", "card-cta", 'Press start <span class="arrow">&rarr;</span>'));
    }

    card.appendChild(body);
    return card;
  }

  function render(games) {
    grid.innerHTML = "";
    if (!games.length) {
      grid.appendChild(el("p", "error", "No games yet — check back soon."));
      return;
    }
    games.forEach(function (g) {
      grid.appendChild(buildCard(g));
    });
  }

  grid.appendChild(el("p", "loading", "Loading games…"));

  fetch("/games.json", { cache: "no-cache" })
    .then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    })
    .then(function (data) {
      render((data && data.games) || []);
    })
    .catch(function (err) {
      console.error("Failed to load games.json:", err);
      grid.innerHTML = "";
      grid.appendChild(
        el(
          "p",
          "error",
          'Could not load the game list. Try <a href="https://drugbiz.jmsgames.com">Drug BiZ</a> directly.'
        )
      );
    });
})();
