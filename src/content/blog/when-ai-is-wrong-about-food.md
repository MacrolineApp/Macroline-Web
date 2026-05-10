---
title: When AI is wrong about food (and how to spot it)
description: AI is good enough at parsing meals into macros that the failure modes are no longer obvious. The wrong number doesn't look wrong. Here's a taxonomy of the specific ways AI gets food data wrong, and what to look for in your own logs.
publishedAt: 2026-03-03
author: alex-rivera
tags: ["AI accuracy", "food data", "verification", "edge cases"]
---

The "AI describes a meal" feature has gotten very good in the last 18 months. You say "two scrambled eggs, a slice of sourdough, half an avocado, and a coffee with cream" and you get back something that looks like a complete macro breakdown. It usually IS a complete macro breakdown. That's the problem.

When AI is right, it's right. When AI is wrong, the answer doesn't look wrong. It looks like a plausibly-shaped macro breakdown that happens to be 30% off in one nutrient. You can't visually tell the difference, and most users don't try.

I've been auditing AI-generated food data — both for Macroline and other projects — for over a year now. Here's the taxonomy of failure modes I keep seeing.

## Failure mode 1: Plausible portion inflation

AI parsing routinely picks middle-of-the-distribution portion sizes when the meal description is ambiguous. "A bowl of oatmeal" → AI assumes 1.5 cups cooked, which is 1 cup dry oats. Most actual people are eating ½ to ¾ cup dry oats. The AI's estimate is 60-100% too high.

This is the most common failure mode and the hardest one to catch by eye. The macro breakdown looks "reasonable" — it just reflects a portion that's 50% larger than what you actually ate. Across a day, you log 200-400 calories of food you didn't eat, you go to bed having "eaten 2000," and you're actually closer to 1700.

**What to look for**: any time the parsed entry's serving description is "a bowl," "a plate," "a portion," etc. — without a specific weight or measure — assume the AI inflated. Either provide a specific quantity in your description, or visually check the calorie estimate against your normal portion size.

## Failure mode 2: The brand-substitute

If you say "I had a Chipotle bowl with chicken, brown rice, black beans, fajita veggies, mild salsa, guac," the AI knows Chipotle's official nutrition values for those ingredients and (when working well) returns Chipotle-specific data.

If you say "a chicken burrito bowl with rice and beans," the AI doesn't know it was Chipotle. It pulls a generic recipe from training data. Generic chicken burrito bowls in published recipes are often 30-40% more calorically dense than Chipotle's, because home recipes use more oil and richer protein cuts than the chain.

Same meal, different description, different macros — and not because the math is wrong. Because "chicken burrito bowl" matches a different reference set than "Chipotle chicken bowl."

**What to look for**: brand name in the description. Always specify the chain or restaurant if it's a chain meal. "Olive Garden chicken parmigiana" gets very different macros than "chicken parmigiana with pasta."

## Failure mode 3: Hidden cooking-method assumptions

"Grilled chicken" vs "fried chicken" vs "pan-seared chicken" produce very different fat profiles, and AI handles this well. What it doesn't handle well is the *implied* cooking method.

"Salmon with rice and broccoli" — how was the salmon cooked? AI guesses. If it guesses pan-seared with butter, you get one fat profile. If it guesses baked plain, another. The user typically meant something specific (because they cooked it), and the AI's guess is unverifiable from the description.

A frustrating second-order effect: if the AI guesses "pan-seared with butter" and adds 10g of fat for the cooking step, but you actually baked it dry, your log over-counts ~90 calories on that meal. Repeated across a week, that's a measurable cut error.

**What to look for**: when a parsed entry's fat content seems higher than you expected, check whether the AI added an inferred cooking-fat component. Macroline's tier badge is helpful here — anything that says "estimated" or "unverified" should be eyeball-checked against your actual cooking.

## Failure mode 4: Compound foods with optimistic ingredient lists

