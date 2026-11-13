# Case Study: Beauty Product Growth & Recommendation Analytics

**Framework:** Problem → Evidence → Insight → Opportunity → Proposed Solution → MVP → Metrics → Experiment

---

## 1. Business Context

A beauty & cosmetics e-commerce platform (Skincare, Makeup, Haircare,
Fragrance, Personal Care) wants to grow product discovery, conversion,
engagement, and repeat purchases. This case study walks through a full
product-analytics investigation on synthetic but internally-consistent
platform data: 6,000 customers, 330 products, ~200K behavioural events,
and ~16,000 orders.

## 2. Evidence — What the Data Shows

**Discovery funnel is healthy at the top, leaky in the middle.**
Across the platform: 100,277 product views → 31,904 add-to-carts (31.8%
view→cart) → 16,252 purchases (50.9% cart→purchase). Roughly 1 in 6 product
views (16.2%) ever becomes a purchase.

**Browsing and buying don't line up by category.** Skincare and Makeup are
the two most-viewed *and* most-purchased categories, so there's no simple
"discovery gap" at the category level — the real gap only shows up one
level deeper, at the subcategory level.

**Choice-heavy subcategories convert at roughly half the rate of
low-choice ones.** Subcategories with 20+ near-identical SKUs (Moisturizer,
Face Serum, Foundation, Lipstick, Shampoo, Sunscreen) show a view→purchase
rate around **11%**, versus **20%** for subcategories with fewer SKUs
(e.g., Blush, Body Lotion). The drop-off is worse at *every* stage in
choice-heavy subcategories: 75% of views never reach the cart (vs 63% in
low-choice subcategories), and even after add-to-cart, purchase completion
is weaker (56% drop-off vs 46%).

**This isn't a wishlist-awareness problem — people are shortlisting, just
not deciding.** 43 products sit in the "high wishlist, low wishlist→purchase"
bucket, and 60 products are rated 4.3+ yet convert below the platform
median — evidence that quality perception alone isn't what's blocking the
purchase decision.

**Discount is associated with cart adds more than with final purchase.**
Correlation between discount% and view→cart rate is 0.54, versus 0.64 for
view→purchase — close enough that we should be cautious reading too much
into the difference, and in any case this is an observational correlation:
price-sensitive shoppers may simply gravitate toward already-discounted
items, so we can't claim discounting *causes* more purchases without a
controlled test.

**Rating has a much weaker relationship with conversion than expected.**
View→purchase conversion barely moves across rating bands (roughly 15-16%
whether a product is rated 3.5 or 4.8), which further supports that the
bottleneck is upstream of "is this a good product" — it's "which one do I
pick."

*(Supporting charts: `charts/02_choice_heavy_conversion.png`,
`charts/03_discount_vs_conversion.png`, `charts/04_overall_funnel.png`;
full numbers in `docs/analysis_output.txt` and `data/derived/`.)*

## 3. Insight

Users in choice-heavy subcategories show all the signals of *active
interest* — high views, high wishlist activity — but convert at roughly
half the rate of users browsing subcategories with fewer, more
differentiated options. Ratings and discounts, the two levers most product
teams reach for first, explain very little of this gap. The pattern points
to **decision friction from too many similar options**, not a lack of
interest or a quality/price problem.

## 4. Product Opportunity

**Help users compare similar products quickly, so shortlisting turns into
a confident decision instead of a stalled one.**

If the blocker is "I've viewed and even wishlisted four similar
moisturizers, but I can't tell which one is actually different or better
for me," then the fix isn't more product listings or bigger discounts —
it's a lightweight way to put a short list side by side.

## 5. Proposed Solution: "Compare Products"

Let users select up to 3 products **within the same subcategory** and see
them side by side on price, discount, rating, reviews, and key listed
attributes (skin/hair suitability, key benefits) — with a direct
add-to-cart action from the comparison screen. Full detail in
`docs/PRD.md`.

## 6. MVP

- "Add to Compare" on listing-page cards and the product detail page
  (max 3, same subcategory only)
- Compare tray + comparison screen with core attributes and per-item
  add-to-cart
- "Compare with similar products" prompt on the product detail page for
  choice-heavy subcategories specifically (where the data shows the
  problem concentrated)
- Out of scope for v1: cross-subcategory comparison, AI recommendations,
  ingredient-matching logic, comparing review *content*

## 7. Success Metrics

- **Primary:** view→purchase conversion in choice-heavy subcategories
- **Secondary:** feature adoption rate, comparison-to-purchase conversion,
  view→cart rate in choice-heavy subcategories, repeat feature usage
- **Guardrails:** overall site conversion, product detail page engagement
  time, listing-page load time

## 8. Experiment Design (A/B Test)

**Hypothesis:** Giving users a low-effort way to compare similar products
within choice-heavy subcategories will reduce decision friction and
increase view→purchase conversion, without hurting overall site
performance.

- **Population:** Sessions/users browsing choice-heavy subcategories
  (Moisturizer, Face Serum, Foundation, Lipstick, Shampoo, Sunscreen),
  randomized at the user level to avoid contamination.
- **Control:** Existing product experience (no Compare feature).
- **Variant:** Product listing + PDP with "Add to Compare" and the
  comparison screen enabled.
- **Primary metric:** View→purchase conversion rate within choice-heavy
  subcategories.
- **Secondary metrics:** Feature adoption rate, comparison-to-purchase
  conversion, view→cart rate, cart→purchase rate.
- **Guardrail metrics:** Overall conversion rate (platform-wide, to catch
  any negative spillover), average page load time, PDP engagement time.
- **Duration/sample size:** Run long enough to reach adequate power on the
  primary metric at the platform's typical weekly view volume for these
  subcategories (~7,100 views/week per subcategory in this dataset) —
  in practice, run a power calculation off the current 11% baseline
  conversion and a minimum detectable effect (e.g., +2pts) before
  launching.
- **Success criteria:** Statistically significant lift in the primary
  metric with no statistically significant regression in any guardrail
  metric. If adoption is high but conversion doesn't move, that's a signal
  the bottleneck is something other than comparison friction (e.g., price
  or trust), which would redirect the next iteration.

## 9. Limitations & Honest Caveats

- All findings here come from **observational, synthetic data** — the
  choice-heavy vs low-choice conversion gap is a strong *correlation*, but
  only a real A/B test can confirm the comparison feature *causes* the
  lift.
- Discount and rating relationships are correlational; other unmeasured
  factors (brand trust, delivery time, product imagery quality) could
  explain part of the gap and aren't modeled here.
- The "choice-heavy" flag is defined by SKU count per subcategory as a
  simplification — a real platform would want to validate this definition
  against actual user research (e.g., session recordings, surveys) before
  fully committing engineering resources to the comparison feature.

## 10. Final Recommendation

Ship a scoped MVP of "Compare Products" for the six identified
choice-heavy subcategories, validate with the A/B test above before a
platform-wide rollout, and use the adoption + comparison-to-purchase
metrics to decide whether to extend the feature (e.g., AI-assisted
recommendations, cross-subcategory comparison) in a later iteration.
