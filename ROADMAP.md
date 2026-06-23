# JMS Studios — roadmap

Future work for the hub and the games. Ordered by priority.

## Now / next
- [ ] **Add more games.** Each game = its own repo + Cloudflare deployment on
      `gamename.jmsgames.com`, then one entry in [`games.json`](games.json) + a thumbnail
      in `assets/games/`. (See the "add a new game" steps in [README.md](README.md).)
      Grow the arcade before building cross-cutting features below.

## Planned features
- [ ] **Social media share buttons.** Let players share games to their feeds
      (X, Facebook, Reddit, copy-link, etc.).
      - Most valuable on the **individual game pages** (share the specific game), plus
        a "share JMS Studios" option on the hub.
      - Groundwork already done: Open Graph tags + pixel-font OG image mean shared links
        already render a proper preview card. This task is just the click-to-share buttons.
      - Pair share links with `?utm_source=…` tags so GA4 shows which platform drives traffic
        (the `www`→apex Redirect Rule already preserves query strings).
      - Standardize the button component once, then reuse it across each game repo.

## Someday / cleanup
- [ ] **Redeploy the hub as a real Cloudflare Pages project** (it's currently a Worker, which
      is why `www` needed a Redirect Rule). Not urgent — apex + www both work today.
- [ ] **GA4: consolidate** into one "JMS Studios" property with a data stream per game, so the
      whole arcade reports in one place (hub stream already live: `G-0Q1CEDQWTR`).
