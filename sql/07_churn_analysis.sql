-- =============================================================
--  Sales Dashboard — 07: Customer Churn Analysis
-- =============================================================
--  Churned = customer who ordered in 2023 but NOT in 2024
-- =============================================================

WITH customers_2023 AS (
    SELECT DISTINCT customer_id FROM orders
    WHERE status = 'Completed'
      AND order_date BETWEEN '2023-01-01' AND '2023-12-31'
),
customers_2024 AS (
    SELECT DISTINCT customer_id FROM orders
    WHERE status = 'Completed'
      AND order_date BETWEEN '2024-01-01' AND '2024-12-31'
),
churn_base AS (
    SELECT
        c23.customer_id,
        CASE WHEN c24.customer_id IS NULL THEN 1 ELSE 0 END AS is_churned
    FROM customers_2023 c23
    LEFT JOIN customers_2024 c24 ON c23.customer_id = c24.customer_id
)

SELECT
    COUNT(*)                                    AS customers_in_2023,
    SUM(is_churned)                             AS churned_customers,
    COUNT(*) - SUM(is_churned)                  AS retained_customers,
    ROUND(SUM(is_churned) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND((COUNT(*) - SUM(is_churned)) * 100.0 / COUNT(*), 2) AS retention_rate_pct
FROM churn_base;

-- ── Churned Customers Detail ───────────────────────────────
SELECT
    cb.customer_id,
    c.customer_name,
    c.region,
    c.segment,
    SUM(o.amount)     AS last_year_revenue,
    MAX(o.order_date) AS last_order_date,
    CURRENT_DATE - MAX(o.order_date) AS days_since_last_order
FROM churn_base cb
JOIN customers c ON cb.customer_id = c.customer_id
JOIN orders o    ON cb.customer_id = o.customer_id
WHERE cb.is_churned = 1
  AND o.order_date BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY cb.customer_id, c.customer_name, c.region, c.segment
ORDER BY last_year_revenue DESC;
