---
title: "Your food database should correct itself"
description: "Food data drifts — formulas change, labels update, community sources get fixed. Inside the revalidation system we built so stale numbers don't quietly become lies."
publishedAt: 2026-07-12
author: maya-chen
tags: ["data quality", "provenance", "product"]
---

Here's an uncomfortable truth about every nutrition database, including ours: the moment you import a number, it starts aging. Manufacturers reformulate. Serving sizes change. Community databases correct their own mistakes. A protein shake that was entered correctly two years ago can be wrong today *without anyone touching it*.

Most trackers never look back. Data goes in once and fossilizes — which means the app is quietly confident about numbers nobody has checked since import day.

We've been building the machinery to do better, and the design choices are worth showing, because they're all provenance choices.

## Re-check what people actually eat, first

We track when each food was last validated against its source. But with hundreds of thousands of rows and polite rate limits on the sources we check against, "re-check everything" would take months — and most of those rows have never been logged by anyone.

So the queue is **demand-ordered**: foods that appear in real diaries get re-checked first. Freshness lands where it matters — on the shake you log every morning, not on row #380,000 that nobody has ever searched for.

In early test passes, this ordering immediately caught real drift on popular items — a major-brand protein shake whose fiber and sodium had changed upstream, a snack bar whose calories had been corrected by the source community. Exactly the foods you'd want caught.

## Big swings don't auto-apply

Here's the rule we're most opinionated about: **if a re-check says a food's calories moved by 3x or more, we don't apply it.** We quarantine it for human review.

Why? Because a swing that large usually isn't the food changing — it's a data accident. Per-100g values arriving where per-serving belongs. A parse hiccup. A community edit gone wrong. Auto-applying "your 150-calorie bar is now 520" would corrupt the catalog at machine speed. One bad sync should never outrun human judgment.

## Corrections never rewrite your history

When a food row does get corrected, your past diary entries don't change. Every log you make snapshots the macros *as they were when you logged them* — because your Tuesday was your Tuesday. The database getting smarter shouldn't gaslight your history.

And every correction leaves an audit trail: what changed, from what source, when. Tap the food, see the citation. Same promise as always — the numbers show their work.

Fossils are for museums. Your food data should stay alive.
