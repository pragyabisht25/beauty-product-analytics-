# Resume-Ready Project Description

## Short version (1 line, for a resume bullet list)

**Beauty Product Growth & Recommendation Analytics** — End-to-end product
case study (Python, SQL, Power BI) analyzing 200K+ user events to identify
a 9-point conversion gap in choice-heavy product categories; scoped and
proposed a "Compare Products" MVP feature with PRD, success metrics, and
A/B test design.

## Medium version (2-3 bullets, for a resume project section)

**Beauty Product Growth & Recommendation Analytics** | Python, SQL (MySQL), Power BI
- Built and analyzed a synthetic e-commerce dataset (6,000 customers, 330
  products, ~200K behavioural events, ~16,000 orders) covering the full
  discovery-to-purchase funnel for a beauty & cosmetics platform.
- Identified that subcategories with 20+ similar SKUs convert at ~11%
  view→purchase vs ~20% in low-choice subcategories, despite comparable
  or higher engagement — traced the gap through pricing, discount, and
  rating analysis to rule out price/quality as primary drivers.
- Translated the insight into a scoped MVP ("Compare Products"), wrote a
  full PRD (problem, goals, non-goals, user flow, success metrics), and
  designed an A/B test with primary/secondary/guardrail metrics to
  validate impact before platform-wide rollout.
- Built SQL analysis queries (CTEs, window functions) and a 4-page Power
  BI dashboard design (Business Overview, Customer Behaviour, Product
  Performance, Product Opportunity) to communicate findings to
  stakeholders.

## Long version (for a portfolio page / LinkedIn "featured" write-up)

This project simulates the full workflow of an entry-level Product
Manager / Product Analyst at a beauty e-commerce company. Starting from a
generated but internally-consistent dataset spanning customers, products,
behavioural events (search, view, wishlist, cart, purchase, review), and
orders, I ran a structured analysis across five areas — customer
behaviour, product performance, pricing/discount effects, ratings/reviews,
and the product discovery funnel — using Python (Pandas/NumPy) and SQL
(MySQL, including CTEs and window functions).

Rather than stopping at dashboards, I used the analysis to identify one
concrete product problem: subcategories with a large number of similar
SKUs (e.g., moisturizers, foundations, shampoos) show significantly worse
view→purchase conversion than subcategories with fewer, more
differentiated products — even though engagement (views, wishlists) is
just as strong. I ruled out the two most obvious explanations (price and
rating) using correlation analysis before settling on "decision friction
from too many similar options" as the most likely driver.

From there, I worked through the standard PM toolkit: a problem statement
and opportunity framing, a scoped MVP ("Compare Products," letting users
compare up to 3 same-subcategory products side by side), a full PRD with
explicit non-goals, a user flow, primary/secondary/guardrail success
metrics, and an A/B test design with a clear hypothesis and success
criteria. I also designed a 4-page Power BI dashboard (including the DAX
measures) to make the findings explorable for stakeholders, and wrote up
the full narrative as a case study: Problem → Evidence → Insight →
Opportunity → Solution → MVP → Metrics → Experiment.

**Tech stack:** Python (Pandas, NumPy, Matplotlib), SQL (MySQL), Power BI,
Excel/CSV.

**Skills demonstrated:** product thinking, data-driven problem
identification, correlation vs. causation reasoning, PRD writing, MVP
scoping, success-metric design, A/B test design, SQL analytics, and
stakeholder-ready reporting.
