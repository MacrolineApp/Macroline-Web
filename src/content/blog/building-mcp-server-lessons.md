---
title: Building an MCP server — lessons from the trenches
description: Notes from implementing a production-ready MCP server with OAuth 2.1, dynamic client registration, and a real consumer app on the other end. The places we got it wrong, and how the spec helps and hurts.
publishedAt: 2026-04-04
author: alex-rivera
tags: ["MCP", "OAuth", "engineering", "implementation"]
---

We've been running an MCP server in production for a few months now. This is the rough write-up of what worked, what we got wrong, and what the spec doesn't quite tell you when you go to implement it.

## The bones of the spec are good

The Model Context Protocol's core JSON-RPC dispatch is straightforward. `initialize`, `tools/list`, `tools/call`, `ping` — five-ish methods, each with a tight contract. We had a working `tools/list` returning real schemas in a couple of hours.

The spec authors made a defensible call to keep the wire protocol minimal and push complexity into the auth and metadata layers. It means the protocol is approachable, but the *system* you build around it is where the actual work is.

## Auth is where most of the time went

The spec says "MCP servers use OAuth 2.1 with PKCE." That sentence undersells how much code you write to get there.

You need:
- An authorization server with `/authorize` and `/token` endpoints
- PKCE (S256) verification on the token exchange
- Authorization server metadata at `.well-known/oauth-authorization-server`
- Protected resource metadata at `.well-known/oauth-protected-resource`
- Dynamic client registration (RFC 7591) at `/register` so clients you don't know about can register themselves
- A consent flow that's friendly enough for a non-developer to complete in a chat

Most of those endpoints were 30–80 lines of code each. The consent flow was the real time sink — a real login form, mobile-responsive, error states, accessible — and it's the part most existing OAuth tutorials hand-wave through.

Lesson: don't underestimate the consent screen. It's the highest-friction surface in your whole connector experience, and it gets shown to every user every time. Treat it like a checkout page, not a debug page.

## Schema design: spend more than you want to

The temptation when defining tools is to mirror your REST endpoints 1:1. `POST /entries` becomes `add_entry`. Done.

Don't. You'll regret it.

LLM tool design is closer to API design for a slightly distractible junior engineer. Names need to be specific. Descriptions need to clearly state what the tool does and what it returns — not just argument names. Schemas should have descriptions on every property.

A few specific lessons:

**Splitting reads and writes pays off.** We had a `manage_diary` tool that did both. The model called it correctly maybe 70% of the time. Splitting into `get_diary` (read) and `log_meal` (write) jumped that to 95%+.

**Annotations matter.** Once we added `readOnlyHint: true` and `destructiveHint: true` annotations to tools, Claude's behavior around confirmation became much better. It stopped asking "are you sure?" before reading data, and started asking before writing data — which is the right shape.

**Idempotency keys aren't optional.** First time the model retried a `log_meal` after a slow response, we got duplicate diary entries. Now every write tool takes a `clientRequestId` and we de-duplicate at the DB level via a unique constraint on `(user_id, client_request_id)`.

## Origin validation is more important than it sounds

The spec mandates Origin header validation as a DNS-rebinding defense. We almost skipped it in the v0 implementation because "no browser is going to call our MCP endpoint anyway."

That was wrong twice over.

First, browser-based MCP clients exist (claude.ai is one). Second, even without a browser client, the failure mode of *not* validating Origin is exactly the kind of thing a security audit will find six months in: an attacker controls a webpage, the victim visits it logged in to claude.ai or to a related service, and the attacker forges requests to your endpoint via DNS rebinding.

Implementation is ~10 lines. Don't skip it.

## CORS quirks for connector clients

Default app-wide CORS rarely fits what an MCP endpoint needs. We had `https://macroline.app` and our localhost dev origins on the allow-list, which was fine for the iOS client and fine for direct-server-to-server calls — but broke when claude.ai tried to fetch our `.well-known/oauth-authorization-server` cross-origin during connector setup.

Fix: a separate, narrower CORS policy mounted only on the MCP-related routes that includes claude.ai origins. The default global policy stays restricted.

## Response sizes — model context windows are smaller than you think

Tool responses get inlined into the model's context. A `get_diary` that returns 6 weeks of entries with all 12 fields each will easily blow past 25k tokens, which is the soft cap for inline tool responses in many client harnesses.

We learned to:
- Default ranges narrow (last 7 days)
- Strip fields the model doesn't need (timestamps as ISO strings, not full Date objects with timezones)
- Paginate aggressively
- Summarize where possible — for `get_diary` we could return per-day rollups instead of every entry

The model can always ask for more. It can't recover from a response that fills its context.

## What's still rough in the ecosystem

A few things that will get better but currently aren't great:

**Testing tools.** MCP Inspector is fine but it's not a full test harness. Writing automated tests for "does this tool description trigger the model correctly" requires running an actual model.

**Error UX in clients.** When your MCP server returns a JSON-RPC error, what the user sees in claude.ai varies. Sometimes a clean message, sometimes raw JSON, sometimes nothing.

**Rate limit conventions.** No standard for how MCP servers signal "back off." We're using HTTP 429 + Retry-After and hoping clients respect it.

## The high-order takeaway

Building an MCP server is more work than building a REST API, but less work than building a CLI + REST API + custom Slack bot + Zapier integration. It's net-better. And the moment your users start asking "can I get this in Claude," the work pays off in a way other integrations don't.

Worth doing. Worth doing correctly the first time.
