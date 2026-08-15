---
title: "A food database that grows itself (honestly)"
description: "When someone hand-logs a Capital Grille steak because we didn't have it, that's a signal. Inside the pipeline that turns user gaps into researched, verified catalog entries — with the tier labels to match."
publishedAt: 2026-08-03
author: alex-rivera
tags: ["data quality", "provenance", "AI", "product"]
---

The most valuable thing a user can tell a food database is what it doesn't have.

We noticed it in the logs first: a run of hand-created entries for restaurants we didn't cover — a steakhouse tartare, a coney island chicken gyro, a handful of Michigan pubs. Each was one person doing the work of estimating a meal because we'd left them no choice. That's a bad experience for them, and it's a wasted signal for us. The next person searching that restaurant hits the same wall.

So we built a conveyor.

## Demand in, catalog out

Every night, the system groups the brands people hand-logged in the last day. Any brand where we have fewer than a handful of real entries gets queued for research: an AI pass produces a compact lineup of the most-ordered items with estimated nutrition, and every item runs through the same physics screens our imports face — calories have to agree with the macros, servings have to be real-world portions, nothing lands that a label couldn't plausibly say.

Then comes the part we're most careful about. Nothing from that pass goes straight into the catalog. It lands in a candidate queue, and a second, independent stage decides what it is.

## The certifier: honest tiers, automatically

For each candidate, a verifier with live web search asks a simple question: *does this brand publish official nutrition data for this item?*

- **Yes, and the source checks out** — the brand's own nutrition page or PDF, URL answering a real request, domain actually theirs (aggregator sites are blocklisted) — the official numbers win, and the row is published as **authoritative** with that source attached. Chick-fil-A's items landed this way, fifteen of sixteen with the official page cited.
- **No official data, but an independent estimate agrees** with the candidate within a sane tolerance — the row publishes as an **estimate**, badged as one. Two independent opinions is the corroboration we'd otherwise ask a human for.
- **The numbers can't describe the item at any portion** — rejected. Nobody sees it.

Every disposition is written on the candidate row: what was decided, why, and when. The whole thing runs unattended, and the admin surface became something to *glance at* rather than a queue to work.

## Why the tier label is the whole point

It would be trivial to publish every AI-generated row as if it were fact. It would also be a lie, and users can feel lies in a nutrition app — it's the moment they stop trusting the number on the screen.

So the tier follows the evidence, and only the evidence. Official numbers with a live source get the top badge. Good estimates say "estimate." A single unverified guess never gets to look like a label. When the local pub you actually eat at shows up in search with an "AI estimate" tag, that tag is us being straight with you: we did the work, here's how confident we are, tap through and see.

## What it did in its first week

Fifteen items for a fine-dining spot a user had hand-logged once. Eighteen for a burrito chain — with the official nutrition URL found and cited. Dozens of Michigan restaurants that publish nothing, estimated with menu-anchored portion math and labeled honestly. And a stack of ambiguous cases routed back to a human, because the machine's job is to do the tedious 90% and be honest about the rest.

The database you search tomorrow will be a little better than the one you searched today — and it will tell you exactly which parts to trust.
