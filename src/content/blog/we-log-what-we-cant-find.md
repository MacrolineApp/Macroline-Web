---
title: "We now log the searches that find nothing"
description: "Every failed scan and empty search in Macroline becomes a signal. Here's how user misses now decide what we research next — and why five people beat one person retrying five times."
publishedAt: 2026-07-16
author: alex-rivera
tags: ["product", "data quality", "philosophy"]
---

Ask any database company what they have and they'll talk for an hour. Ask them what people *looked for and didn't find* and you'll get silence — most systems don't even record the question.

We started recording the question.

As of this month, every scan that comes up empty and every search that returns nothing in Macroline quietly logs a miss. Not your data — the *gap*. The barcode that matched nothing. The phrase that found no food. That stream of misses now feeds a ranked worklist we look at constantly, and it has one job: decide what gets researched and added next.

## Demand, ranked honestly

The ranking rule matters more than it sounds:

**Five different people missing one food outranks one person missing it five times.** A retry is frustration; five strangers wanting the same thing is demand. So the list counts *distinct people*, not raw attempts.

A couple of details we're proud of:

- **Gaps close themselves.** The moment a missing barcode lands in the catalog — through research, an import, or a curator — it drops off the list automatically. The worklist only ever shows what's still true.
- **Identified misses jump the line.** When a scan misses but we can at least identify the product ("that's a Fun Club Peelable Mango Gummy"), the gap arrives pre-labeled — which makes fixing it fast. Known-name gaps get researched almost immediately.
- **Old gaps age out.** If nobody's missed it in a month, it stops occupying the list. Demand data should be fresh or it's fiction.

## Why tell you this

Because it changes what your failed scan *means*. In most apps, a "not found" is a dead end you experienced alone. Here, it's a vote. You are — literally, mechanically — steering what this database becomes, just by trying to use it.

So when something comes up empty: that miss was heard. Scan the weird protein bar from the regional grocery chain. Search for the dish nobody else logs. The empty result you got today is the reason it won't be empty next month.

The catalog isn't a warehouse. It's a conversation.
