---
title: "Tools we wish existed in the macro-tracking category"
description: "An honest builder's wishlist for what's still missing in nutrition tracking, from substitution preview to cross-tracker import. Open product brief, not a roadmap."
publishedAt: 2026-01-29
author: alex-rivera
tags: ["product design", "category", "AI-native", "developer tools"]
---

I've been logging food on and off for about a decade and building a tracker for the last year. That combination produces a specific kind of frustration: you can see exactly where the category is stuck, you know roughly what it'd take to unstick it, and you also know why nobody's done it (the unit economics are bad, the data is locked up, the platforms don't cooperate).

This post is a wishlist of tools that should exist in the macro-tracking category and mostly don't. Some of these we're working on. Some we're not, because they're outside our scope or the business case is too thin. I'm writing this as an open product brief: if you're building in this space, please go take any of these and run with it. The category is undersupplied.

## Real-time macro impact of meal substitutions

The single biggest interaction gap in every tracker I've used: you can log what you ate, but you can't ask "what if I swap fries for rice." The mental model the user actually has is comparative ("is this better or worse than what I'd otherwise eat") and the tools only support absolute ("here's what you ate").

The shape of this tool: a UI where you've staged a meal but not committed it, and you can tap any item to see substitution suggestions ranked by macro delta against your goals. "If I swap medium fries for white rice, I drop 180 cal, gain 8g carbs, lose 12g fat." The model already knows your goals and your day-so-far, so it can frame the swap in terms that matter: "this swap moves you back into your protein window."

This is hard because it requires a good substitution graph (which foods are reasonable swaps for which others), which itself requires either a large hand-curated dataset or a really good embedding model over the food catalog. Neither exists publicly. We're working on the embedding approach.

## Photo to portion estimation with on-device weight inference

The killer demo every nutrition app wants: snap a photo of your plate, get a logged meal. The reason nobody has shipped this well is that portion estimation from a 2D photo is genuinely hard. You can identify "this is chicken and broccoli" reasonably reliably. You cannot tell from the photo whether the chicken is 4 oz or 8 oz, and the calorie difference is 100%.

The fix that I think actually works: combine the photo with depth data (modern iPhones have LiDAR, modern Androids have ToF on flagships), a known reference object in frame (the plate diameter, which the app can ask for once), and on-device inference. Apple's Vision framework plus a small custom model could plausibly do this for a defined set of common foods to within 20% accuracy. That's good enough to be useful and honest about its limits (surface the confidence interval, let the user adjust).

The part that has to be on-device, not in the cloud: photo of your food carries metadata you don't want flowing through someone else's inference infrastructure. Time-stamped, geotagged photos of every meal you eat is the kind of data that should stay local.

## Restaurant menu API with cached macros

The state of restaurant nutrition data is embarrassing. Chain restaurants in the US are required by law (FDA menu labeling rule) to publish calorie counts, and most publish full macros on a PDF buried two clicks deep on their site. There's no public API. There's no even-vaguely-standard format. Every nutrition app is scraping these pages independently, getting different results, and updating on different cadences.

The tool that should exist: a public, well-cached, well-versioned API for chain restaurant menu items. Standard schema. Last-updated timestamps. Provenance back to the source PDF. Free for non-commercial use, paid tier for trackers.

This is a "someone should just do it" project. The data is public. The work is unglamorous (scraping, normalization, monitoring for menu changes). The benefit is every nutrition app gets better, and the maintainer becomes the source-of-truth layer for a category. Pick 50 chains, build a scraper and a normalizer, charge $50/mo for commercial access. We'd be a paying customer day one.

## Cross-tracker import (the "data trapped in MyFitnessPal" problem)

I have eight years of food data in MyFitnessPal. I cannot meaningfully get it out. There's a CSV export buried in account settings that gives you a flattened diary with no food IDs, no serving info, just dates and calorie totals. Cronometer is somewhat better but still poor. LoseIt is worse.

The user impact: switching trackers means losing your history, which means the category has aggressive lock-in. The trackers know this. The trackers also know they're not motivated to fix it.

The tool that should exist: a third-party "nutrition data portability" service. User connects their MFP/Cronometer/LoseIt account via screen-scraping (since none expose proper APIs), the service does the slow work of walking the diary, resolving each entry against a canonical food database, and producing a clean export that any modern tracker can import. Run it once, get your history out.

Build it as a B2B tool that challenger trackers pay for. Incumbents won't pay because they benefit from the friction. The harder question is legal: screen-scraping a user's own data through their own credentials sits in a gray zone (CFAA, hiQ v. LinkedIn). Get a lawyer involved before shipping.

## Shared family meal logging

If you cook for a household, every tracker treats you as a single user and asks you to re-enter the same recipe every time anyone eats it. The user model is wrong: the meal is shared, the data should be shared, the per-person split is a derived view.

The tool that should exist: meals as first-class shared objects across accounts. Family member A cooks dinner for four, logs the recipe and total portions. Family member B sees "you had 1.5 portions of A's lasagna" appear in their own diary with the correct macros pre-computed. The recipe owner can edit the recipe once and everyone's history corrects.

This is implementation-heavy (you're suddenly a small social network with permission edges and shared state) but conceptually obvious. It's also a moat against the AI-only competitors: a feature that depends on relationships between accounts is structurally harder for a chatbot to replicate.

## Macro budgeting like financial budgeting

Macros are a resource allocation problem and the tools all treat them as a logging problem. The financial equivalent would be Mint showing you "you spent $4,200 this month" and stopping there, never suggesting an envelope budget or a rebalance.

The tool that should exist: macro budgeting with envelopes. "Of my 180g daily carbs, 60 are reserved for post-workout, 40 for breakfast, the rest is flexible." When you log a meal, the relevant envelope ticks down. When you're staring at an afternoon snack decision, you can see "you have 35g of flex carbs left, this granola bar takes 28."

This reframes the daily experience from "did I go over" to "how do I spend what's left." The first version of this could be built on top of any existing tracker as a layer; eventually it wants to be the primary interaction.

## Honest medication-and-food interaction logging

A real one. Lots of people on GLP-1 agonists (semaglutide, tirzepatide) experience food aversions, reflux triggers, dosing-day appetite drops. The tracker apps mostly ignore this because medication tracking is its own product category. The result is that users juggle two apps and never connect the patterns.

The tool that should exist: a logbook that knows about your medication schedule and surfaces correlations honestly. "Your protein intake drops 40% in the 48 hours after your weekly dose." "Spicy foods correlate with reflux flags on dosing weeks." Treat the data with care (this is medical-adjacent) and surface patterns without diagnosing. We're shipping a version of this and the user response has been strong, because nobody else is doing it.

## Why these tools mostly don't exist

The pattern across this list is that the gaps are not technical. The substitution preview is buildable. The portion estimator is buildable on current hardware. The restaurant API is just labor. Cross-tracker import is a weekend of scraping code and a lawyer.

The gap is that the category's incumbents have shipped enough features to claim coverage and don't have a competitive reason to invest in any of these. The challengers (us included) are small and have to pick. So the gaps stay.

If you're a builder reading this and one of these resonates: please go build it. The category is undersupplied. The user value is real. The "but who would use this" question has an answer (people who actually log their food, which is millions of people who are currently underserved). And if you build the restaurant menu API, please email me. I will be your first paying customer.
