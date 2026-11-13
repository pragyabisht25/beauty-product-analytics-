# Power BI Dashboard Design

**Data source:** MySQL `beauty_analytics` DB (via `sql/01_schema.sql`) or the
CSVs in `data/` and `data/derived/`. Import mode is fine at this data size.

## Data Model

Star-ish schema:
- `customers` (dimension)
- `products` (dimension)
- `orders` → `order_items` (fact, revenue grain)
- `user_events` (fact, behavioural grain — one row per event)

Relationships:
- `orders[customer_id]` → `customers[customer_id]` (many-to-one)
- `order_items[order_id]` → `orders[order_id]` (many-to-one)
- `order_items[product_id]` → `products[product_id]` (many-to-one)
- `user_events[customer_id]` → `customers[customer_id]` (many-to-one)
- `user_events[product_id]` → `products[product_id]` (many-to-one)

Add a `Date` calculated table (from `order_date` / event date) for
time-intelligence measures if trending by month is wanted.

## Core DAX Measures

```
Revenue = SUM(order_items[selling_price] * order_items[quantity])
Orders = DISTINCTCOUNT(orders[order_id])
Customers = DISTINCTCOUNT(orders[customer_id])
AOV = DIVIDE([Revenue], [Orders])

Views = CALCULATE(COUNTROWS(user_events), user_events[event_type] = "product_view")
Wishlists = CALCULATE(COUNTROWS(user_events), user_events[event_type] = "wishlist")
Carts = CALCULATE(COUNTROWS(user_events), user_events[event_type] = "add_to_cart")
Purchases = CALCULATE(COUNTROWS(user_events), user_events[event_type] = "purchase")

View to Cart Rate = DIVIDE([Carts], [Views])
Cart to Purchase Rate = DIVIDE([Purchases], [Carts])
View to Purchase Rate = DIVIDE([Purchases], [Views])

Conversion Rate = DIVIDE([Orders], [Views])   -- overall site conversion proxy
```

---

## Page 1 — Business Overview

**Purpose:** Executive snapshot of platform health.

- KPI cards: Revenue, Orders, Customers, AOV, Overall Conversion Rate
- Line chart: Revenue by month (if using order_date trend)
- Bar chart: Revenue by category
- Donut chart: New vs Returning customer share
- Table: Top 10 products by revenue

## Page 2 — Customer Behaviour

**Purpose:** Who's buying, and how they behave.

- Bar chart: Revenue & orders by age group
- Bar chart: Orders by city
- Donut: New vs Returning customers
- Bar chart: Views by category vs Purchases by category (side-by-side, to
  visualize the browsing-vs-buying gap)
- Table: Top 10% high-value customers (spend, order count)
- KPI card: Top-10%-customer revenue share

## Page 3 — Product Performance

**Purpose:** Funnel health at the product/subcategory level.

- Funnel visual: Search → View → Wishlist → Cart → Purchase (overall)
- Table: Product-level funnel (views, wishlist, cart, purchase, all three
  conversion rates) — sortable/filterable by category, subcategory, brand
- Scatter chart: Views (x) vs View→Purchase Rate (y), bubble size = review
  count — visually isolates high-view/low-conversion products (bottom-right
  cluster) and high-rated/low-sales products
- Slicers: category, subcategory, rating band, discount band

## Page 4 — Product Opportunity

**Purpose:** The page that carries the story of this project — where is
the platform leaking conversion, and why.

- Bar chart: View→Purchase conversion by subcategory, sorted ascending,
  color-coded by `choice_heavy_subcategory` flag — this is the single
  visual that makes the case for the "Compare Products" feature
- KPI cards: Choice-heavy view→purchase rate (11%) vs Low-choice
  view→purchase rate (20%)
- Table: High-view/low-conversion product list (candidates for
  merchandising or comparison-feature prioritization)
- Table: High-rated (4.3+) but low-sales products
- Callout text box: one-line problem statement + link/reference to the
  full case study (`docs/case_study.md`)

## Suggested Theme

Soft rose/mauve palette to match the beauty category context
(`#B76E79`, `#7A5C61`, `#F4E7E9`, neutral greys for backgrounds) — avoid
default Power BI blue/yellow so it doesn't read as a generic sales
dashboard.

## Note on Delivery

This repo ships the data model, DAX measures, and page-by-page layout
spec above so the dashboard can be rebuilt quickly in Power BI Desktop
(File → Get Data → CSV/MySQL, then follow this spec). A `.pbix` binary
isn't included since it can't be authored outside Power BI Desktop itself
— import `data/*.csv` (or connect to the MySQL DB), paste in the DAX
measures, and build the four pages as specified.
