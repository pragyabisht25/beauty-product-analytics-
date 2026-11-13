-- ============================================================
-- Beauty Product Growth & Recommendation Analytics
-- Analysis Queries (MySQL 8+, uses window functions / CTEs)
-- ============================================================
USE beauty_analytics;

-- ------------------------------------------------------------
-- 1. CUSTOMER BEHAVIOUR
-- ------------------------------------------------------------

-- 1.1 New vs returning customer split and revenue contribution
SELECT
    c.new_or_returning,
    COUNT(DISTINCT c.customer_id)              AS customers,
    COUNT(DISTINCT o.order_id)                 AS orders,
    ROUND(SUM(o.total_amount), 2)              AS revenue,
    ROUND(SUM(o.total_amount) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.new_or_returning;

-- 1.2 Revenue and orders by age group
SELECT
    c.age_group,
    COUNT(o.order_id)                AS orders,
    ROUND(SUM(o.total_amount), 2)    AS revenue,
    ROUND(AVG(o.total_amount), 2)    AS avg_order_value
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.age_group
ORDER BY revenue DESC;

-- 1.3 Most viewed vs most purchased categories (browsing vs buying gap)
SELECT
    p.category,
    SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END) AS views,
    SUM(CASE WHEN e.event_type = 'purchase'     THEN 1 ELSE 0 END) AS purchases,
    ROUND(SUM(CASE WHEN e.event_type = 'purchase' THEN 1 ELSE 0 END) /
          NULLIF(SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END), 0), 4) AS view_to_purchase_rate
FROM user_events e
JOIN products p ON p.product_id = e.product_id
GROUP BY p.category
ORDER BY views DESC;

-- 1.4 High-value customers: top 10% of spenders and their revenue share
WITH customer_spend AS (
    SELECT customer_id, SUM(total_amount) AS total_spend
    FROM orders
    GROUP BY customer_id
),
ranked AS (
    SELECT
        customer_id,
        total_spend,
        PERCENT_RANK() OVER (ORDER BY total_spend) AS pct_rank
    FROM customer_spend
)
SELECT
    SUM(CASE WHEN pct_rank >= 0.90 THEN total_spend ELSE 0 END) / SUM(total_spend) AS top10pct_revenue_share,
    COUNT(CASE WHEN pct_rank >= 0.90 THEN 1 END)                                    AS top10pct_customer_count
FROM ranked;

-- 1.5 Browsing vs purchasing ratio per customer (heavy browsers who rarely buy)
SELECT
    e.customer_id,
    SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END) AS views,
    SUM(CASE WHEN e.event_type = 'purchase'     THEN 1 ELSE 0 END) AS purchases
FROM user_events e
GROUP BY e.customer_id
HAVING views >= 10 AND purchases = 0
ORDER BY views DESC
LIMIT 50;


-- ------------------------------------------------------------
-- 2. PRODUCT PERFORMANCE
-- ------------------------------------------------------------

-- 2.1 Product-level funnel (views, wishlist, cart, purchase, conversion rates)
WITH funnel AS (
    SELECT
        p.product_id, p.category, p.subcategory, p.brand,
        p.price, p.discount_pct, p.rating, p.review_count, p.choice_heavy_subcategory,
        SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END) AS views,
        SUM(CASE WHEN e.event_type = 'wishlist'     THEN 1 ELSE 0 END) AS wishlists,
        SUM(CASE WHEN e.event_type = 'add_to_cart'  THEN 1 ELSE 0 END) AS carts,
        SUM(CASE WHEN e.event_type = 'purchase'     THEN 1 ELSE 0 END) AS purchases
    FROM products p
    LEFT JOIN user_events e ON e.product_id = p.product_id
    GROUP BY p.product_id, p.category, p.subcategory, p.brand,
             p.price, p.discount_pct, p.rating, p.review_count, p.choice_heavy_subcategory
)
SELECT *,
       ROUND(carts     / NULLIF(views, 0), 4)  AS view_to_cart_rate,
       ROUND(purchases / NULLIF(carts, 0), 4)  AS cart_to_purchase_rate,
       ROUND(purchases / NULLIF(views, 0), 4)  AS view_to_purchase_rate
FROM funnel;

-- 2.2 High-view / low-conversion products (candidates for "why aren't these converting?")
WITH funnel AS (
    SELECT
        p.product_id, p.category, p.subcategory,
        SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END) AS views,
        SUM(CASE WHEN e.event_type = 'purchase'     THEN 1 ELSE 0 END) AS purchases
    FROM products p
    JOIN user_events e ON e.product_id = p.product_id
    GROUP BY p.product_id, p.category, p.subcategory
    HAVING views >= 25
)
SELECT *,
       ROUND(purchases / views, 4) AS view_to_purchase_rate
