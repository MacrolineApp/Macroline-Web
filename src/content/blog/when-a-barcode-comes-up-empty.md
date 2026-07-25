---
title: "When a barcode comes up empty"
description: "A scan miss used to be a dead end. Now it's the start of a lookup chain: identify the product, research the nutrition, cite the source — and the next scan just works."
publishedAt: 2026-06-23
author: marcus-hayes
tags: ["product", "data quality", "scanning"]
---

Every tracker has the same worst moment: you scan a barcode and get nothing. Empty state. "Not found." You're standing in your kitchen holding a protein bar, and the app that promised to make this easy just shrugged.

Most apps handle this by making it *your* problem — "add a custom food!" — which means typing eleven numbers off a nutrition label into your phone while your dinner gets cold.

We think a miss is *our* problem. Here's what happens now when a scan comes up empty in Macroline.

## The chain

**Step one: check our own shelves.** Your scan first hits our catalog — 400,000+ foods, most with barcodes, stored under every padding variant scanners actually emit (12-digit UPC, 13-digit EAN, the works). Most scans end here.

**Step two: ask OpenFoodFacts.** A community database with global coverage. If the product's there and the data passes our ingest checks — physically plausible macros, sane serving sizes — we cache it and hand it back, labeled as what it is: community data, `estimated` tier.

**Step three: figure out what the thing IS.** This is the new part. On a true miss, we ask a barcode registry to at least *identify* the product — brand and name. Knowing "that's a Joyride Lemonade Stand Smacks Candy, 3.5 oz" turns an unanswerable question into a researchable one.

**Step four: research it properly.** With a real product name in hand, our research pipeline goes to work on the nutrition — and whatever it finds gets written into the catalog *with the barcode attached*. That last detail matters most: the next person who scans that UPC gets an instant hit. Every miss makes the catalog better.

## What we won't do

If the registry has never heard of the code, we stop. We could ask an AI to guess nutrition from a bare number — but a guess dressed up as data is exactly the thing we built Macroline to end. A clean "not found" plus a manual-entry path beats a confident fabrication every time.

And everything the chain produces is tiered and cited like all our data. Research output isn't stamped "authoritative" — it's labeled as researched, sources shown, upgradeable when an official source confirms it.

A dead end became a flywheel. Keep scanning weird stuff — you're building the database.
