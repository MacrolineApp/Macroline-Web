---
title: Why we built an MCP server for nutrition data
description: Macroline runs as a Model Context Protocol server. Here's what that means, why it matters, and how AI-native tools change what a tracker can be.
publishedAt: 2026-05-02
author: alex-rivera
tags: ["MCP", "AI", "developer tools"]
---

The Model Context Protocol (MCP) lets AI assistants — Claude, ChatGPT, custom agents — read from and write to external systems through a standardized interface. Think of it as USB for AI tools.

Macroline runs as an MCP server. Once you connect it to Claude (or any MCP-compatible client), you can:

- Log meals from any AI conversation. "I had pasta for lunch, log it" — Claude figures out the macros and writes it to your diary.
- Query your own data conversationally. "What was my average protein intake last week?"
- Build custom dashboards. Ask Claude to summarize your trends, generate weekly reports, plan meals around your remaining macros.
- Integrate with anything. If it speaks MCP, it speaks to Macroline.

## Why this is more than a chatbot integration

The lazy version of "AI macro tracking" is a ChatGPT wrapper that calls a nutrition API. We didn't build that.

What we built is the inverse: **the tracker is the source of truth, and AI clients are dispatchers**. Your diary, your goals, your weight, your saved meals — they all live in Macroline. The AI just talks to them.

This matters because:

**You own your data.** Switch AI clients tomorrow — the data doesn't move. We're not lock-in software.

**The food database is the moat.** 8,500+ USDA foods, OpenFoodFacts barcodes, chain restaurants researched on demand, every row sourced. AI clients all benefit from the same authoritative database.

**Privacy is bounded.** AI clients only see what your account allows. You don't dump your whole life into the model — you grant scoped access through OAuth.

## What you can do today

The MCP server is in active development. The first wave of tools:

- `search_food` — Find a food by name or brand
- `log_meal` — Add diary entries with idempotency
- `get_diary` — Read recent entries
- `get_summary` — Daily macros + remaining
- `set_goals` — Update calorie/macro targets

Future waves will add the research agent (chain restaurant lookups), barcode scanning via shared cache, and weight/medication tracking endpoints.

## How to connect

Once we ship MCP OAuth, connecting Claude to Macroline will be a one-tap flow in the iOS app. Coming with v0.5.0.

Until then, the MCP server is being scaffolded internally. If you're an AI developer who wants early API access, [drop us a line](mailto:info@macroline.app).

## The bigger bet

We think most apps will eventually be AI-accessible by default. The question is whether they're **AI-first** (built around the assumption that an AI agent will be a primary user) or **AI-bolted-on** (a chatbot button stuck on a 2018 app).

Macroline is the former. The MCP server isn't a feature — it's how we think the next decade of consumer software should be built.