FROM funnel
ORDER BY views DESC, view_to_purchase_rate ASC
LIMIT 20;

-- 2.3 High-rated but low-sales products
SELECT
    p.product_id, p.category, p.subcategory, p.rating, p.review_count,
    COUNT(CASE WHEN e.event_type = 'purchase' THEN 1 END) AS purchases
FROM products p
LEFT JOIN user_events e ON e.product_id = p.product_id
WHERE p.rating >= 4.3
GROUP BY p.product_id, p.category, p.subcategory, p.rating, p.review_count
HAVING purchases <= 20
ORDER BY p.rating DESC, purchases ASC
LIMIT 20;

-- 2.4 High-wishlist but low wishlist->purchase conversion
WITH w AS (
    SELECT
        p.product_id, p.category, p.subcategory,
        SUM(CASE WHEN e.event_type = 'wishlist' THEN 1 ELSE 0 END) AS wishlists,
        SUM(CASE WHEN e.event_type = 'purchase' THEN 1 ELSE 0 END) AS purchases
    FROM products p
    JOIN user_events e ON e.product_id = p.product_id
    GROUP BY p.product_id, p.category, p.subcategory
    HAVING wishlists >= 20
)
SELECT *, ROUND(purchases / wishlists, 4) AS wishlist_to_purchase_rate
FROM w
ORDER BY wishlist_to_purchase_rate ASC
LIMIT 20;

-- 2.5 *** KEY FINDING QUERY: choice-heavy vs low-choice subcategory conversion ***
SELECT
    p.choice_heavy_subcategory,
    COUNT(DISTINCT p.product_id) AS products,
    SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END) AS views,
    SUM(CASE WHEN e.event_type = 'purchase'     THEN 1 ELSE 0 END) AS purchases,
    ROUND(SUM(CASE WHEN e.event_type = 'purchase' THEN 1 ELSE 0 END) /
          SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END), 4) AS view_to_purchase_rate
FROM products p
JOIN user_events e ON e.product_id = p.product_id
GROUP BY p.choice_heavy_subcategory;

-- 2.6 Subcategory-level funnel ranked by worst conversion (drives the PRD problem statement)
SELECT
    p.subcategory,
    p.choice_heavy_subcategory,
    COUNT(DISTINCT p.product_id) AS products,
    SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END) AS views,
    SUM(CASE WHEN e.event_type = 'add_to_cart'  THEN 1 ELSE 0 END) AS carts,
    SUM(CASE WHEN e.event_type = 'purchase'     THEN 1 ELSE 0 END) AS purchases,
    ROUND(SUM(CASE WHEN e.event_type = 'purchase' THEN 1 ELSE 0 END) /
          SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END), 4) AS view_to_purchase_rate
FROM products p
JOIN user_events e ON e.product_id = p.product_id
GROUP BY p.subcategory, p.choice_heavy_subcategory
ORDER BY view_to_purchase_rate ASC;


-- ------------------------------------------------------------
-- 3. PRICING & DISCOUNT ANALYSIS
-- ------------------------------------------------------------

-- 3.1 Conversion by discount band
WITH funnel AS (
    SELECT
        p.product_id,
        CASE
            WHEN p.discount_pct = 0 THEN '0%'
            WHEN p.discount_pct BETWEEN 1  AND 10 THEN '1-10%'
            WHEN p.discount_pct BETWEEN 11 AND 20 THEN '11-20%'
            WHEN p.discount_pct BETWEEN 21 AND 30 THEN '21-30%'
            ELSE '30%+'
        END AS discount_band,
        SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END) AS views,
        SUM(CASE WHEN e.event_type = 'add_to_cart'  THEN 1 ELSE 0 END) AS carts,
        SUM(CASE WHEN e.event_type = 'purchase'     THEN 1 ELSE 0 END) AS purchases
    FROM products p
    JOIN user_events e ON e.product_id = p.product_id
    GROUP BY p.product_id, discount_band
)
SELECT
    discount_band,
    COUNT(*) AS products,
    ROUND(AVG(carts / NULLIF(views,0)), 4)     AS avg_view_to_cart_rate,
    ROUND(AVG(purchases / NULLIF(views,0)), 4) AS avg_view_to_purchase_rate
FROM funnel
GROUP BY discount_band
ORDER BY FIELD(discount_band, '0%', '1-10%', '11-20%', '21-30%', '30%+');

-- 3.2 Average discount by category
SELECT category, ROUND(AVG(discount_pct), 1) AS avg_discount_pct
FROM products
GROUP BY category
ORDER BY avg_discount_pct DESC;

