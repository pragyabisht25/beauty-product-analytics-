# Beauty Product Growth & Recommendation Analytics

An end-to-end **Product Management + Product Analytics case study** for a
beauty & cosmetics e-commerce platform (Nykaa-style), built as an
APM / Product Analyst / Product Ops portfolio project.

This is **not a dashboard project**. It's a full product-thinking
exercise: `User Problem → Data Analysis → Product Insight → Product
Opportunity → Feature Proposal → MVP → Success Metrics → Measurement`.

**→ Start here: [`docs/case_study.md`](docs/case_study.md)** — the full
narrative, with the actual finding and the product decision it drove.

---

## The One-Line Finding

Subcategories with 20+ similar products (Moisturizer, Face Serum,
Foundation, Lipstick, Shampoo, Sunscreen) convert **~11%** view→purchase
vs **~20%** for subcategories with fewer, more differentiated options —
despite equal or higher browsing/wishlist activity. This shaped a scoped
MVP: a **"Compare Products"** feature, validated by A/B test design before
platform-wide rollout.

## Project Structure

```
beauty-product-analytics/
├── README.md                      <- you are here
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── user_events.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── derived/                   <- analysis output tables (funnel, spend, etc.)
├── scripts/
│   ├── 01_generate_data.py        <- synthetic data generation
│   └── 02_analysis.py             <- full analysis (5 sections) + chart export
├── charts/                        <- PNG charts from the analysis
├── sql/
│   ├── 01_schema.sql              <- MySQL DDL + LOAD DATA templates
│   └── 02_analysis_queries.sql    <- all analysis queries (CTEs, window fns)
├── powerbi/
│   └── dashboard_design.md        <- 4-page dashboard spec + DAX measures
└── docs/
    ├── case_study.md              <- ⭐ the main deliverable
    ├── PRD.md                     <- full Product Requirements Document
    ├── analysis_output.txt        <- raw console output from 02_analysis.py
    ├── interview_qna.md           <- 10 APM/Analyst interview Q&A
    └── resume_description.md      <- resume bullets + long-form write-up
```

## How to Reproduce

```bash
cd scripts
python3 01_generate_data.py     # writes CSVs to ../data
python3 02_analysis.py          # runs analysis, writes charts + derived tables
```

For SQL: create the schema with `sql/01_schema.sql`, load the CSVs from
`data/` (templates included in the schema file), then run
`sql/02_analysis_queries.sql`.

For Power BI: follow `powerbi/dashboard_design.md` — import the CSVs (or
connect to MySQL), add the listed DAX measures, and build the four pages.

## Dataset Summary

| Table | Rows | Notes |
|---|---|---|
| customers | 6,000 | age group, gender, city, new/returning, signup date |
| products | 330 | 5 categories, 19 subcategories, price/discount/rating/reviews |
| user_events | ~200,000 | search, product_view, wishlist, add_to_cart, purchase, review |
| orders | ~16,250 | order-level totals |
| order_items | ~16,250 | line-item detail (quantity, selling price) |

The data is synthetic but **not random** — funnel conversion rates,
discount effects, and rating effects are deliberately modeled with
realistic (and realistically imperfect) relationships so the analysis has
something genuine to find, rather than a pre-baked "correct answer."

## Analysis Covered

1. **Customer behaviour** — segments, high-value customers, browsing vs.
   purchasing patterns, repeat purchase mix
2. **Product performance** — funnel per product/subcategory, high-view/
   low-conversion products, high-rated/low-sales products
3. **Pricing & discount** — discount-band conversion, price quintiles,
   explicit correlation-vs-causation discussion
4. **Reviews & ratings** — rating-band conversion, review count vs.
   engagement
5. **Product discovery funnel** — overall funnel, and where choice-heavy
   vs. low-choice subcategories diverge

Full numbers: [`docs/analysis_output.txt`](docs/analysis_output.txt)

## Product Deliverables

- **Case study:** [`docs/case_study.md`](docs/case_study.md)
- **PRD:** [`docs/PRD.md`](docs/PRD.md)
- **A/B test design:** included in the case study, section 8
- **Interview prep:** [`docs/interview_qna.md`](docs/interview_qna.md)

## Tech Stack

Python (Pandas, NumPy, Matplotlib) · SQL (MySQL, CTEs & window functions)
· Power BI (design spec + DAX) · Excel/CSV

## Limitations

This project uses synthetic data with intentionally embedded patterns —
it demonstrates the *analysis-to-product-decision workflow*, not a claim
about real Nykaa/beauty-platform user behaviour. See
[`docs/case_study.md`](docs/case_study.md#9-limitations--honest-caveats)
for the full discussion of what would need to change with real production
data.
