---
title: What we built — Macroline 1.0 ships today
description: Today Macroline 1.0 lands on the App Store. Here's what's in the box, what we deliberately left out, who 1.0 is for, and the design principles behind the cuts. Substance, no hype — that's the brand.
publishedAt: 2026-05-22
author: alex-rivera
tags: ["launch", "product", "macroline", "MCP", "GLP-1"]
---

Today is launch day. Macroline is live on the [App Store](https://apps.apple.com/us/app/macroline/id6765770579), available on iPhone, with the matching web companion at [my.macroline.app](https://my.macroline.app). The free tier covers the core tracking experience; the $4.99/month Pro tier unlocks AI-heavy features (more describe-a-meal quota, MCP integration to connect Claude or any MCP-compatible assistant, advanced history charts) and removes the soft daily limits on cost-heavy operations.

I want to walk through what 1.0 actually is — the *substance*, not the marketing copy — because the shape of a product on launch day says more about the design intent than any subsequent feature push does. Here is what we built.

## What's in 1.0

**Describe a meal.** The product's first principle: just say what you ate. Open the app, tap the microphone, say "I had a chicken caesar wrap, a small fries, and a Coke Zero." The AI parses it into individual items, matches each against the database, and gives you a single log entry with macros and provenance tags. If the AI is unsure about an item, it tells you so. If it estimates, the estimate is tagged Estimated, not Authoritative. The downstream view never confuses the two.

**Barcode scan with manual fallback.** Point the camera at a packaged food's barcode. If we have it (we ship with roughly 470,000 indexed barcodes, weighted toward U.S. retail), the food row appears with full macros and a source link to either USDA Branded, OpenFoodFacts, or the manufacturer's own data. If the scanner can't read the barcode — torn label, damaged box, glare — you can type the number manually. Either way, if we don't have it, we'll research it: a backend agent tries UPCitemdb and then Claude with the barcode + best-effort context, and the entry shows up on a later session.

**Diary with snapshot semantics.** Every logged entry preserves the macros that were true at the moment you logged it. If a food row gets corrected three weeks later — say, OpenFoodFacts updates the entry, or our team flags and revises a bad row — your historical log doesn't retroactively shift. The diary is a record, not a live view.

**Provenance tier badges, everywhere.** Every food has one of four tiers — Authoritative (USDA Foundation, USDA Branded, chain-official nutrition pages, manufacturer labels), Computed (derived from established factors like Atwater 4/4/9), Estimated (AI-generated or community-sourced with verification gaps), Unverified (user-created and private). The badge is on the search row, on the picked-food sheet, on the diary entry. You always see where a number came from.

**Weight tracking with a chart.** Log a weight reading; see the 60-day trend; see the rolling delta. The chart doesn't include moralizing copy about whether you're up or down — it's the trend, neutral.

**GLP-1 / medication tracking.** Log doses for any commonly-prescribed GLP-1 (semaglutide, tirzepatide, liraglutide), bariatric-adjuncts, naltrexone-bupropion, phentermine, orlistat, and a generic supplement category. Side effects, schedule reminders, dose history. The medications surface is deliberately a *log*, not a *recommender* — no titration prompts, no "you should increase," no therapeutic claims. That's not a regulatory hedge; it's the product position.

**MCP server.** Connect Claude (or any MCP-compatible AI client) to your Macroline account, and the assistant can read your diary, log meals, pull summaries, log exercise, log water, and search the food database. Free tier gets read-only and a daily query quota; Pro tier removes the cap. This is the wedge that makes Macroline an AI-native nutrition app rather than an AI-bolted-on one — your assistant has the same view of your data that the app does.

**Cookieless web companion.** Everything works in your browser at my.macroline.app — same provenance, same logging, same MCP. The marketing site at macroline.app sets zero non-strictly-necessary cookies; the web companion sets only the session cookies required for login, which is the textbook strictly-necessary GDPR exemption. No third-party trackers anywhere.

## What we deliberately didn't ship

This list is doing as much work as the previous one. We had time and budget for several of these and decided against. Each is a position statement.

**Food-photo recognition.** Point your camera at a plate and let AI estimate the macros. We didn't ship this in 1.0 because the accuracy ceiling on plate-photo estimation is significantly lower than barcode + describe combined, and shipping a feature whose median output is "guess from pixels" against a backdrop of authoritative provenance would degrade the brand position. It's on the roadmap, and we'll ship it the moment we're confident it can carry an Estimated tag and stay useful.

**Streaks.** No "logged for 14 days in a row, keep it up" notifications. No green-flame icon next to your name. Streak mechanics are well-documented to drive engagement in food trackers — and to drive disordered behaviors in the population most likely to be using a food tracker. We aren't going to ship the dopamine loop that punishes people for missing a day.

**Photo-log of meals (as a social feed).** Some popular trackers ship a Photo Diary where you can post pictures of every meal to your timeline. We don't, by design. Tracking is for *awareness*, not performance. A camera-roll of every meal you've eaten in the last year is fascinating to nobody and emotionally weird to a meaningful subset.

**Social and community features.** No followers, no leaderboards, no comments. There are real positives to community in weight-management apps — the bariatric and GLP-1 communities have done tremendous peer work — and we're not the right team to build that responsibly. The communities that exist (the GLP-1 subreddits, the bariatric Facebook groups, the strength-training Discord rooms) already do this better than we would. We ship a tracker; they ship community.

**Diet templates / "do keto with us."** We don't prescribe a way of eating. The app is macro-and-calorie-agnostic by default; if you want to track only protein and ignore carbs, the UI doesn't shame you. If you want to follow keto, the app supports it; if you want to follow Mediterranean, the app supports that too. We don't pick.

## The principles, in plain words

The cuts above run through five principles, which I'll write out so the next product decision can be measured against them:

1. **Provenance over volume.** A smaller database with sourcing is more useful than a larger database without.
2. **Tracking is for awareness, not performance.** Streak mechanics, social feeds, public weigh-ins — out.
3. **AI is a feature, not the brand.** Macroline works without an AI assistant connected. The MCP integration is a power tool, not the product.
4. **No therapeutic claims, ever.** The app logs medication doses and side effects; it doesn't suggest doses or interpret medical state. The line moves the moment we cross it.
5. **The user is the expert on the user.** We don't refuse the calorie target your clinician set. We don't second-guess the protocol you're on. We log what you tell us, surface the data honestly, and stay out of your medical relationship.

## Who 1.0 is for

If you're tracking macros for a real reason — a cut, a bulk, a bariatric or GLP-1 protocol, a sports goal, a curiosity about what you actually eat — and you want a tracker whose food data has sources you can check, this is the version for you. If you have an AI assistant in your daily workflow and you want it to read and write your food log, this is the version for you. If you're a developer or a power user who wants the data you generate to belong to you and to leave with you, this is the version for you.

If you want a tracker that turns your eating into a stream you post about, gives you streak mechanics, and recommends a specific diet — that's a different product, and there are many good ones. We aren't trying to be that.

Macroline is on the [App Store](https://apps.apple.com/us/app/macroline/id6765770579) today. The web companion is at [my.macroline.app](https://my.macroline.app), the MCP setup guide is at [/connect-claude](/connect-claude), and you can read more about the principles behind every cut in the rest of this blog.

Just say what you ate. We'll do the rest.

— Alex (and the whole Macroline team)
