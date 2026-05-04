# Macroline-Web — Claude guidance

The marketing & support site at macroline.app. Astro 5 static site, deployed via Cloudflare Pages.

## What lives here

- **Public marketing** — hero, features, pricing, provenance pillars
- **Apple-required pages** — privacy policy, terms of service (currently placeholders)
- **Support FAQ** — public help, no auth needed
- **Waitlist signup** — `<form action="https://api.macroline.app/api/waitlist">` (TODO: implement endpoint in MacrolineDb)

## What does NOT live here

- The app itself (that's `Macroline/` — Tauri/Svelte)
- API or auth endpoints (that's `MacrolineDb/`)
- Authenticated user dashboard (lives in the Tauri app, also accessible at my.macroline.app via the separate Macroline-WebApp repo)

## Working principles

- **Static and fast.** No client-side framework needed. Astro renders Svelte/React if we ever need islands, but the v1 pages are server-rendered HTML + a tiny bit of CSS.
- **Brand voice:** direct, confident about AI, "Just say what you ate." Don't slip into hype-y AI marketing.
- **Provenance is the marketing wedge.** Lead with it. Tier badges visible on the homepage.
- **Mobile-first responsive.** This site will be opened on a phone after someone hears about us — make sure that path is clean.

## Pages I should not edit casually

- `/privacy` and `/terms` are legal documents. Once we ship the real versions (replacing placeholders), they should not change without explicit approval — Apple reviewers cite specific phrases.

## What's NOT done yet

- Real privacy policy (currently placeholder)
- Real terms (currently placeholder)
- Waitlist endpoint in MacrolineDb (form posts somewhere that doesn't exist)
- App Store badges (need actual download URL after launch)
- OG image at `/og.png` (1200×630, generate via Pillow once logo is finalized)
- Actual blog (no `/blog` index yet)
- Logo SVG file in `public/` (currently using inline 3-segment bar; export proper SVG once finalized)
- API documentation page at `/api`

## Deployment

Cloudflare Pages auto-deploys on push to `main`. PR previews work too. No manual deploy needed.
