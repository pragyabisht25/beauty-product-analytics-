# Interview Q&A — Based on This Project

## 1. Walk me through this project in two minutes.

I built an end-to-end product analytics case study for a beauty
e-commerce platform: synthetic but realistic data across customers,
products, behavioural events, and orders; SQL/Python analysis across
customer behaviour, product performance, pricing, ratings, and the
discovery funnel; and I used the findings to define a real product
problem — choice-heavy subcategories convert at roughly half the rate of
low-choice ones — then scoped an MVP feature ("Compare Products"), wrote
a PRD, defined success metrics, and designed an A/B test to validate it.

## 2. How did you identify the core problem instead of just picking one upfront?

I started from the funnel, not from a feature idea. I looked at where
views, wishlists, carts, and purchases diverged across categories and
subcategories. Category-level data didn't show a clear gap — Skincare and
Makeup were both the most-viewed and most-purchased. The gap only
appeared at the subcategory level, once I split subcategories by SKU
count. That's when the "choice-heavy vs low-choice" pattern showed up:
roughly 11% vs 20% view→purchase conversion. I treated that split as a
hypothesis to test with the data, not an assumption.

## 3. Why "Compare Products" and not a bigger discount or a better recommendation algorithm?

Because the data didn't support those as the primary lever. Discount% was
correlated with cart adds more than with final purchase, and rating had
almost no relationship with conversion across bands (roughly 15-16%
regardless of rating). If price or perceived quality were the blocker,
I'd expect those metrics to move more with conversion. What did line up
was decision volume: subcategories with many similar SKUs saw worse
drop-off at every funnel stage, plus high wishlist activity that never
converted — that's a "shortlisting but not deciding" signature, which
points at comparison friction, not price or quality.

## 4. How would you validate that this is really a causal effect and not just correlation?

I wouldn't ship it platform-wide off analysis alone — that's exactly why
the case study proposes an A/B test. Randomize users browsing the six
choice-heavy subcategories into control (current experience) and variant
(Compare feature), and measure view→purchase conversion as the primary
metric with clear guardrails (overall site conversion, page load time,
PDP engagement time) so I can catch regressions the observational data
wouldn't show me.

## 5. What would you do if the A/B test showed high adoption but no conversion lift?

That result would tell me the bottleneck isn't comparison friction after
all — probably price sensitivity, trust, or something else not captured
in this dataset. I'd segment the variant group by whether they used
Compare and still didn't buy, look at what they compared (e.g., did they
compare against a much cheaper option and abandon?), and consider testing
a different lever — like transparent pricing/value messaging — before
investing further in the comparison UI itself.

## 6. How did you decide on the success metrics and guardrails?

Primary metric had to be the thing closest to the actual problem —
view→purchase conversion in choice-heavy subcategories, since that's what
the case study is trying to move. Secondary metrics (adoption,
comparison-to-purchase conversion) tell me *how* the feature is being
used, which matters for the next iteration even if the primary metric
moves. Guardrails protect against the feature working "locally" — more
comparisons, more time on the comparison screen — while quietly hurting
overall performance or PDP engagement elsewhere.

## 7. What are the limitations of this analysis?

It's the biggest caveat of the whole project: this is synthetic,
observational data. The choice-heavy conversion gap is a real pattern in
the dataset, but real platforms have confounders this dataset doesn't
model — brand trust, delivery time, product photography quality, and so
on. I called this out explicitly in the case study rather than
overclaiming causality, and that's exactly why the recommendation is "run
the A/B test," not "ship platform-wide."

## 8. How would this project change if you had real production data instead of synthetic data?

I'd expect more noise and more confounders, so I'd want to run this
analysis with proper significance testing (not just eyeballing rate
differences), check for seasonality and marketing-campaign effects that
could distort the funnel numbers, and validate the "choice-heavy" SKU
threshold against actual user research (surveys, session recordings)
instead of assuming SKU count alone is the right proxy for decision
difficulty.

## 9. Why did you scope the MVP the way you did (max 3 products, same subcategory only)?

Two reasons. First, the data problem is subcategory-specific — comparing
across subcategories (a serum vs a lotion) doesn't map to a real user
need, so scoping to same-subcategory keeps the feature focused on the
actual evidence. Second, capping at 3 keeps the UI usable on mobile and
avoids scope creep into a bigger recommendation-engine project before
we've validated the core hypothesis with a simple version.

## 10. If you had to pick one number from this whole project to put in front of a VP, what would it be and why?

The 9-point gap: 11% view→purchase conversion in choice-heavy
subcategories vs 20% in low-choice ones. It's a single, concrete number
that (a) quantifies a real revenue opportunity, (b) is specific enough to
act on (it names which subcategories to fix first), and (c) is honest
about being a correlation that needs a test — which is the kind of
number a VP can approve a scoped experiment against, rather than a vague
"users seem confused" narrative.
