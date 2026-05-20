---
title: Calorie targets after bariatric surgery — why your app should never refuse the number
description: A bariatric beta tester told us the iOS app wouldn't let her set 880 cal/day, even though her surgeon prescribed it. The bug is on us. But it's also a pattern in nearly every tracker on the App Store, and it tells you something about how the industry thinks about you.
publishedAt: 2026-05-13
author: maya-chen
tags: ["bariatric", "GLP-1", "evidence-based", "input validation", "clinical practice"]
---

A beta tester emailed the team last week. She'd had bariatric surgery a few months earlier, was on a medically supervised post-op plan, and her calorie target was **880 per day**. Two weeks of trying to set that number in Macroline's iOS app — and the input field refused. "Enter a valid value," the browser tooltip said.

She's right and the app was wrong. We've shipped the fix. But the larger question is the one worth writing about, because it sits underneath nearly every nutrition app on the App Store: **why does the input refuse a number a clinician already wrote down?**

## What's actually clinical here

A few facts that get lost when "1200 minimum" gets baked into nutrition apps as a kind of cultural default:

**Post-bariatric protocols sit in the 600–1000 kcal range for months after surgery, by design.** The American Society for Metabolic and Bariatric Surgery (ASMBS) clinical guidance describes a stage-by-stage protocol — clear liquids in the first week, then full liquids, then puréed, then soft solids, then a regular post-bariatric diet — with intake typically reaching only 800–1000 kcal/day by month two or three for sleeve gastrectomy and Roux-en-Y patients. Single-anastomosis duodeno-ileal bypass (SADI-S) and biliopancreatic diversion (BPD/DS) protocols can run lower. This isn't an emergency reading. It's the standard of care, monitored by the surgeon, the bariatric dietitian, and (often) labs every few weeks.

**Very low calorie diets (VLCDs) sit in the 450–800 kcal range and are also clinical.** Supervised VLCDs are used pre-bariatric to shrink liver volume before surgery, in select non-surgical weight-loss programs, and as part of some pharmacotherapy ramps. They are not "extreme dieting." They are a medical intervention with a body of published evidence behind them.

**GLP-1 receptor agonists routinely reduce intake below traditional "minimum" thresholds.** Patients on semaglutide and tirzepatide commonly report appetite at 30–50% of their pre-medication baseline. A patient who used to maintain at 2200 may eat 1100 comfortably for months. This is the medication doing what it's supposed to do.

The point isn't that 880 calories is right for any specific person. It might be wildly wrong, depending on whose 880 we're talking about. The point is that **the number 880 is not, by itself, pathological**. It can be exactly what a competent clinician prescribed, after careful consideration of body composition, surgery type, time since procedure, and labs.

When a tracking app refuses to accept it, the app is making a medical judgment it isn't qualified to make.

## Where the 1200-calorie floor comes from

It's worth pausing on this, because it's almost universal in consumer trackers.

The "minimum 1200 calories for women, 1500 for men" line traces back to popular dieting guidance in the 1990s, codified in some commercial weight-loss programs and adopted unreflexively across the consumer app ecosystem. It is **not in current ACSM, AHA, AND, or ASMBS guidance** as a categorical floor for all adults. The current evidence-based view, where there is one, is that calorie targets are individualized — a function of body composition, metabolic context, medical history, and (when relevant) surgical or pharmacological intervention.

The 1200-floor lives on in trackers for two reasons. The first is genuine: some app builders are trying, awkwardly, to discourage disordered restriction. The second is liability theater: it's easier to refuse low numbers than to think clearly about which low numbers are which.

But here's what the refusal actually does:

- A bariatric patient gets told by her surgeon to track at 800. The app refuses. She moves to a competitor that accepts the number — usually a less careful competitor — or she gives up tracking and loses the most useful tool she had for catching protein gaps.
- A GLP-1 patient eating 1050 because she literally cannot eat more gets told by the app that her *intake* is dangerous. She blames herself. She over-rides and logs phantom food. The app's data is now garbage.
- A pre-bariatric VLCD patient on a 700-kcal liver-shrinking protocol can't track at all for the four weeks before surgery — the period when adherence matters most.

**The number isn't the danger. Refusing to trust the user (and their clinician) is.**

## What "disordered restriction" actually looks like — and what to do about it

The harder, more honest question is: how does an app distinguish a clinically prescribed low target from someone in active disorder?

The honest answer is: it can't. Not from a single number in a goal field. A 19-year-old logging 600 with no other context might be a pre-bariatric patient, an athlete in pre-competition water-cut (also clinical), or someone in a real eating disorder. The number alone won't tell you.

What you can do — and what I'd push every tracker to do, including ours — is **support the clinician relationship rather than substitute for it**. That looks like:

1. **Accept the number.** Don't quantize. Don't impose a "common-sense" floor. Validate against obvious typos (zero, negative, an absurd >20,000) and otherwise trust the user.
2. **Surface a contextual note for low targets** the first time a user sets one. Not blocking, not paternalistic: a one-time "If a clinician didn't prescribe this, we'd encourage you to talk to one before targeting it — here are resources." Acknowledge that the user may already be working with one.
3. **Don't notify them they're below a goal.** A bariatric patient hitting 720 at 7 PM doesn't need a push notification telling them they're under. They know.
4. **Provide eating-disorder resources discoverably.** The NEDA helpline (1-800-931-2237, U.S.) and equivalent international lines should be findable without being moralized about.
5. **Let them export.** A user who decides this isn't the right tool should be able to take their data with them — to a clinician's office, to a different app, anywhere. Trapping data is its own quiet harm.

The framing I'd hold onto, both as a clinician and as a tool designer, is: **the user is the expert on the user's situation, in collaboration with their clinical team**. An app's job is to make tracking honest, not to make medical decisions through input validation.

## What Macroline got wrong, and the fix

The actual bug in the iOS Goals editor was technically not a "minimum" — it was a *step* constraint. The HTML number input had `step="50"`, which means the browser refuses any value that isn't a multiple of 50. 880 is not a multiple of 50. The error message — "Enter a valid value" — is uninformative to a user who has no reason to know the input is quantized.

The macros had `step="5"`, which broke values like 33 g protein. The calorie input also had a 500-kcal minimum baked into the backend validation. All three constraints were unnecessary, none were medical, and combined they made the app's input layer functionally hostile to anyone with a non-round number.

We've shipped fixes across all three layers — the iOS app, the web app, and the backend. The new behavior: typo protection only. The minimum is 100, which exists to catch zero/single-digit input errors. The step is 1.

This was a small bug with a large message attached. If your tracker won't let you set the number your surgeon wrote down, that's a design statement about how it sees you. We'd rather not make that statement.

---

*Macroline is a tracking tool, not medical advice. Targets, including the low-calorie ranges discussed above, should be set in consultation with your bariatric team, GLP-1 prescriber, or registered dietitian. If you or someone you know is struggling with disordered eating, the National Eating Disorders Association helpline is 1-800-931-2237 (U.S.); international resources are at neda.nationaleatingdisorders.org/help-support/contact-helpline.*
