---
title: "The numbers you can't read don't count"
description: "Font sizes, truncated names, and six 'greek yogurt' rows on six different serving bases. What a real-app design audit found — and the readability release it produced."
publishedAt: 2026-08-13
author: alex-rivera
tags: ["product", "tracking", "data quality"]
---

We spent a lot of this summer on what's *behind* the numbers — provenance, revalidation, a certifier that verifies official sources. This week we worked on something more basic: whether you can actually read them.

It started with two user notes. *The diary text is small.* And: *when I tap an entry, it still doesn't show me the whole name.* Both turned out to be symptoms of the same habit — bounding text so long, community-contributed food names couldn't blow up the layout — applied one level too far. The row clamped the name at two lines. Then the detail sheet clamped it *again*. A long name was truncated at every level of the app with no way to ever read it in full.

We ran a full walk of the real app — every screen, at phone size — and looked at it the way a new user would. Here's what changed.

## Bigger where it counts

The food name is the diary's primary content, and it was rendering at fine-print size. It's bigger now, with the time and serving line up a notch too. Rows still cap at two lines so a 200-character name can't wreck the list — but the detail sheet is now the one place the full name always shows, wrapping as long as it needs to. The subtitle there shows the brand *and* the serving together, instead of arbitrarily picking one.

## Rows that tell you what you're choosing

Search "greek yogurt" and you'd get six rows at 92, 61, 73, 78 calories — each on a *different serving basis*, with no serving shown and no protein. People picked the smallest number and logged the wrong food.

Every typeahead row now shows the serving basis under the calories, and protein in the meta line. For an app whose users are choosing food by protein more than anything else, putting that number at the decision moment is the highest-leverage change on the list, and it cost one line per row.

The raw database names got the same treatment. "Yogurt, Greek, plain, nonfat" — the USDA's comma-inverted convention — now reads "Greek Yogurt (plain, nonfat)." Same row, same source, same citation; it just doesn't read like a database dump.

## Nothing hides behind the search bar

The floating search bar was covering the last card on Today and the last row on Diary. The Coach's pitch was cut off mid-sentence; a logged food sat half-buried. It's the same class of bug as our earlier "the copy button isn't there" report — a useful thing hidden under floating chrome. Both screens now leave clearance.

## Kindness in the zero state

A brand-new account's very first screen used to say "LOGGED **0/7** days this week." A failing score before you've done anything. It now reads "—/7 · log once to start the week." And the morning cards — yesterday at a glance, the reminder offer, "same as yesterday?" — became quick, dismissable notices at the top of the screen instead of a stack of banners sitting on your numbers. Your board opens to your data.

None of this is a headline feature. All of it is the difference between an app you *can* use and one you *want* to. Provenance is what makes the numbers trustworthy. Readability is what makes them yours.
