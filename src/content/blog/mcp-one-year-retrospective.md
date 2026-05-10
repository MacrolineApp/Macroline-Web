---
title: MCP turned one — what shipped, what didn't
description: Anthropic announced the Model Context Protocol in late 2024. A year and a quarter in, the protocol has stabilized in surprising ways and stalled in others. Here's what's actually in production, what got built and abandoned, and where I think the next year goes.
publishedAt: 2026-02-15
author: alex-rivera
tags: ["MCP", "AI tools", "protocols", "retrospective"]
---

The Model Context Protocol is roughly fifteen months old. Anthropic announced it in November 2024; the spec went 1.0 in January 2025; the broader ecosystem of clients and servers spent most of 2025 figuring out what they actually wanted to do with it. We're now far enough past the announcement to look at what stuck and what didn't.

I've been building on MCP since spring 2025, and I have opinions. Here's the field as I see it from inside the trench.

## What stuck

**Stdio transport for local tools.** The spec's MVP transport — JSON-RPC over stdin/stdout, with a server that the client spawns as a subprocess — turned out to be the right call. It's simple, it has zero auth surface for local-only tools, and it's the transport everyone deploys to first. ~90% of public MCP servers are stdio-only as of early 2026.

**HTTP transport for remote tools.** Took longer to settle. The original SSE-based transport (Streamable HTTP) shipped in mid-2025 after several iterations. By Q4 2025 most non-trivial remote MCP servers had migrated. The OAuth dance in front of HTTP MCP is still rough — every client implements it slightly differently — but the underlying transport is stable.

**Tools as the primary primitive.** The "tools, resources, prompts" trio in the spec assumed roughly equal weight at launch. In practice, tools dominated. Resources are barely used in the wild. Prompts shipped but client UIs around them are inconsistent. If you're building MCP, you're effectively building a tool list with maybe a few resources thrown in.

**Tool descriptions matter more than expected.** The single biggest performance lever in any MCP server is the prose description of what the tool does. A vague description gets misused or ignored; a precise one with a "when to use this" sentence gets used reliably. This is the part of MCP development that feels more like writing copy than writing code, and most servers don't take it seriously enough.

## What didn't ship the way we expected

**Standardized auth.** OAuth 2.0 + PKCE was sketched in the spec, but the actual flows that clients implement vary. Claude Desktop, Cursor, the OpenAI client adapter, and the various IDE integrations all have slightly different ideas of what "the OAuth flow" looks like. As a server author you end up with a `/.well-known/oauth-authorization-server` discovery doc, a `/oauth/authorize` endpoint, a `/oauth/token` endpoint, and a refresh-token contract — and you test it against the half-dozen clients that matter and pray.

**Resource subscriptions.** The spec includes a subscribe-to-resource-changes mechanism. Almost no clients implement it, almost no servers implement it. Real-time data through MCP mostly happens via tools that return current state when called, not via push subscriptions.

**Multi-tenant servers.** Lots of teams started 2025 thinking they'd build a single MCP server hosting many users. Auth complexity made this much harder than expected, and most production deployments became single-tenant per OAuth-issued token. Multi-tenant in the sense of "one infrastructure, many users" exists, but it's auth-isolated per request, not multi-tenant in the data-sharing sense.

**Sampling.** The spec includes a way for the server to ask the client to call its own LLM with provided context. Almost nothing uses this. The handful of servers that do use sampling get weird interactions with client cost models and feel like a hack. Probably a feature that should sunset.

## Where the surprise wins came from

**Agentic loops outside of chat.** I expected MCP to mostly be used in conversational chat (you ask Claude something, Claude calls an MCP tool, you see the result). What's actually emerged is automated agentic loops — cron-triggered, webhook-triggered, or part of long-running tasks where the LLM picks up MCP tools as part of a multi-step plan with no human in the loop. The Claude Agent SDK landed mid-2025 and accelerated this pattern. Claude Code (the CLI) also pushed it, since most Claude Code sessions involve chained MCP calls without per-call human approval.

**Domain-specific servers.** Generic MCP servers (file system, web search, etc.) are useful but commodity. The interesting servers in 2026 are domain-specific: nutrition data, code search across enterprise repos, internal operations APIs at large companies, specific scientific datasets. These have moats — a generic MCP server can't replace knowing the actual data you're serving.

**Cross-org integration.** The most surprising 2025 trend was companies exposing internal APIs through MCP for partner integrations rather than building partner-specific REST APIs. The model is "we already have this for our internal AI use; here's an OAuth-gated endpoint for yours." It's a strictly better partner-API story than the previous decade's REST sprawl, and I expect this to keep growing.

## Where I'd bet on the next twelve months

**Standardized tool-call telemetry.** Every server author currently invents their own logging. There's been informal discussion in MCP-spec channels about a standard format for "this tool was called, by this client, with these args, and returned this much data." Probably ships in some form by mid-2026.

**Better client capability negotiation.** The current `initialize` handshake exchanges capability lists but in practice clients announce a consistent capability set and servers ignore it. A more granular negotiation (this client supports streaming responses, that one doesn't, this one supports binary attachments, that one only text) would let servers actually adapt. Whether the spec catches up is an open question.

**A real OAuth profile.** The current ad-hoc-per-client OAuth situation is the biggest pain point in production MCP. Anthropic and the ecosystem need to converge on a specific OAuth profile (probably a stripped-down OIDC subset) that all clients implement identically. There's enough commercial pressure now — every enterprise rollout hits this wall — that I'd be surprised if 2026 ends without something.

**Tool versioning.** Right now if you change a tool's argument schema, you've broken every cached client conversation. There's no version negotiation. This is going to bite hard as servers mature and want to evolve their tool surface. Probably shows up as a `tool/v2/...` naming convention in practice before it hits the spec.

## What MCP is actually for, looking back

Fifteen months in, my read is: MCP is the protocol that makes "your data, in your AI" practical. Before MCP, getting Claude to use your private nutrition data, your internal documents, your team's cron job results, etc., required building either a custom client wrapper or a brittle "tell Claude to call this API and parse the response" prompt scaffold.

MCP collapses that into a structured contract. Anthropic gets a way to invoke your data without baking it into model weights. You get a way to expose your data without surrendering it to a vendor. The end user gets to ask their AI questions about their actual life, with citations they can verify.

That's a real win, even with the rough edges. Most of the friction now is at the auth layer, the client-discrepancy layer, and the long-tail-of-edge-cases layer — none of which require a protocol redesign. They require time, ecosystem maturity, and someone shipping the boring profile docs.

---

If you're building on MCP today: focus on tool descriptions, accept that your OAuth flow will need per-client tweaks, ignore resources/prompts/sampling for v1, and assume the agentic-loop case (not just chat) is half your production traffic. That's where I think the actual wins are at fifteen months in.
