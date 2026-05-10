---
title: Why I don't connect my food log to my AI assistant
description: I work on AI tooling. I build MCP servers. And I deliberately do not connect my personal nutrition data to a cloud AI assistant. Here's the threat model, what 'connected' actually exposes, and the version of this I do use.
publishedAt: 2026-02-26
author: alex-rivera
tags: ["AI privacy", "MCP", "personal data", "threat modeling"]
---

I get asked this a lot: "You build MCP servers for nutrition data. Is your own food log connected to Claude or ChatGPT or whatever?"

No. Mine's local-only. The diary lives on my phone and on the server my account talks to, and there's no MCP token issued for my account. I made that call deliberately and I'd recommend most people make it deliberately too — in either direction. The point is that "connected to AI" is a real choice with real tradeoffs and most people are making it without thinking about either.

This isn't a "AI bad" argument. I work on this stuff. It's a "here's the actual threat model, decide accordingly" argument.

## What 'connected to AI' actually means

When you connect a food-tracking app to a cloud AI (whether through MCP, an OpenAPI integration, a vendor-specific connector, or whatever), here's what happens at the data layer:

1. The AI provider (Anthropic, OpenAI, etc.) holds an OAuth token for your account.
2. When you have a conversation that triggers an AI tool call against your data, the AI provider's infrastructure sends a request to the app's backend (or your local MCP server).
3. The app responds with the requested data — which might be your day's diary, your last week of macros, your medications list, or whatever the tool exposes.
4. That data flows back through the AI provider's inference infrastructure to generate a response.
5. Depending on the provider's data handling, the data may or may not be retained, used for training, or available to provider employees.

Steps 4 and 5 are the part most people don't think about. The data isn't just "in the AI" abstractly — it's flowing through someone else's compute, getting logged in trace systems, and possibly getting retained for unspecified periods.

## The four privacy layers worth distinguishing

I think about it in four layers, from least to most exposed:

**Layer 1: Local-only.** Your data lives on your device(s) and on the app's first-party servers. No AI provider has a token. No external system has access. This is what I run.

**Layer 2: AI on a per-query opt-in.** You can paste data into Claude or ChatGPT for a specific question ("here's my macros for the week, what should I tweak"). The AI provider sees just what you paste. No persistent connection.

**Layer 3: AI with a persistent token, but each tool call is auditable.** You've connected your data to Claude via MCP, but you can see every tool call in the conversation, you can revoke the token at any time, and the AI provider's terms commit to not training on this data. This is the layer most "connect to AI" features sit at, and where most people are.

**Layer 4: AI with deep, opaque integration.** Some tracker apps now embed AI features inside their own product, where AI requests flow through their infrastructure to a third-party model with terms you didn't separately consent to. Often advertised as "powered by [Model X]." You have no visibility into what's sent on each request. Hardest to audit, easiest to opt out of by just not using the feature.

For my own food data, Layers 1 and 2 are fine. Layer 3 I evaluate per-app. Layer 4 I avoid by default.

## What's actually in a food log that matters

People underestimate how revealing a year of food data is. From my own logs you could derive:

- **Eating disorder history.** Patterns of restriction-and-binge are visible in calorie distribution. Periods of <1200 kcal followed by 4000+ kcal stretches are diagnostic.
- **GLP-1 use.** Sharp drop in caloric intake on consistent days, reduced eating frequency, particular avoidance patterns (high-fat meals → reflux). All visible in the data.
- **Medical conditions.** Bowel-disease-friendly diet patterns. Allergen avoidance. Pregnancy markers (specific aversion patterns + later cravings).
- **Mental health correlates.** Stress eating during specific weeks (Tuesday meetings, end-of-month sprints). Late-night carb spikes during depressive episodes.
- **Travel and lifestyle.** Restaurant patterns geo-locate you. Time-zone-shifted eating implies travel. Cluster-eating implies hosting visitors.
- **Relationship status.** "Cooking for one" vs "cooking for two" patterns are visible in portion sizes and meal complexity.

This isn't theoretical. With a year of granular food data, a sufficiently motivated party can infer most of the above with high confidence.

## Why connecting it to a cloud AI is different from connecting it to anything else

You probably already share your food data with the tracker app's own backend. That's necessary for the app to work. So why does adding an AI connection change the threat profile?

Three reasons:

**The data crosses a provider boundary.** Your tracker app has agreed-upon terms with you. The AI provider has separate terms. When you connect them, your data flows under both, and the weakest link sets the floor.

**AI provider trace logs and request data are different from app logs.** Most apps log "user X requested their diary" with the request metadata. AI provider trace systems log the actual content (tool call args + response content) for debugging and quality assurance. The retention policies and access controls on those traces are separate from the app's, and have historically been less restrictive.

**Inference is computationally expensive, so it gets routed through different infrastructure.** Your tracker's backend probably runs in a single region under a known compliance framework (SOC 2, HIPAA-adjacent, whatever). AI inference often runs across multiple regions, in shared compute, possibly through partners. The compliance footprint widens.

These aren't show-stoppers. They're items to weigh against the value of the AI feature.

## The version of this I do use

For the record, I'm not anti-AI for personal data. Here's how I actually use AI with my food log, from Layer 2:

When I want to think through a specific question — "should I bump my carbs this week given my training volume?" — I'll paste a week's macro summary (totals, no per-meal data) into a Claude conversation and discuss. The data shared is aggregated, not granular. The conversation isn't persistent in any of my apps. I get the AI value without giving the AI provider a persistent window into my eating patterns.

This is more friction than "ask Claude to look at my diary." It's also a better fit for how I personally want to share data. Friction is sometimes the feature.

## What to think about before connecting

If you're considering connecting your tracker to an AI assistant, the questions worth asking yourself:

1. **What value am I getting from the connection that I can't get from copy-pasting summaries?** If the answer is "convenience," weigh that against the persistent-data-access cost.
2. **Does the AI provider's terms commit to not training on this data?** Most current Anthropic/OpenAI enterprise terms do; consumer terms vary.
3. **Can I revoke the token easily, and would I notice if the connection started behaving weirdly?** If revocation is buried five menus deep, that's a flag.
4. **Am I comfortable with the worst-case scenario being public?** Not "would it be public" but "if a breach happened tomorrow, would I be okay?"
5. **What's the data-retention story on the provider side?** Anthropic's standard is currently around 30 days for trace data. Other providers vary.

These are personal calls. None of them have a single right answer.

## Why this is worth thinking about for nutrition specifically

Most personal data we share with AI is text — emails, drafts, documents. We've been giving search engines documents for two decades, and our intuition for "this is normal" mostly works.

Granular food data is different. It's structured, time-series, behaviorally rich, and hard to reconstruct from text alone. The aggregate signal is much higher than people expect. Connecting it to a cloud AI is a legitimate productivity choice and a legitimate privacy concern simultaneously, and the right answer is *deliberately picking* a posture rather than defaulting in.

---

I work on this stuff and my answer for me is local-only. Yours might be different. The thing I'd push back on is the default — neither "connect everything because AI is the future" nor "connect nothing because AI is scary" is a serious posture. Sit with the threat model for an hour, decide where you actually want to be on the four-layer scale, and then build accordingly.
