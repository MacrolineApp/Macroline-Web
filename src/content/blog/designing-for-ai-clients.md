---
title: Designing for AI clients vs. human clients — same data, different shape
description: A REST API for humans and an MCP server for AI agents look superficially similar. They aren't. The contracts, error semantics, and data shapes that work for one are quietly bad for the other. Here's what the second-class consumer of your API actually needs.
publishedAt: 2026-03-18
author: alex-rivera
tags: ["MCP", "API design", "AI agents", "developer experience"]
---

I keep seeing teams ship MCP servers that are thin wrappers around their existing REST API. The reasoning is sensible: we have an API, the AI just calls the same endpoints, why duplicate work? In practice the AI does worse with that surface than humans do, and the team spends the next quarter patching the difference one tool at a time.

The fix isn't a different API. It's understanding what an AI agent actually needs from a tool, vs. what a human (or human-built client) needs.

I've been building MCP servers since spring 2025 and a REST-API-for-humans architect for longer. The differences that matter, in my experience:

## Difference 1: Error semantics

A human client treats a 404 differently than a 500 differently than a 422. The codes carry meaning that the calling code (which a human wrote) interprets correctly.

An AI agent reads error messages as text and decides what to do based on the prose. A 404 with body `{"error": "not_found"}` and a 500 with body `{"error": "internal_error"}` look like the same kind of failure to the agent: "the call didn't work, try something else." The agent often retries the wrong way — because the error text didn't tell it whether retry was reasonable.

The AI-friendly version of an error is a paragraph explaining what happened, what the agent should do next, and what arguments to provide. Something like:

```json
{
  "error": "food_not_found",
  "message": "No food in the catalog matches 'banana smoothie'.
              Try the more specific name (brand + product),
              or call create_custom_food with the macro values
              if this is a homemade recipe."
}
```

This is bad REST design (errors should be terse), but it's good MCP design. The agent uses the prose to plan its next call.

## Difference 2: Argument schemas need natural-language descriptions

A human client developer reads your OpenAPI spec, understands the field names, writes correct calls. The field name `consumedAt` makes sense to a human; they know it's an ISO timestamp.

An AI agent infers from the description what the field expects. `consumedAt: string (ISO 8601 datetime in UTC, e.g. 2026-03-18T14:30:00Z)` works. `consumedAt: string` does not. The agent will pass `"3/18/2026 2:30 PM"` and your endpoint will 422.

Your tool descriptions need to be over-specified for AI consumption — describe the format, the units, the time zone semantics, the edge cases. None of this is needed for human-built clients, but it's the difference between an agent that works and an agent that fails 30% of the time on subtle parsing issues.

## Difference 3: Pagination and listing semantics

REST APIs typically return paginated results: `?limit=20&offset=0`, with a `next_page_token` or similar. Human clients write loops to walk pagination.

AI agents don't reliably walk pagination. They request the first page, look at the result, decide whether to continue. The cost of getting the agent to walk all 14 pages of your search results is high — usually it'll just respond based on the first 20 items and call it good.

For AI-friendly listing tools:

- Default page size should be the *useful* size, not the *server-load* size. If 50 results is a reasonable view of "the user's recent foods," return 50, not 10.
- `next_page_token` is fine as a concept but include in the response prose: "showing first 50 of N total. Call this tool with `cursor: ...` to see more if needed."
- Better: provide a separate "browse" tool for paginated walks and a "summary" tool for overviews. Different purposes, different shapes.

## Difference 4: Tools that return state should return state, not deltas

Human clients are good at maintaining client-side state. They sync once, get a delta stream, apply changes locally. The agent doesn't have local state. Each tool call is roughly stateless — what it knows, it knows from the response.

This means agent tools should return the full current state on each call, not just what changed. "Get today's diary" should give the agent the entire current day, even if 95% is unchanged from the last call. Trying to be clever with partial responses ("here are the new entries since your last call") confuses agents because they can't reliably reconstruct full state.

This costs more bandwidth. It pays for itself in correctness.

## Difference 5: Side effects need explicit confirmation

Human-driven clients are typically structured so the user clicks a confirmation before a destructive action. The API doesn't need to confirm — the human did.

Agents have no equivalent. If your tool deletes data on call, the agent will sometimes call it speculatively. "Let me try deleting that and see if it works" is a real failure mode I've seen.

Two patterns help:

**Two-step flow.** A `delete_diary_entry` tool returns "are you sure" without actually deleting. A second tool with `confirm: true` does the delete. The agent has to deliberately call the second one.

**Idempotent destructive operations.** If your delete is idempotent and tied to a request ID the agent generated, the agent can be replayed safely. (Your existing `clientRequestId` patterns help here too.)

## Difference 6: Don't confuse identifiers and labels

Human clients pass UUIDs around all day. They don't expect to display them or remember them. The agent does the opposite — it works in human-readable text most of the time.

A tool that takes a `food_id` (UUID) as an argument is hard for the agent to use unless there's a separate `search_foods_by_name` tool that returns ID + name pairs. Otherwise the agent has to fabricate a UUID, which it can't.

A tool that takes `food_name` as an argument and resolves it server-side ("yogurt → returns the most-confirmed yogurt entry") is much more agent-friendly. The agent describes what it wants in prose; the server does the lookup.

## Difference 7: Documentation lives in the tool description

For a REST API, you document each endpoint in OpenAPI spec, in API reference docs, in ADRs, in the developer portal. Humans read those.

For an MCP server, the agent's "documentation" is whatever you put in the tool description. Period. If the agent doesn't know about a tool, the agent won't use it. If the description is two sentences, the agent has two sentences to work from. If you say "this tool searches foods" but don't mention that it supports brand-prefixed queries, the agent won't try them.

I'd write the tool description as a small persuasive essay: what the tool does, when to use it, when not to use it, what arguments work well, what failure modes to expect, what the response shape means. 200-400 words per tool. It's the highest-leverage code you write in an MCP server, and most servers underspend on it.

## What stays the same

Most of the lower-level engineering carries across. Auth is auth. Rate limiting is rate limiting. Caching is caching. Database queries are database queries. The differences are in the API surface and the response shapes, not in the infrastructure.

You also still want clean, maintainable code. The MCP server should be a thin layer that exposes domain operations as tools — not a layer that re-implements the domain. The shared internal service handles the actual business logic; the MCP layer translates request shapes and adds the prose.

## A concrete example from Macroline

The `search_foods` MCP tool takes a `query: string` and an optional `limit: number`. Its description is roughly: "Search the food database. Match against name and brand. Returns up to `limit` results sorted by confirmation count (most-trusted first). Each result includes id, name, brand, serving description, calories, macros, and source tier (authoritative/computed/estimated/unverified). Use the source tier to decide whether to use the value as-is or to ask the user to verify."

The same logic running under `GET /api/foods/search` for the human-driven web app returns the same data — but the human-driven UI doesn't need the source-tier-as-prose explanation, because the badge component renders it visually. The agent does need it. The same data, different shape.

---

If you're building MCP servers and finding the agent unreliable, audit your tool descriptions and your error semantics first. Those are usually the gap. The data isn't wrong; the surface is wrong. The agent is a different kind of consumer, and it deserves a different kind of API.