"A salad with greens, chicken, avocado, almonds, blue cheese, and balsamic vinaigrette" gets parsed reasonably accurately for the components — but the dressing volume is almost always estimated low. AI defaults to 1-2 tablespoons of vinaigrette for a "salad with dressing." Most restaurant salads ship with 4-6 tablespoons.

Vinaigrette at 60-80 calories per tablespoon × an unaccounted 3 tablespoons = 200 silent calories.

The same logic applies to:
- **Cooking oil for sautéed vegetables** (AI assumes 1 tsp; restaurants use 2-3 tsp)
- **Mayo on sandwiches** (AI assumes 1 tablespoon; deli portions are 2-3)
- **Sauce on pasta dishes** (AI undercounts unless told otherwise)

**What to look for**: any mention of a sauce, dressing, or oil. Bias the estimate up if it's a restaurant meal, hold the estimate as-is if you cooked at home.

## Failure mode 5: The semantic-near-miss

"Greek yogurt" → AI returns the macros for full-fat plain Greek yogurt, ~120 calories per cup. You ate non-fat plain Greek yogurt at 90 calories. Or you ate flavored Greek yogurt at 180 calories. None of these are visually different in the parse output unless you check specifically.

Same pattern across:
- Milk (whole vs 2% vs skim)
- Cheese (regular vs reduced-fat)
- Bread (white vs sourdough vs whole grain — the macros differ meaningfully)
- Pasta (regular vs whole-wheat vs chickpea)

The AI can't tell which version you had unless you specified.

**What to look for**: any food where multiple variants exist with different macro profiles. Dairy is the worst offender. If your log has "yogurt" without a specific brand or fat percentage, the parsed values are a coin flip.

## Failure mode 6: Made-up branded products

This is the embarrassing one. If you say "I had a Chompers protein bar," and Chompers is a brand the AI doesn't know, two things can happen:

- AI says "I don't have data on Chompers, here's a generic protein bar estimate" — fine, you handle it.
- AI fabricates plausible-looking macros for the bar — bad. You log them as if they were real.

The hallucinated case is rarer in 2026 than it was in 2023, but not extinct. The fabricated values usually look like a "typical protein bar": 200 calories, 20g protein, 25g carbs, 7g fat. They are not the real values for your specific bar.

**What to look for**: any branded product with confident-looking macros from a brand you've never seen called out before. If the parsed entry doesn't have a tier badge of "authoritative," treat it as a guess. Verify by scanning the actual barcode if possible.

## How to catch these in your own log

The single best habit is to **trust the tier badges**. If your tracker shows a source tier on each food entry — Macroline does — anything below "computed" should get a quick gut-check before you accept it as fact.

Beyond that:

**Spot-check the ones you remember best.** If you ate a meal yesterday you cooked yourself and you know the ingredients, look at the AI-parsed entry. Does the calorie total feel right within ±10%? If not, you've found a systematic bias to correct for.

**Sample the chains you eat at.** If you eat at Sweetgreen weekly, check one Sweetgreen entry against Sweetgreen's published macros. If they match, you can trust future Sweetgreen entries. If they don't, you know to specify "Sweetgreen" explicitly in your descriptions.

**Notice systematic drift across weeks.** If your scale isn't moving and your "tracked deficit" says it should, the most likely explanation is silent over-counting somewhere. AI-parsed meals with hidden cooking oils and underestimated dressings are a frequent culprit.

## The principle

AI food parsing is good at giving you a fast, plausible answer. It's not necessarily good at giving you a *correct* answer. The two get conflated because the answer is presented with the same confidence either way.

Provenance — which Macroline makes visible — closes some of this gap. So does the simple practice of giving more context in your meal descriptions. "Grilled chicken with rice" gets you AI's best guess. "6 oz grilled chicken thigh with 1 cup cooked white rice and 1 tablespoon olive oil for cooking" gets you something much closer to the true number.

---

When AI is right about food, it's right enough that nobody notices. When AI is wrong about food, nobody notices that either. The tools to mitigate this — explicit portion specs, brand callouts, tier-badge awareness, periodic ground-truth checks — aren't AI features. They're user habits. Build them.
