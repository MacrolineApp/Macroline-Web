---
title: "Why we wrote our own nutrition parser instead of stuffing GPT into it"
description: "A vanilla LLM call looks like a free meal parser until you ship it. Here's what breaks (units, portions, brand canonicalization) and why a structured parser with confidence scoring is the right tool."
publishedAt: 2025-12-18
author: alex-rivera
tags: ["AI tools", "engineering", "product design", "data quality"]
---

The first version of any "log your meal" feature in 2025 looks the same. You take the user's freeform text ("two scrambled eggs, a slice of sourdough, black coffee"), you stuff it into a prompt, you ask GPT-4 or Claude to "extract the foods and their portions as JSON," and you ship a demo video on Twitter. It looks magical. It is also, in production, kind of bad.

We built Macroline's meal parser the other way: a structured extraction pipeline that verifies against the food database, scores its own confidence, and falls back to a research agent when it knows it doesn't know. The LLM is in there, but it's doing the part it's actually good at, not the part it's confidently wrong about.

This post is the engineering case for that split.

## What goes wrong when you just call the model

I want to be specific here, because "LLMs hallucinate" is the kind of statement that gets nodded at and then ignored. The failure modes that actually bite you on a meal parser are concrete and recurring.

**Units get mis-coerced.** A user types "8 oz chicken." The model returns `{ "food": "chicken breast", "amount": 8, "unit": "oz" }`. Fine. The user types "a chicken breast." The model returns `{ "amount": 1, "unit": "breast" }`. Now your downstream code has to handle "breast" as a unit, or silently coerce it to something arbitrary, or 422 out and frustrate the user. Multiply by every food shape: "a banana," "two slices of pizza," "a handful of almonds," "a scoop of protein." There's no clean schema for this if you let the model invent the unit field.

**Portions get hallucinated with confidence.** Ask GPT-4 how many grams are in "a medium banana" and you'll get 118. Ask it three more times and you'll get 120, 105, and 125. Each answer is plausible, each is delivered without hedging, and the variance is invisible to the caller. The user sees one number and trusts it. Real banana mass varies by a factor of two depending on what "medium" means at your grocery store, but the model never says "I'm guessing." That's the problem: a model that's confidently wrong is worse than a parser that knows when it doesn't know.

**Brand names get normalized to the wrong canonical form.** "Chobani vanilla" becomes "vanilla yogurt" because the model decided to be helpful and generic. "Trader Joe's everything bagel seasoning" becomes "everything bagel seasoning." The brand-specific macro data (which is the actual reason you care) gets dropped on the floor. Worse, the user thinks they logged the branded item.

**Restaurant items get fabricated.** "Chipotle bowl with double chicken and brown rice" produces a JSON object with macro values that look right. They're not from Chipotle's published nutrition data. They're the model's best guess from training data that's probably 18 months old, mixed with general knowledge about chicken and rice. The numbers might be off by 30% and you'd never know.

**Multi-language and regional foods collapse.** A user logs "onigiri" and the model returns "rice ball" with generic rice macros. The actual onigiri has seaweed, salt, and often a filling (tuna mayo, umeboshi, salmon) that materially changes the macro profile. The model didn't ask. It just answered.

None of these are exotic edge cases. They all happen in the first 50 entries any real user logs.

## What our parser actually does

The parsing pipeline has four stages. The LLM is in one of them, doing a specific job.

**1. Tokenize the freeform input into candidate entries.** "Two scrambled eggs, a slice of sourdough, black coffee" splits into three candidates. This is mostly deterministic with some light model assistance for ambiguous boundaries ("chicken and rice" is one dish or two? context-dependent). The LLM here is a classifier, not an extractor.

**2. Structured extraction per candidate.** For each candidate, we extract a typed shape: `{ rawText, quantity, unit, foodDescriptor, modifiers }`. The schema is tight. `quantity` is a number or null. `unit` is from a closed vocabulary (g, oz, ml, cup, tbsp, tsp, slice, piece, serving, etc.) or null. `foodDescriptor` is the cleaned food name. `modifiers` is a list of qualifiers (scrambled, grilled, low-fat, etc.). If the model returns something outside the schema, we reject and re-prompt with the error. This costs latency but eliminates a whole class of garbage downstream.

**3. Resolve against the food database.** This is the part most "just call GPT" implementations skip. Each candidate gets fuzzy-matched against our food catalog, which has provenance tiers (authoritative, computed, estimated, unverified). Matches return ranked options with a confidence score derived from string similarity, brand-prefix match, popularity, and source tier. If the top match scores above the threshold, we use it. If it doesn't, we surface options to the user. If nothing matches at all, we kick to stage 4.

**4. Research agent fallback.** For things the catalog doesn't know about (a new restaurant menu item, a regional brand, a homemade recipe), the research agent kicks off an actual web lookup, parses the source page, and stages a new food entry for review. The agent's outputs are tagged as unverified until a human confirms. The user sees "we found this but haven't verified it, the values might be off."

The confidence score is the load-bearing piece. Every parsed entry carries a number from 0 to 1 representing "how sure are we." Below 0.6, we always ask the user to confirm. Above 0.9, we just log it and tell the user what we did. In between, we show the match but make the confirm-or-edit affordance prominent. Users learn the system's reliability quickly because the system shows them when it's guessing.

## Why this matters for trust

The interaction model is different from a pure LLM parser, and the difference is the point.

A pure LLM parser is a black box that gives you a number. When the number is wrong, the user has no way to know it's wrong until much later (their week's macros don't match how they feel, the trend line is off, they catch a specific entry and lose faith in the whole log). The trust collapse is sudden and total.

A confidence-scored parser is a glass box. The user sees "high confidence" entries get logged silently and "low confidence" entries get flagged. When the parser is wrong on a low-confidence entry, the user already knew it might be. When it's wrong on a high-confidence entry, that's a real bug we can fix, and we can fix it in the data layer (add the right entry to the catalog, retrain the matcher) rather than in a prompt we have to keep tweaking.

The food database is the actual moat. The LLM is a router on top of it. If we'd let the LLM do the extraction *and* the answering, we'd be a thin wrapper around someone else's confidently-wrong autocomplete. Instead we're a verified catalog with a smart input layer, and the input layer is honest about its limits.

## The takeaway for builders

If you're building a feature where the LLM has to produce a numerical answer that the user will trust, ask yourself a specific question: when the model is wrong, will the user know?

If the answer is no, you don't have an AI feature. You have a confidence trap. The fix is almost always the same shape: constrain the model to the part of the problem where it's actually good (classification, extraction into a tight schema, picking among options) and ground the answers in a verified source. Surface uncertainty. Make "I don't know" a first-class output.

Stuffing GPT into the parser is a one-week ship. Doing it right is a quarter. The first version looks better in the demo. The second version is the one that survives contact with users.
