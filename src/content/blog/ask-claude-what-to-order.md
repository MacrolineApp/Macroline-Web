---
title: I asked Claude what to order, then told it to log it
description: "Macroline runs as an MCP server, so an AI assistant can read your diary and write to it. Here's a real workflow: ask Claude for the best thing to order, then have it log the meal, without the AI ever inventing a number."
publishedAt: 2026-06-13
author: alex-rivera
tags: ["MCP", "AI", "Claude", "developer tools"]
---

Here's a thing I actually do now. I'm walking into a restaurant, I want the highest-protein option I can order for around 700 calories, and I don't want to think about it. So I ask Claude. It answers with a specific order. Then I say "log that in Macroline," and it does. I never open the app. I just eat.

That works because Macroline runs as a Model Context Protocol (MCP) server, which is a genuinely different architecture than the AI features bolted onto most apps.

## The tracker is the source of truth, the AI is a dispatcher

The lazy version of "AI nutrition" is a chatbot that calls some nutrition API and hands you numbers it made up on the spot. We built the inverse. Your diary, your goals, your weight, your saved meals all live in Macroline. Claude, or any MCP-compatible client, just talks to them through a small set of scoped tools: search the food database, log a meal, read your diary, get your daily summary, set your goals.

So when Claude logs that restaurant order, it isn't inventing macros. It's searching the same sourced database the app uses and writing a real entry. The meal lands in your diary carrying its source, exactly as if you'd logged it by hand.

## Why provenance is the answer to "AI slop"

There's a fair worry about AI and food tracking: that the AI just makes up your calories. It's the top objection I hear, and honestly it's a reasonable thing to be suspicious of.

Our answer is provenance. Every food the AI logs shows where its numbers came from: USDA, a manufacturer's label, or a clearly marked estimate. The AI is not allowed to quietly fabricate a nutrition fact and pass it off as data. If something is an estimate, it says so. That source badge is the difference between an AI that helps you track and one that just generates plausible-looking numbers.

## You own the data, access is scoped

Two more things that matter to anyone who thinks about this stuff. First, you own your data: switch AI clients tomorrow and nothing moves, because the data was never living in the model, it lives in your Macroline account. Second, access is bounded: the AI connects through OAuth with scoped permissions, so you're granting specific capabilities, not dumping your whole life into a chatbot.

## Try it

Connecting Claude to Macroline is a guided flow, walked through at [macroline.app/connect-claude](https://macroline.app/connect-claude). If you want the app itself first, it's [on the App Store](https://apps.apple.com/us/app/macroline/id6765770579) and [in the browser](https://my.macroline.app).

The bet we're making is that the useful version of AI in a tracker isn't a chat bubble in the corner. It's the app being something your assistant can actually operate, on your behalf, without ever guessing at the numbers.
