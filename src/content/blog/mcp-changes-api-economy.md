---
title: How MCP changes the API economy
description: The Model Context Protocol isn't just another integration spec — it's a shift in who the primary user of an API actually is. Here's what that means for product builders.
publishedAt: 2026-03-15
author: alex-rivera
tags: ["MCP", "AI", "developer experience", "platform shifts"]
---

Most APIs are built with a specific assumption: the consumer is a developer who has read the docs, knows what they want, and will write code to call you in a structured way. The whole shape of REST — verbs, resources, status codes, pagination — is optimized for that consumer.

MCP breaks that assumption. The Model Context Protocol's primary consumer is a model, mediated by an agent harness, mediated by a user who doesn't know your API exists. That changes the design surface meaningfully.

## What MCP actually is

A short version, since the term is getting overloaded: MCP is a JSON-RPC protocol that lets an AI client (Claude, ChatGPT plugins, custom agents) discover and invoke "tools" exposed by a server. Each tool has a name, a description, a JSON Schema for inputs, and an executor on the server side. The model reads the descriptions, decides which tool to call for the user's intent, and calls it.

That's it. That's the protocol. The interesting part is what happens once the protocol is widely adopted.

## What changes when the model is the user

Three things look different when you design for an LLM consumer instead of a human developer:

**Descriptions become product copy.** With a REST API, your endpoint name and your docs are separate concerns. With MCP, the description is *the* product surface. The model decides whether to call your tool based on the one or two sentences you wrote in the description field. If your description is vague, the model picks something else.

**Schema validation matters more.** A developer who hits a 400 will read the error and adjust their code. A model will retry with a slightly different shape, then give up and tell the user "I couldn't do that." Tight schemas with good error messages aren't quality polish — they're the difference between your tool getting used and getting silently dropped.

**Idempotency is structural.** Models retry. They retry on timeouts, they retry on ambiguous responses, they sometimes retry because their planner second-guesses itself. Every write tool needs a `clientRequestId` or equivalent, and the server has to actually honor it. Otherwise users get duplicate diary entries, double-charged invoices, accidentally deleted rows.

## Why this isn't "just another integration"

The Slack-bot era of integrations was build-once, copy-paste-everywhere. Each app had a custom slash-command syntax, a custom auth model, a custom webhook for events. The "integration" was a humans-in-the-loop business agreement layered with a bespoke protocol.

MCP collapses that. There's one protocol. The model figures out the rest. That means:

- The cost of being integratable goes way down. Spec, ship, list.
- The cost of *not* being integratable goes way up. If your competitors are accessible to Claude and you aren't, you've quietly become invisible.
- The integration design owner shifts. It's no longer your sales team writing partnership agreements with Slack — it's your API team writing tool descriptions for an LLM.

## What this means for product structure

A few specific implications I'm watching:

**Read APIs become more important than write APIs again.** For a long time the "rich" surface in consumer software has been the UI. Read endpoints were minimal — mostly to feed the UI. With MCP, reads are how the model understands the user's state. Stale read APIs mean dumb agents. Investing in good read shapes pays off twice.

**Provenance becomes table stakes.** When an AI is reading your data and synthesizing answers, the user is going to ask "where did this come from." If your API doesn't surface provenance, the AI fabricates it or admits ignorance. Either is bad. (This is part of why we lead with source tiers and citation URLs at Macroline — the LLM consumer is a more demanding reader of metadata than a UI ever was.)

**Auth gets weirder.** OAuth 2.1 with PKCE, dynamic client registration — these specs were always there but rarely used. MCP forces the issue. Your OAuth flow has to be smooth enough that a non-technical user can complete it inside a chat conversation.

## Where this goes

I think we're maybe two years from a world where most consumer SaaS has an MCP endpoint by default — the way most have a "Connect to Zapier" button now. The surface looks like:

- A `mcp.json` (or similar) at a well-known path
- A small set of clearly named, clearly described tools
- OAuth that actually works with public clients

The companies that get there first won't be the ones with the most tools. They'll be the ones with the best tool *descriptions* — because that's the part the model reads, and that's what determines whether users get value.

Worth thinking about while it's still early.
