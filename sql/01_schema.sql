-- ============================================================
-- Beauty Product Growth & Recommendation Analytics
-- MySQL Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS beauty_analytics;
USE beauty_analytics;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS user_events;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- ------------------------------------------------------------
-- CUSTOMERS
-- ------------------------------------------------------------
CREATE TABLE customers (
    customer_id       INT PRIMARY KEY,
    age_group          VARCHAR(10)  NOT NULL,
    gender             VARCHAR(20),
    city               VARCHAR(50)  NOT NULL,
    new_or_returning   VARCHAR(10)  NOT NULL,
    signup_date        DATE         NOT NULL
);

-- ------------------------------------------------------------
-- PRODUCTS
-- ------------------------------------------------------------
CREATE TABLE products (
    product_id                 INT PRIMARY KEY,
    category                   VARCHAR(30)  NOT NULL,
    subcategory                VARCHAR(30)  NOT NULL,
    brand                      VARCHAR(50)  NOT NULL,
    price                      DECIMAL(10,2) NOT NULL,
    discount_pct                TINYINT      NOT NULL,
    rating                     DECIMAL(2,1) NOT NULL,
    review_count               INT          NOT NULL,
    choice_heavy_subcategory   BOOLEAN      NOT NULL
        COMMENT 'TRUE if subcategory has 20+ near-identical SKUs (choice overload flag)'
);

-- ------------------------------------------------------------
-- USER EVENTS  (search / product_view / wishlist / add_to_cart / purchase / review)
-- ------------------------------------------------------------
CREATE TABLE user_events (
    event_id     BIGINT PRIMARY KEY,
    customer_id  INT NOT NULL,
    product_id   INT NULL,                 -- NULL for pure "search" events
    event_type   VARCHAR(20) NOT NULL,
    subcategory  VARCHAR(30),
    event_time   DATETIME NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id)
);

CREATE INDEX idx_events_customer   ON user_events(customer_id);
CREATE INDEX idx_events_product    ON user_events(product_id);
CREATE INDEX idx_events_type       ON user_events(event_type);
CREATE INDEX idx_events_time       ON user_events(event_time);

-- ------------------------------------------------------------
-- ORDERS
-- ------------------------------------------------------------
CREATE TABLE orders (
    order_id      INT PRIMARY KEY,
    customer_id   INT NOT NULL,
    order_date    DATE NOT NULL,
    total_amount  DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date     ON orders(order_date);

-- ------------------------------------------------------------
-- ORDER ITEMS
-- ------------------------------------------------------------
CREATE TABLE order_items (
    order_id       INT NOT NULL,
    product_id     INT NOT NULL,
    quantity       INT NOT NULL,
    selling_price  DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- ------------------------------------------------------------
-- LOAD DATA (adjust local file paths, run with LOCAL INFILE enabled)
-- ------------------------------------------------------------
-- LOAD DATA LOCAL INFILE 'customers.csv'
--   INTO TABLE customers FIELDS TERMINATED BY ',' ENCLOSED BY '"'
--   LINES TERMINATED BY '\n' IGNORE 1 ROWS
--   (customer_id, age_group, gender, city, signup_date, new_or_returning);
--
-- LOAD DATA LOCAL INFILE 'products.csv'
--   INTO TABLE products FIELDS TERMINATED BY ',' ENCLOSED BY '"'
--   LINES TERMINATED BY '\n' IGNORE 1 ROWS
--   (product_id, category, subcategory, brand, price, discount_pct, rating, review_count, choice_heavy_subcategory);
--
-- LOAD DATA LOCAL INFILE 'user_events.csv'
--   INTO TABLE user_events FIELDS TERMINATED BY ',' ENCLOSED BY '"'
--   LINES TERMINATED BY '\n' IGNORE 1 ROWS
--   (event_id, customer_id, product_id, event_type, subcategory, event_time);
--
-- LOAD DATA LOCAL INFILE 'orders.csv'
--   INTO TABLE orders FIELDS TERMINATED BY ',' ENCLOSED BY '"'
--   LINES TERMINATED BY '\n' IGNORE 1 ROWS
--   (order_id, customer_id, order_date, total_amount);
--
-- LOAD DATA LOCAL INFILE 'order_items.csv'
--   INTO TABLE order_items FIELDS TERMINATED BY ',' ENCLOSED BY '"'
--   LINES TERMINATED BY '\n' IGNORE 1 ROWS
--   (order_id, product_id, quantity, selling_price);
