"""
02_analysis.py
Runs the full product-analytics pass over the synthetic data and:
  1. Prints key numbers to stdout (captured into docs/analysis_output.txt)
  2. Saves supporting charts into ../charts/
  3. Saves a few summary tables into ../data/derived/ for Power BI / Excel

Sections mirror the brief:
  1. Customer behaviour
  2. Product performance
  3. Pricing & discount analysis
  4. Reviews & ratings
  5. Product discovery funnel
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

DATA = "../data"
CHARTS = "../charts"
DERIVED = "../data/derived"
import os
os.makedirs(DERIVED, exist_ok=True)

customers = pd.read_csv(f"{DATA}/customers.csv")
products = pd.read_csv(f"{DATA}/products.csv")
events = pd.read_csv(f"{DATA}/user_events.csv")
orders = pd.read_csv(f"{DATA}/orders.csv")
order_items = pd.read_csv(f"{DATA}/order_items.csv")

events["timestamp"] = pd.to_datetime(events["timestamp"])
orders["order_date"] = pd.to_datetime(orders["order_date"])

print("=" * 70)
print("1. CUSTOMER BEHAVIOUR")
print("=" * 70)

seg = customers["new_or_returning"].value_counts()
print("\nNew vs Returning customers:")
print(seg)
print(f"Returning-customer share: {seg.get('Returning',0) / seg.sum():.1%}")

age_orders = orders.merge(customers[["customer_id", "age_group"]], on="customer_id")
age_summary = age_orders.groupby("age_group")["total_amount"].agg(["count", "sum", "mean"]).round(1)
age_summary.columns = ["orders", "revenue", "avg_order_value"]
age_summary = age_summary.sort_values("revenue", ascending=False)
print("\nRevenue & orders by age group:")
print(age_summary)

view_events = events[events.event_type == "product_view"].merge(
    products[["product_id", "category"]], on="product_id", how="left")
most_viewed_cat = view_events["category"].value_counts()
print("\nMost-viewed categories:")
print(most_viewed_cat)

purchase_events = events[events.event_type == "purchase"].merge(
    products[["product_id", "category"]], on="product_id", how="left")
most_purchased_cat = purchase_events["category"].value_counts()
print("\nMost-purchased categories:")
print(most_purchased_cat)

# high value customers (top 10% by total spend)
cust_spend = orders.groupby("customer_id")["total_amount"].sum().sort_values(ascending=False)
top10_cutoff = cust_spend.quantile(0.90)
top10_customers = cust_spend[cust_spend >= top10_cutoff]
top10_share_of_revenue = top10_customers.sum() / cust_spend.sum()
print(f"\nTop 10% customers by spend contribute {top10_share_of_revenue:.1%} of total revenue")
print(f"(min spend to be in top 10%: Rs {top10_cutoff:,.0f})")

customers.to_csv  # noop, keep import used
cust_spend.rename("total_spend").reset_index().to_csv(f"{DERIVED}/customer_spend.csv", index=False)

fig, ax = plt.subplots(figsize=(7, 4.5))
most_viewed_cat.sort_values().plot(kind="barh", ax=ax, color="#B76E79")
ax.set_title("Product Views by Category")
ax.set_xlabel("Views")
plt.tight_layout()
plt.savefig(f"{CHARTS}/01_views_by_category.png", dpi=150)
plt.close()

print("\n" + "=" * 70)
print("2. PRODUCT PERFORMANCE")
print("=" * 70)

funnel = events.pivot_table(index="product_id", columns="event_type",
                             values="event_id", aggfunc="count", fill_value=0)
for col in ["search", "product_view", "wishlist", "add_to_cart", "purchase", "review"]:
    if col not in funnel.columns:
        funnel[col] = 0

funnel = funnel.merge(products, left_index=True, right_on="product_id")
funnel["view_to_cart_rate"] = np.where(funnel.product_view > 0, funnel.add_to_cart / funnel.product_view, 0)
funnel["cart_to_purchase_rate"] = np.where(funnel.add_to_cart > 0, funnel.purchase / funnel.add_to_cart, 0)
funnel["view_to_purchase_rate"] = np.where(funnel.product_view > 0, funnel.purchase / funnel.product_view, 0)
funnel["wishlist_to_purchase_rate"] = np.where(funnel.wishlist > 0, funnel.purchase / funnel.wishlist, 0)

funnel.to_csv(f"{DERIVED}/product_funnel.csv", index=False)

MIN_VIEWS = 25
eligible = funnel[funnel.product_view >= MIN_VIEWS].copy()

high_view_low_conv = eligible.sort_values(
    ["product_view", "view_to_purchase_rate"], ascending=[False, True]
).query("view_to_purchase_rate < view_to_purchase_rate.median()").head(15)
print(f"\nHigh-view / low-conversion products (views >= {MIN_VIEWS}), sample of 15:")
print(high_view_low_conv[["product_id", "category", "subcategory", "product_view",
                           "purchase", "view_to_purchase_rate"]].to_string(index=False))

high_rated_low_sales = eligible[(eligible.rating >= 4.3) & (eligible.purchase <= eligible.purchase.median())]
print(f"\nHigh-rated (>=4.3) but low-sales products: {len(high_rated_low_sales)} of {len(eligible)} eligible")

high_wishlist_low_purchase = eligible[eligible.wishlist >= eligible.wishlist.quantile(0.75)]
high_wishlist_low_purchase = high_wishlist_low_purchase[
    high_wishlist_low_purchase.wishlist_to_purchase_rate <= high_wishlist_low_purchase.wishlist_to_purchase_rate.median()]
print(f"High-wishlist but low wishlist->purchase products: {len(high_wishlist_low_purchase)}")

# THE CORE COMPARISON: choice-heavy vs non-choice-heavy subcategories
choice_summary = eligible.groupby("choice_heavy_subcategory").agg(
    products=("product_id", "count"),
    avg_views=("product_view", "mean"),
    avg_wishlist=("wishlist", "mean"),
    view_to_cart_rate=("add_to_cart", "sum"),
    total_views=("product_view", "sum"),
    total_purchases=("purchase", "sum"),
)
choice_summary["view_to_purchase_rate"] = choice_summary.total_purchases / choice_summary.total_views
choice_summary.index = choice_summary.index.map({True: "Choice-heavy subcategory (20+ SKUs)",
                                                    False: "Low-choice subcategory (<20 SKUs)"})
print("\n*** KEY FINDING: Choice-heavy vs low-choice subcategories ***")
print(choice_summary[["products", "avg_views", "avg_wishlist", "view_to_purchase_rate"]])

fig, ax = plt.subplots(figsize=(6.5, 4.5))
choice_summary["view_to_purchase_rate"].plot(kind="bar", ax=ax, color=["#B76E79", "#7A5C61"])
ax.set_ylabel("View -> Purchase conversion rate")
ax.set_title("Conversion Rate: Choice-Heavy vs Low-Choice Subcategories")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(f"{CHARTS}/02_choice_heavy_conversion.png", dpi=150)
plt.close()

# subcategory-level funnel table (used heavily in the case study / Power BI)
subcat_funnel = funnel.groupby("subcategory").agg(
    products=("product_id", "count"),
    views=("product_view", "sum"),
    wishlists=("wishlist", "sum"),
    carts=("add_to_cart", "sum"),
    purchases=("purchase", "sum"),
    choice_heavy=("choice_heavy_subcategory", "max"),
).reset_index()
subcat_funnel["view_to_cart_rate"] = subcat_funnel.carts / subcat_funnel.views
subcat_funnel["cart_to_purchase_rate"] = subcat_funnel.purchases / subcat_funnel.carts
subcat_funnel["view_to_purchase_rate"] = subcat_funnel.purchases / subcat_funnel.views
subcat_funnel = subcat_funnel.sort_values("view_to_purchase_rate")
subcat_funnel.to_csv(f"{DERIVED}/subcategory_funnel.csv", index=False)
print("\nSubcategory funnel (worst 8 by view->purchase conversion):")
print(subcat_funnel.head(8)[["subcategory", "products", "choice_heavy", "views",
                              "view_to_cart_rate", "cart_to_purchase_rate", "view_to_purchase_rate"]]
      .to_string(index=False))

print("\n" + "=" * 70)
print("3. PRICING & DISCOUNT ANALYSIS")
print("=" * 70)

funnel["discount_band"] = pd.cut(funnel.discount_pct, bins=[-1, 0, 10, 20, 30, 100],
                                  labels=["0%", "1-10%", "11-20%", "21-30%", "30%+"])
discount_summary = funnel.groupby("discount_band", observed=True).agg(
    products=("product_id", "count"),
    avg_view_to_cart=("view_to_cart_rate", "mean"),
    avg_cart_to_purchase=("cart_to_purchase_rate", "mean"),
    avg_view_to_purchase=("view_to_purchase_rate", "mean"),
)
print("\nConversion by discount band:")
print(discount_summary)

corr_discount_cart = funnel[["discount_pct", "view_to_cart_rate"]].corr().iloc[0, 1]
corr_discount_purchase = funnel[["discount_pct", "view_to_purchase_rate"]].corr().iloc[0, 1]
print(f"\nCorrelation(discount%, view->cart rate)   = {corr_discount_cart:.2f}")
print(f"Correlation(discount%, view->purchase rate) = {corr_discount_purchase:.2f}")
print("Interpretation: discount is more strongly associated with ADD-TO-CART than with")
print("final PURCHASE. This is a correlation, not a causal claim - price-sensitive shoppers")
print("may self-select into high-discount items regardless of the discount's causal effect,")
print("and we have not run a controlled experiment here.")

price_bins = pd.qcut(funnel.price, q=5, duplicates="drop")
price_conv = funnel.groupby(price_bins, observed=True)["view_to_purchase_rate"].mean()
print("\nView->purchase conversion by price quintile:")
print(price_conv)

fig, ax = plt.subplots(figsize=(6.5, 4.5))
discount_summary["avg_view_to_cart"].plot(ax=ax, marker="o", label="View -> Cart")
discount_summary["avg_view_to_purchase"].plot(ax=ax, marker="o", label="View -> Purchase")
ax.set_title("Conversion vs Discount Band")
ax.set_ylabel("Conversion rate")
ax.legend()
plt.tight_layout()
plt.savefig(f"{CHARTS}/03_discount_vs_conversion.png", dpi=150)
plt.close()

print("\n" + "=" * 70)
print("4. REVIEWS & RATINGS")
print("=" * 70)

rating_bins = pd.cut(funnel.rating, bins=[2.4, 3.5, 4.0, 4.5, 5.0])
rating_summary = funnel.groupby(rating_bins, observed=True).agg(
    products=("product_id", "count"),
    avg_view_to_purchase=("view_to_purchase_rate", "mean"),
    avg_review_count=("review_count", "mean"),
)
print("\nConversion by rating band:")
print(rating_summary)

corr_reviewcount_views = funnel[["review_count", "product_view"]].corr().iloc[0, 1]
print(f"\nCorrelation(review_count, product_view) = {corr_reviewcount_views:.2f}")

high_rating_low_conv = funnel[(funnel.rating >= 4.3) &
                               (funnel.view_to_purchase_rate < funnel.view_to_purchase_rate.median()) &
                               (funnel.product_view >= MIN_VIEWS)]
print(f"\nHigh-rated (>=4.3) but below-median conversion products: {len(high_rating_low_conv)}")

print("\n" + "=" * 70)
print("5. PRODUCT DISCOVERY FUNNEL (overall)")
print("=" * 70)

overall_funnel = {
    "search": (events.event_type == "search").sum(),
    "product_view": (events.event_type == "product_view").sum(),
    "wishlist": (events.event_type == "wishlist").sum(),
    "add_to_cart": (events.event_type == "add_to_cart").sum(),
    "purchase": (events.event_type == "purchase").sum(),
}
of = pd.Series(overall_funnel)
print(of)
print(f"\nOverall view -> cart rate:      {of.add_to_cart / of.product_view:.1%}")
print(f"Overall cart -> purchase rate:  {of.purchase / of.add_to_cart:.1%}")
print(f"Overall view -> purchase rate:  {of.purchase / of.product_view:.1%}")

fig, ax = plt.subplots(figsize=(6.5, 4.5))
of.reindex(["search", "product_view", "wishlist", "add_to_cart", "purchase"]).plot(
    kind="bar", ax=ax, color="#B76E79")
ax.set_title("Overall Discovery-to-Purchase Funnel")
ax.set_ylabel("Event count")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(f"{CHARTS}/04_overall_funnel.png", dpi=150)
plt.close()

# where users struggle most: compare drop-off rate at each stage, choice-heavy vs not
dropoff = funnel.groupby("choice_heavy_subcategory").agg(
    views=("product_view", "sum"), carts=("add_to_cart", "sum"), purchases=("purchase", "sum"))
dropoff["view_to_cart_dropoff"] = 1 - dropoff.carts / dropoff.views
dropoff["cart_to_purchase_dropoff"] = 1 - dropoff.purchases / dropoff.carts
dropoff.index = dropoff.index.map({True: "Choice-heavy", False: "Low-choice"})
print("\nDrop-off comparison:")
print(dropoff[["view_to_cart_dropoff", "cart_to_purchase_dropoff"]])

print("\nAll charts saved to ../charts/  |  Derived tables saved to ../data/derived/")