-- 3.3 Price quintile vs conversion (NTILE window function)
WITH priced AS (
    SELECT product_id, price, NTILE(5) OVER (ORDER BY price) AS price_quintile
    FROM products
),
funnel AS (
    SELECT
        pr.price_quintile,
        SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END) AS views,
        SUM(CASE WHEN e.event_type = 'purchase'     THEN 1 ELSE 0 END) AS purchases
    FROM priced pr
    JOIN user_events e ON e.product_id = pr.product_id
    GROUP BY pr.price_quintile
)
SELECT price_quintile, views, purchases,
       ROUND(purchases / views, 4) AS view_to_purchase_rate
FROM funnel
ORDER BY price_quintile;


-- ------------------------------------------------------------
-- 4. REVIEWS & RATINGS
-- ------------------------------------------------------------

-- 4.1 Conversion by rating band
WITH funnel AS (
    SELECT
        p.product_id,
        CASE
            WHEN p.rating < 3.5 THEN '<3.5'
            WHEN p.rating < 4.0 THEN '3.5-4.0'
            WHEN p.rating < 4.5 THEN '4.0-4.5'
            ELSE '4.5-5.0'
        END AS rating_band,
        SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END) AS views,
        SUM(CASE WHEN e.event_type = 'purchase'     THEN 1 ELSE 0 END) AS purchases
    FROM products p
    JOIN user_events e ON e.product_id = p.product_id
    GROUP BY p.product_id, rating_band
)
SELECT rating_band, COUNT(*) AS products,
       ROUND(AVG(purchases / NULLIF(views,0)), 4) AS avg_view_to_purchase_rate
FROM funnel
GROUP BY rating_band
ORDER BY FIELD(rating_band, '<3.5', '3.5-4.0', '4.0-4.5', '4.5-5.0');

-- 4.2 Highly rated, high review-count, but below-median conversion (needs merchandising attention)
WITH funnel AS (
    SELECT
        p.product_id, p.subcategory, p.rating, p.review_count,
        SUM(CASE WHEN e.event_type = 'product_view' THEN 1 ELSE 0 END) AS views,
        SUM(CASE WHEN e.event_type = 'purchase'     THEN 1 ELSE 0 END) AS purchases
    FROM products p
    JOIN user_events e ON e.product_id = p.product_id
    GROUP BY p.product_id, p.subcategory, p.rating, p.review_count
    HAVING views >= 25
),
scored AS (
    SELECT *, purchases / views AS conv_rate,
           AVG(purchases / views) OVER () AS median_ish_conv
    FROM funnel
)
SELECT product_id, subcategory, rating, review_count, views, purchases, ROUND(conv_rate, 4) AS conv_rate
FROM scored
WHERE rating >= 4.3 AND conv_rate < median_ish_conv
ORDER BY rating DESC, conv_rate ASC
LIMIT 20;


-- ------------------------------------------------------------
-- 5. PRODUCT DISCOVERY FUNNEL
-- ------------------------------------------------------------

-- 5.1 Overall funnel counts and stage-to-stage conversion
SELECT
    SUM(event_type = 'search')       AS searches,
    SUM(event_type = 'product_view') AS views,
    SUM(event_type = 'wishlist')     AS wishlists,
    SUM(event_type = 'add_to_cart')  AS carts,
    SUM(event_type = 'purchase')     AS purchases,
    ROUND(SUM(event_type = 'add_to_cart') / SUM(event_type = 'product_view'), 4) AS view_to_cart_rate,
    ROUND(SUM(event_type = 'purchase')    / SUM(event_type = 'add_to_cart'), 4)  AS cart_to_purchase_rate
FROM user_events;

-- 5.2 Drop-off comparison: choice-heavy vs low-choice subcategories
SELECT
    p.choice_heavy_subcategory,
    ROUND(1 - SUM(e.event_type='add_to_cart') / SUM(e.event_type='product_view'), 4) AS view_to_cart_dropoff,
    ROUND(1 - SUM(e.event_type='purchase')    / SUM(e.event_type='add_to_cart'), 4)  AS cart_to_purchase_dropoff
FROM products p
JOIN user_events e ON e.product_id = p.product_id
GROUP BY p.choice_heavy_subcategory;

-- 5.3 Repeat purchase behaviour: orders per customer distribution
SELECT
    order_count_bucket,
    COUNT(*) AS customers
FROM (
    SELECT
        c.customer_id,
        CASE
            WHEN COUNT(o.order_id) = 0 THEN '0 orders'
            WHEN COUNT(o.order_id) = 1 THEN '1 order'
            WHEN COUNT(o.order_id) BETWEEN 2 AND 3 THEN '2-3 orders'
            ELSE '4+ orders'
        END AS order_count_bucket
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.customer_id
    GROUP BY c.customer_id
) t
GROUP BY order_count_bucket
ORDER BY FIELD(order_count_bucket, '0 orders', '1 order', '2-3 orders', '4+ orders');
