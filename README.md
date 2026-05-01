# Macroline-Web

Marketing & support site for [Macroline](https://macroline.app). Hosted on Cloudflare Pages.

## Stack

- [Astro 5](https://astro.build) — static site, fast Lighthouse, MD-friendly
- Inter / Inter Display fonts via [rsms.me/inter](https://rsms.me/inter/)
- Cloudflare Pages — connect this repo, build cmd `npm run build`, output `dist/`

## Local development

```bash
npm install
npm run dev          # http://localhost:4321
npm run build        # → dist/
npm run preview      # preview the production build locally
```

## Pages

| Path | Purpose |
|---|---|
| `/` | Hero, three pillars, provenance moat, waitlist signup |
| `/features` | Detailed feature list |
| `/pricing` | Free vs Pro, $4.99/mo or $39.99/yr |
| `/privacy` | Privacy policy (placeholder — replace before App Store submission) |
| `/terms` | Terms of Service (placeholder) |
| `/support` | Contact + FAQ |

## Cloudflare Pages setup

In Cloudflare Pages dashboard:
1. Connect to `mikejamescalvert/Macroline-Web` GitHub repo
2. Framework preset: **Astro**
3. Build command: `npm run build`
4. Build output: `dist`
5. Custom domain: `macroline.app` (apex) — Cloudflare automatically configures DNS since the domain is on Cloudflare
6. Optional: redirect `www.macroline.app` → apex

## Brand

- Tagline: *Just say what you ate.*
- Logo mark: 3-segment macro bar (protein/carbs/fat)
- Voice: direct, confident about AI, provenance-forward, no diet shame

See `K:\_FoodTracker\PLAN.md` §6 for full visual identity spec.

## License

Proprietary.
