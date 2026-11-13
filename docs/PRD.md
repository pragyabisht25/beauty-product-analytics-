# PRD — "Compare Products" (Beauty Product Comparison Tool)

**Product:** Beauty & Cosmetics E-commerce Platform (Nykaa-style)
**Author:** Product Analyst / APM candidate
**Status:** Draft for review
**Related analysis:** `docs/case_study.md`, `data/derived/subcategory_funnel.csv`

---

## 1. Problem Statement

Shoppers browsing **choice-heavy subcategories** — those with 20+ near-identical
SKUs, such as Moisturizers, Face Serums, Foundation, Lipstick, and Shampoo —
view products at a similar or higher rate than shoppers in low-choice
subcategories, but convert at roughly **half the rate**:

- Choice-heavy subcategories: **11% view→purchase conversion**
- Low-choice subcategories: **20% view→purchase conversion**
- Choice-heavy view→cart drop-off is **75%**, vs **63%** for low-choice
  subcategories

Wishlist activity is also high in these subcategories, which suggests
shoppers *are* interested and *are* shortlisting products — they are
comparing mentally across browser tabs / product pages, but the platform
gives them no side-by-side way to do this. The likely result: decision
fatigue, repeated back-and-forth between similar product pages, and
abandonment before add-to-cart or before final purchase.

This is a **discovery-to-decision problem**, not a discovery-to-awareness
problem — users are finding the products, they're just not confidently
picking one.

## 2. Target Users

- Shoppers actively browsing within a single subcategory that has many
  similar SKUs (e.g., comparing 4-5 moisturizers or foundations before
  deciding).
- New and price/ingredient-conscious shoppers who lack brand familiarity
  and rely on browsing many options.
- Secondary: returning shoppers restocking a category who want to check if
  a similar-but-cheaper or better-rated alternative exists.

## 3. User Story

> As a beauty shopper comparing several similar products, I want to see
> their price, discount, rating, reviews, and key attributes side by side,
> so that I can confidently pick the right one without opening and
> re-opening multiple product pages.

## 4. Goals

- Reduce the decision friction that causes high view→cart and cart→purchase
  drop-off specifically in choice-heavy subcategories.
- Increase view→purchase conversion in choice-heavy subcategories, closing
  some of the gap versus low-choice subcategories.
- Give users a reason to add multiple shortlisted items to a single
  comparison view instead of tab-switching or abandoning.
- Surface objective differentiators (price, discount, rating, reviews) so
  users don't have to manually reconcile scattered information.

## 5. Non-Goals (out of scope for MVP)

- Comparing products **across** subcategories (e.g., a serum vs a
  moisturizer) — comparison only makes sense within a subcategory.
- AI-generated "which one is right for you" recommendations — that's a v2
  personalization feature, not MVP.
- Comparing more than 3 products at once (keeps the UI readable on mobile).
- Ingredient-level allergen/skin-type filtering logic — MVP will surface
  listed ingredients as text, not a matching algorithm.
- Comparison of user-generated review *content* (only aggregate rating and
  review count are shown in MVP).

## 6. MVP Feature Scope

1. **"Add to Compare" action** on product cards in listing/search pages and
   on the product detail page (max 3 products at a time, same subcategory).
2. **Compare tray**: a persistent small bar showing selected items with a
   "Compare Now" CTA once 2+ items are selected.
3. **Comparison screen** showing, side by side:
   - Product image, name, brand
   - Price and discount (and effective price after discount)
   - Rating and review count
   - Key listed attributes (e.g., skin type suitability, key benefits,
     volume/size) pulled from existing product data
   - "Add to Cart" button per product, directly from the comparison screen
4. **Entry points**: comparison tray accessible from category/subcategory
   listing pages (where choice-heavy browsing happens) and from the product
   detail page ("Compare with similar products" suggesting 2 same-subcategory
   alternatives).

## 7. User Flow

```
Search / Category Browse
        │
        ▼
Product Listing Page  ──(select 2-3 products)──▶  Compare Tray
        │                                              │
        ▼                                              ▼
  Product Detail Page ──(Compare with similar)──▶ Comparison Screen
                                                        │
                                                        ▼
                                                 Product Selection
                                                        │
                                                        ▼
                                                    Add to Cart
                                                        │
                                                        ▼
                                                     Purchase
```

## 8. Success Metrics

**Primary metric**
- View→purchase conversion rate in choice-heavy subcategories (target:
  close ~30-40% of the current 9-point gap vs low-choice subcategories
  within one quarter of full rollout).

**Secondary metrics**
- Feature adoption rate: % of sessions in choice-heavy subcategories that
  use "Add to Compare."
- Comparison-to-purchase conversion: % of comparison-screen sessions that
  result in an add-to-cart within the same session.
- Add-to-cart rate in choice-heavy subcategories (view→cart).
- Repeat usage: % of users who use Compare more than once across sessions.

**Guardrail metrics**
- Overall site conversion rate (should not regress due to added UI
  friction/latency).
- Product detail page engagement time (a large negative shift could signal
  users are comparing instead of reading full descriptions, losing
  information).
- Page load time / Core Web Vitals on listing pages (compare tray must not
  degrade performance).

## 9. Assumptions & Risks

- Assumes the drop-off is driven by decision difficulty, not by
  price/quality dissatisfaction — validated only by an A/B test, not by
  observational data alone (see `case_study.md` limitations section).
- Risk: users may use Compare but still not purchase if the underlying
  issue is price sensitivity rather than comparison friction — the A/B test
  is designed to detect this.
- Risk: low awareness of the new feature if entry points aren't prominent
  enough — mitigated by placing "Add to Compare" directly on listing page
  cards, where browsing already happens.
