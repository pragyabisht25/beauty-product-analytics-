"""
01_generate_data.py
Generates realistic, internally-consistent synthetic data for the
Beauty Product Growth & Recommendation Analytics project.

Design intent (baked into the data on purpose, so the later analysis
has something real to discover):
  - Subcategories with MANY similar products (choice-heavy) show
    strong search/view/wishlist activity but a WEAKER view->cart and
    cart->purchase conversion than subcategories with few products.
    This is the seed for the "users struggle to compare similar
    products" problem statement.
  - Discount increases add-to-cart rate but has a much weaker effect
    on final purchase (to support "don't assume discount = more
    sales" analysis).
  - Rating has a positive but non-linear relationship with purchase.
  - A meaningful share of highly-viewed, highly-wishlisted products
    have low purchase conversion (the "high engagement, low
    conversion" product list).

Output CSVs land in ../data/
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(42)

OUT = "../data"

# ---------------------------------------------------------------
# 1. PRODUCTS
# ---------------------------------------------------------------
categories = {
    "Skincare":      ["Moisturizer", "Face Serum", "Sunscreen", "Cleanser", "Face Mask"],
    "Makeup":        ["Lipstick", "Foundation", "Mascara", "Eyeliner", "Blush"],
    "Haircare":      ["Shampoo", "Conditioner", "Hair Oil", "Hair Serum"],
    "Fragrance":     ["Perfume", "Deodorant Spray"],
    "Personal Care": ["Body Wash", "Body Lotion", "Hand Cream"],
}

# How many products to generate per subcategory (deliberately uneven ->
# some subcategories are "choice-heavy" with many near-identical SKUs)
subcat_product_count = {
    "Moisturizer": 28, "Face Serum": 30, "Sunscreen": 22, "Cleanser": 18, "Face Mask": 14,
    "Lipstick": 32, "Foundation": 26, "Mascara": 16, "Eyeliner": 14, "Blush": 12,
    "Shampoo": 20, "Conditioner": 16, "Hair Oil": 12, "Hair Serum": 10,
    "Perfume": 18, "Deodorant Spray": 10,
    "Body Wash": 12, "Body Lotion": 12, "Hand Cream": 8,
}

brands = [
    "GlowLab", "PureSkin", "Nourie", "Bloomora", "Verve Cosmetics", "Rooted",
    "CityGlow", "Dermistry", "Petal & Co", "Suvida", "Aroma House", "Skinly",
    "Radiance Rx", "Curl & Co", "Barefaced", "Lumina", "Herbivore Naturals",
    "Nykaa Naturals", "Plum", "Mamaearth", "Minimalist", "The Face Lab",
]

products = []
product_id = 1000
for category, subcats in categories.items():
    for subcat in subcats:
        n = subcat_product_count[subcat]
        # choice-heavy subcategory flag: many similar options for shoppers to sift through
        choice_heavy = n >= 20
        for _ in range(n):
            base_price = {
                "Moisturizer": 550, "Face Serum": 750, "Sunscreen": 450, "Cleanser": 350, "Face Mask": 300,
                "Lipstick": 450, "Foundation": 650, "Mascara": 400, "Eyeliner": 300, "Blush": 500,
                "Shampoo": 350, "Conditioner": 380, "Hair Oil": 300, "Hair Serum": 600,
                "Perfume": 1400, "Deodorant Spray": 250,
                "Body Wash": 300, "Body Lotion": 350, "Hand Cream": 250,
            }[subcat]
            price = max(99, round(rng.normal(base_price, base_price * 0.28), -1))
            discount_pct = int(np.clip(rng.exponential(15), 0, 70))
            rating = round(np.clip(rng.normal(4.1, 0.5), 2.5, 5.0), 1)
            review_count = int(max(0, rng.gamma(2.0, 60)))
            products.append({
                "product_id": product_id,
                "category": category,
                "subcategory": subcat,
                "brand": rng.choice(brands),
                "price": int(price),
                "discount_pct": discount_pct,
                "rating": rating,
                "review_count": review_count,
                "choice_heavy_subcategory": choice_heavy,
            })
            product_id += 1

products_df = pd.DataFrame(products)
products_df.to_csv(f"{OUT}/products.csv", index=False)
print(f"Products generated: {len(products_df)}")

# ---------------------------------------------------------------
# 2. CUSTOMERS
# ---------------------------------------------------------------
N_CUSTOMERS = 6000
cities = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Pune", "Chennai",
          "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"]
age_groups = ["18-24", "25-34", "35-44", "45-54"]
age_weights = [0.32, 0.38, 0.20, 0.10]

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
signup_days = (end_date - start_date).days

customers = []
for cid in range(1, N_CUSTOMERS + 1):
    signup_date = start_date + timedelta(days=int(rng.integers(0, signup_days)))
    customers.append({
        "customer_id": cid,
        "age_group": rng.choice(age_groups, p=age_weights),
        "gender": rng.choice(["Female", "Male", "Prefer not to say"], p=[0.78, 0.19, 0.03]),
        "city": rng.choice(cities),
        "signup_date": signup_date.date().isoformat(),
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv(f"{OUT}/customers.csv", index=False)
print(f"Customers generated: {len(customers_df)}")

# ---------------------------------------------------------------
# 3. EVENTS (search -> product_view -> wishlist / add_to_cart -> purchase -> review)
# ---------------------------------------------------------------
# Each customer gets a random number of "sessions"; each session browses
# within 1-2 categories and generates a funnel of events.

event_rows = []
event_id = 1
order_rows = []
order_item_rows = []
order_id = 5000

products_by_subcat = products_df.groupby("subcategory")

def pick_products(subcat, n):
    pool = products_by_subcat.get_group(subcat)
    n = min(n, len(pool))
    return pool.sample(n=n, random_state=int(rng.integers(0, 1_000_000)))

session_days_span = (end_date - start_date).days

for _, cust in customers_df.iterrows():
    cust_signup = datetime.fromisoformat(cust["signup_date"])
    n_sessions = int(max(1, rng.poisson(4)))
    cust_orders = 0
    for s in range(n_sessions):
        days_after_signup = int(rng.integers(0, max(1, (end_date - cust_signup).days) or 1))
        session_date = cust_signup + timedelta(days=days_after_signup)
        subcat = rng.choice(list(subcat_product_count.keys()))
        pool = products_by_subcat.get_group(subcat)
        choice_heavy = bool(pool["choice_heavy_subcategory"].iloc[0])

        # number of products viewed in this session - choice-heavy subcats get browsed more widely
        n_viewed = int(rng.integers(3, 9)) if choice_heavy else int(rng.integers(2, 6))
        n_viewed = min(n_viewed, len(pool))
        viewed_products = pool.sample(n=n_viewed, random_state=int(rng.integers(0, 1_000_000)))

        # 1 search event kicks off the session
        event_rows.append({
            "event_id": event_id, "customer_id": cust["customer_id"], "product_id": None,
            "event_type": "search", "subcategory": subcat,
            "timestamp": (session_date).isoformat(timespec="seconds"),
        })
        event_id += 1

        for _, prod in viewed_products.iterrows():
            view_ts = session_date + timedelta(minutes=int(rng.integers(1, 45)))
            event_rows.append({
                "event_id": event_id, "customer_id": cust["customer_id"], "product_id": prod["product_id"],
                "event_type": "product_view", "subcategory": subcat, "timestamp": view_ts.isoformat(timespec="seconds"),
            })
            event_id += 1

            # base propensities
            wishlist_p = 0.22
            cart_p = 0.30 if not choice_heavy else 0.19   # choice-heavy => lower view->cart
            # discount lifts cart propensity
            cart_p += min(0.15, prod["discount_pct"] / 300)
            # rating lifts cart propensity mildly
            cart_p += max(0, (prod["rating"] - 4.0)) * 0.05

            if rng.random() < wishlist_p:
                wl_ts = view_ts + timedelta(minutes=int(rng.integers(1, 10)))
                event_rows.append({
                    "event_id": event_id, "customer_id": cust["customer_id"], "product_id": prod["product_id"],
                    "event_type": "wishlist", "subcategory": subcat, "timestamp": wl_ts.isoformat(timespec="seconds"),
                })
                event_id += 1

            if rng.random() < cart_p:
                cart_ts = view_ts + timedelta(minutes=int(rng.integers(2, 20)))
                event_rows.append({
                    "event_id": event_id, "customer_id": cust["customer_id"], "product_id": prod["product_id"],
                    "event_type": "add_to_cart", "subcategory": subcat, "timestamp": cart_ts.isoformat(timespec="seconds"),
                })
                event_id += 1

                # cart -> purchase conversion: choice-heavy subcats also convert
                # slightly worse from cart (decision paralysis persists), discount helps more here
                purchase_p = 0.46 if not choice_heavy else 0.37
                purchase_p += min(0.20, prod["discount_pct"] / 200)

                if rng.random() < purchase_p:
                    purchase_ts = cart_ts + timedelta(minutes=int(rng.integers(2, 30)))
                    event_rows.append({
                        "event_id": event_id, "customer_id": cust["customer_id"], "product_id": prod["product_id"],
                        "event_type": "purchase", "subcategory": subcat, "timestamp": purchase_ts.isoformat(timespec="seconds"),
                    })
                    event_id += 1

                    selling_price = round(prod["price"] * (1 - prod["discount_pct"] / 100), 2)
                    qty = int(rng.choice([1, 1, 1, 2], p=[0.7, 0.15, 0.1, 0.05])) if False else int(rng.choice([1, 2], p=[0.85, 0.15]))
                    order_item_rows.append({
                        "order_id": order_id, "product_id": prod["product_id"],
                        "quantity": qty, "selling_price": selling_price,
                    })
                    order_rows.append({
                        "order_id": order_id, "customer_id": cust["customer_id"],
                        "order_date": purchase_ts.date().isoformat(),
                        "total_amount": round(selling_price * qty, 2),
                    })
                    order_id += 1
                    cust_orders += 1

                    # occasional review after purchase
                    if rng.random() < 0.35:
                        rev_ts = purchase_ts + timedelta(days=int(rng.integers(2, 20)))
                        if rev_ts <= end_date:
                            event_rows.append({
                                "event_id": event_id, "customer_id": cust["customer_id"], "product_id": prod["product_id"],
                                "event_type": "review", "subcategory": subcat, "timestamp": rev_ts.isoformat(timespec="seconds"),
                            })
                            event_id += 1

events_df = pd.DataFrame(event_rows)
orders_df = pd.DataFrame(order_rows)
order_items_df = pd.DataFrame(order_item_rows)

# new_or_returning derived from order count (>=2 orders => returning)
order_counts = orders_df.groupby("customer_id").size().rename("order_count")
customers_df = customers_df.merge(order_counts, on="customer_id", how="left")
customers_df["order_count"] = customers_df["order_count"].fillna(0).astype(int)
customers_df["new_or_returning"] = np.where(customers_df["order_count"] >= 2, "Returning", "New")
customers_df.drop(columns=["order_count"]).to_csv(f"{OUT}/customers.csv", index=False)

events_df.to_csv(f"{OUT}/user_events.csv", index=False)
orders_df.to_csv(f"{OUT}/orders.csv", index=False)
order_items_df.to_csv(f"{OUT}/order_items.csv", index=False)

print(f"Events generated: {len(events_df):,}")
print(f"Orders generated: {len(orders_df):,}")
print(f"Order items generated: {len(order_items_df):,}")
print("All CSVs written to", OUT)
