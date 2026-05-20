---
title: No tracking, no theater — the macroline.app stack, in full
description: Most consent-banner sites set thirty or more third-party cookies on first load. macroline.app sets zero non-strictly-necessary cookies. Here's what we actually use, what we deliberately don't, and why the popular "Accept all / Reject" pattern is theater more often than it's a defensible privacy practice.
publishedAt: 2026-05-19
author: alex-rivera
tags: ["privacy", "web architecture", "cookies", "GDPR", "trust"]
---

If you open macroline.app and look at the Cookies tab in your browser's devtools, you'll find an empty list. Not "minimal." Empty. The site sets zero non-strictly-necessary cookies on first load. No Google Analytics. No Facebook Pixel. No TikTok pixel. No Mixpanel. No Segment. No Hotjar session recording. No retargeting iframe. No third-party SaaS sneaking a cookie in through a chat widget.

This is unusual enough that I want to walk through it explicitly — what's actually loaded, what we left out, and the reasoning behind both.

## What macroline.app actually uses

Three external requests. That's it.

**Cloudflare Pages analytics.** Cloudflare runs the hosting and serves the site. Their built-in Pages analytics gives us page-view counts, country distribution at the country level, and basic referrer data. It's **server-side**: no JavaScript injected into your browser, no cookie set, no per-user identifier created. The data we see is a count of HTTP requests by URL, aggregated.

**The Inter typeface from rsms.me.** This loads two CSS files and the font binaries. No cookies. No analytics. No script. It's a single Inter Display CDN — Rasmus Andersson, who designed the typeface, hosts it himself. The only thing your browser tells the rsms.me server is what every browser request tells every server it talks to: your IP and the URL you asked for. No cross-site tracking.

**Stripe.** Loaded only on `/pricing` when you click Subscribe. It does set cookies — Stripe needs them to process a payment session — but they're loaded **on your action**, on the page where you are explicitly initiating a billing transaction. Under GDPR's "strictly necessary for a service the user explicitly requested" carve-out, these don't require consent because they only exist when you've explicitly asked for the service Stripe provides. If you never click Subscribe, Stripe never loads.

That's the complete dependency graph. There is no fourth thing.

## What we left out, and why

Most marketing sites in 2026 ship some combination of:

- Google Analytics 4 (sets `_ga`, `_ga_*` cookies; persistent device ID)
- Facebook / Meta Pixel (sets `_fbp`, `fr`; persistent fingerprint)
- TikTok pixel
- LinkedIn Insight Tag
- A consent management platform (paradoxically setting its own tracking cookies to remember your consent state)
- Hotjar or FullStory or Microsoft Clarity for session replays
- An intercom-style chat widget (sets its own cookies for conversation persistence)
- A retargeting pixel from whatever ad platform the brand is buying on

Each of these is a defensible decision in isolation. Combined, you end up at a site that sets twelve to thirty cookies on first visit, mostly for vendors the user has no relationship with. The consent banner that pops up to ask "Accept all / Reject all / Customize" is a UI patch on a stack that was assembled with the user as a data source.

The reason we don't do this isn't ideological — it's that none of those vendors give us information worth the cost. Pageviews from Cloudflare are enough to tell us which blog posts are doing what. We don't run paid ad campaigns yet, so the pixel data would feed nothing. Session replay is a great tool when you've got a debugging problem; it's not a great default. The chat widget would help support volume if we had it; we don't, so we route to email instead.

When we add features that genuinely need a third-party loaded on the marketing site — and that day will come — we'll decide whether to do it at all, and if we do, we'll add it with consent in front of it. The same component shell that renders our current transparency notice can flip to a categories-based consent banner without a redesign.

## Why "Accept all / Reject" banners are theater

The pattern you see everywhere — "We use cookies. Accept all / Reject" — solves a much narrower problem than it pretends to.

Under the ePrivacy Directive and GDPR, you need explicit consent to set **non-strictly-necessary** cookies. Strictly-necessary cookies (your shopping cart, your CSRF token, your login session) are exempt. The consent banner is only legally meaningful for the non-necessary set.

A site that sets zero non-necessary cookies has nothing to gate behind that banner. Showing one is performative — a costume of compliance, not a compliance act. It costs the user a click and a moment of friction; it gives the site the appearance of taking privacy seriously without the site having had to change anything else about its data practices. Many sites do this because their compliance vendor told them to. Some do it because they're saving on the upfront audit work and using the banner as a kind of insurance policy.

The result, in the average web user's mind, is that "privacy banner" has become a near-synonym for friction. The signal is no longer trustworthy. When a site that actually doesn't track you puts up a consent banner, the user reads it as theater — because most of the time, it is.

The honest version, for sites with the data practices to back it, is the version we shipped this week: a small transparency notice that says, in so many words, *we don't have anything to ask you about, but here's what we use, and here's the privacy policy with the receipts*. It takes one click to dismiss and never returns. The component will stay through launch and beyond.

## How to audit any site for this in five minutes

You don't need to take our word for the empty cookie list. Open the site, then your browser's devtools (right-click → Inspect → Application or Storage tab in Chrome; Storage tab in Firefox; Storage Inspector in Safari). Under Cookies, click the site's domain. The list you see is the cookies that site has set in your browser.

Do the same with the sites you visit most. The result is usually instructive. A typical Shopify-hosted store sets eight to twelve cookies on landing. A typical SaaS marketing site lands at fifteen to twenty. A typical news site is in the hundreds, mostly from ad-tech partners.

For comparison: a request to macroline.app, with no prior history, sets zero. Cloudflare Pages analytics does its work entirely server-side; your browser never sees a counter.

You can verify the same on any site you build. The audit takes five minutes and is one of the clearer signals about how a team thinks of its users.

## The cost we accepted

We give up some things by running this way. We don't have funnel analytics on the marketing site — we can't tell you which post led to which signup, which referrer converts at what rate, which CTA outperforms which. We don't have session replays when a user reports a UI bug; we have screenshots and reproduction steps and that's it. We don't run retargeting, so we don't see the second touch.

These are real costs. We've decided they're worth paying because the alternative — assembling a tracker stack and putting a banner in front of it — would erode something we'd then spend the rest of the product's life trying to rebuild.

The piece that actually matters about trust is that it has to be verifiable. "We respect your privacy" written on a marketing page is uncheckable. An empty cookie list, on the other hand, is something you can confirm in your devtools right now.

---

Macroline runs a single transparency notice on first visit — *No tracking, no theater* — with an expandable list of what we actually use. You can re-trigger it from the Privacy page's section 9. The notice is also designed to flip cleanly to a categories-style consent banner the day we ship a feature that needs one. We'd rather not.
