-- =============================================================
--  Sales Dashboard — 01: Create Tables (PostgreSQL)
-- =============================================================

-- Drop in reverse FK order
DROP TABLE IF EXISTS orders     CASCADE;
DROP TABLE IF EXISTS customers  CASCADE;
DROP TABLE IF EXISTS products   CASCADE;
DROP TABLE IF EXISTS sales_reps CASCADE;


-- ── Sales Reps ─────────────────────────────────────────────
CREATE TABLE sales_reps (
    rep_id          VARCHAR(20)   PRIMARY KEY,
    rep_name        VARCHAR(100)  NOT NULL,
    region          VARCHAR(50),
    team            VARCHAR(50),
    annual_target   NUMERIC(15,2),
    join_date       DATE
);

-- ── Customers ──────────────────────────────────────────────
CREATE TABLE customers (
    customer_id     VARCHAR(20)   PRIMARY KEY,
    customer_name   VARCHAR(150)  NOT NULL,
    city            VARCHAR(100),
    region          VARCHAR(50),
    segment         VARCHAR(50),
    join_date       DATE,
    email           VARCHAR(200),
    tenure_days     INTEGER,
    tenure_years    NUMERIC(5,1)
);

-- ── Products ───────────────────────────────────────────────
CREATE TABLE products (
    product_id          VARCHAR(20)   PRIMARY KEY,
    product_name        VARCHAR(200)  NOT NULL,
    category            VARCHAR(50),
    cost_price          NUMERIC(12,2),
    mrp                 NUMERIC(12,2),
    brand               VARCHAR(100),
    profit_margin_pct   NUMERIC(6,2)
);

-- ── Orders ─────────────────────────────────────────────────
CREATE TABLE orders (
    order_id            VARCHAR(20)   PRIMARY KEY,
    customer_id         VARCHAR(20)   REFERENCES customers(customer_id),
    product_id          VARCHAR(20)   REFERENCES products(product_id),
    sales_rep_id        VARCHAR(20)   REFERENCES sales_reps(rep_id),
    amount              NUMERIC(12,2) NOT NULL,
    order_date          DATE          NOT NULL,
    status              VARCHAR(30),
    order_month         SMALLINT,
    order_quarter       SMALLINT,
    order_year          SMALLINT,
    order_day_of_week   VARCHAR(15),
    is_repeat_customer  SMALLINT DEFAULT 0
);

-- ── Indexes for performance ────────────────────────────────
CREATE INDEX idx_orders_date       ON orders(order_date);
CREATE INDEX idx_orders_status     ON orders(status);
CREATE INDEX idx_orders_customer   ON orders(customer_id);
CREATE INDEX idx_orders_product    ON orders(product_id);
CREATE INDEX idx_customers_region  ON customers(region);
CREATE INDEX idx_products_category ON products(category);

COMMENT ON TABLE orders     IS 'All sales transactions — source: CRM export';
COMMENT ON TABLE customers  IS 'Customer master data — source: CRM export';
COMMENT ON TABLE products   IS 'Product catalog — source: ERP system';
COMMENT ON TABLE sales_reps IS 'Sales team data — source: HR system';
