---
title: Bad food data wrecks a cut faster than bad programming
description: I've audited the food logs of more than thirty clients whose cuts stalled. The training plan wasn't the problem in roughly twenty-four of them. The numbers in their tracker were off, sometimes by a lot, and the compounding made the stall inevitable.
publishedAt: 2026-05-16
author: marcus-hayes
tags: ["cutting", "muscle preservation", "data quality", "macro precision", "tracking"]
---

I get the call a lot: "Coach, my cut stalled, my training's been solid, can we look at the program?" And we look at the program, and the program is usually fine. The deload is in the right place, volume's appropriate for the calorie deficit, sleep is reasonable. There's no obvious leak. We tighten a few things. Two weeks pass. Still stalled.

The next thing I ask is: send me your last fourteen days of food logs.

About 80% of the time, that's where the cut is actually leaking. Not in the gym. In the tracker.

## The compounding math nobody runs

Here's what 20% per-meal calorie error looks like over a real cut.

A 200-lb male lifter cutting 500 cal/day below maintenance. Target intake: 2400 cal. He's logging meticulously by a measuring-cup standard, but the food entries he's pulling from a crowd-sourced database are systematically light — maybe 12% under on average across his typical foods. He thinks he's at 2400. He's actually at 2688.

288 extra calories per day, 7 days a week, 12 weeks. **24,000 extra calories** across the cut. That's a little under 7 lb of would-be-lost fat, and the actual scale movement reflects roughly what 288 cal/day of additional intake would predict.

Now factor in that crowd-sourced entries skew under, not random. People uploading entries are generally underestimating portion size, omitting cooking oils, missing the sugar in the sauce. The 12% number above is on the conservative side. I've seen clients whose typical logged-vs-actual gap was 22%.

This is why the cut "stalled." The cut didn't stall. The data did.

## Two patterns I see constantly

**Pattern 1: The stranger's MyFitnessPal entry.** A client logs "chicken breast 8 oz" and picks the first entry that comes up. That entry was uploaded in 2019 by a user who weighed cooked chicken (smaller than raw), guessed at the oz, and entered macros they got from a generic Google search. There's no source attached. No way to verify. Three days later, the same client logs the same food and picks a different entry — same name, different numbers. Now their logged total is internally inconsistent across days, and the trends they're trying to read are noise.

**Pattern 2: AI-estimated restaurant meals with no source attribution.** This is the new one. A client describes a restaurant meal to an AI parser — "I had a chicken Caesar wrap and a side of fries" — and the parser returns numbers. The numbers look reasonable. They're an estimate based on a generic chicken Caesar wrap and a generic side of fries. The actual restaurant version might have 300 more calories from a creamier dressing, larger portion, and fries fried in a heavier oil. The client doesn't know that. The tracker doesn't tell them.

Both patterns produce logs that **look correct** but are wrong. And a log that looks correct is harder to debug than a log you know is wrong.

## What I make my clients do now

After the third or fourth time I traced a stalled cut to crowd-sourced food data, I changed how I run my clients' tracking. Three rules:

**Rule 1: Audit the entry, not just the food.** When you add a new food to your daily rotation, look at where the number came from. USDA Foundation entries (the U.S. Department of Agriculture's reference database) are nutritional truth, measured in actual labs. Manufacturer-labeled entries are bound by FDA labeling rules — they're allowed some rounding, but they're directly tied to the product on the shelf. Crowd-sourced entries with no attached source are guesses by a stranger.

If you're cutting, the difference between Foundation/manufacturer and crowd-sourced isn't a 2% accuracy improvement. It's the difference between data and noise.

**Rule 2: Lock your staples.** I have my clients pick their twenty most-frequent foods and lock the entries — same row, every time, from a known-source database. If oats are oats, they're always *that* oat entry. If chicken breast is chicken breast, it's always *that* entry, weighed raw, measured the same way. Lock-and-repeat means the noise from entry selection drops to zero on the foods you eat constantly.

**Rule 3: Use AI estimates as honest estimates, not as facts.** The new AI-parsing tools are useful — sometimes essential, especially for restaurant meals where there's no other option. But the output is an *estimate*. I tell clients to treat any AI-estimated meal as "best guess, +/- 15%." If your cut math is leaning on a string of AI-estimated days, that's the variance you're working with. Plan accordingly: build in more deficit headroom, weigh more often, expect more noise in the weekly weight average.

The version of this rule I've come to is: **the more you depend on estimates, the less precision you can claim about your deficit**. You can have a precise deficit on rule-1 data. You can't have a precise deficit on rule-3 data. Both are fine. Just don't confuse them.

## Why provenance tags matter for a coach

I started using Macroline mid-2025 partly because of how it surfaces this. Every food entry has a tier badge — Authoritative (USDA/manufacturer), Computed (derived from other entries), Estimated (AI-generated), Unverified (user-created). My clients can see, in the moment of logging, whether they're working with reference data or a guess.

That signal changes behavior. I have one client who started picking the higher-tier entry every time a duplicate came up. His weekly average tightened up immediately. Not because the food changed. Because the *information about the food* got better.

If you're tracking through any other app, the equivalent move is: check the source. USDA Foundation or a manufacturer with a real ingredient list = trust. A blank source field on a community-uploaded entry = audit before you trust.

## When the numbers are right and the cut still stalls

For the record: yes, some cuts stall for real reasons. Adaptive thermogenesis exists. Steady-state cardio adaptation exists. Sleep debt accumulating across a cut is real. Stress-driven cortisol shifts are real. Compliance fatigue is real, and it shows up in subtle places (the bite you didn't log, the salad dressing eyeballed instead of weighed).

But every one of those is downstream of the tracking. If the tracking is solid — high-tier sources, locked staples, honest treatment of estimates — then a real stall is at least diagnosable. You can look at the actual deficit, see it's actually being held, and start investigating non-intake factors with confidence.

When the tracking is loose, you can't tell what's a real stall and what's a data stall. Most of the calls I get fall into the second bucket. The cut isn't broken. The data is.

---

The takeaway I'd give any lifter mid-cut: if your weekly weight average isn't moving the way the math predicts, audit the data layer before you blame the program. The program is usually right. The numbers, on a community-sourced tracker, often aren't.
