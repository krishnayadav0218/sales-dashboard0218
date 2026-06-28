-- =============================================================
--  Sales Dashboard — 04: Top Customers by Lifetime Value
-- =============================================================
--  Powers: Customer Segmentation page — Top 10 LTV table
-- =============================================================

WITH customer_stats AS (
    SELECT
        o.customer_id,
        COUNT(o.order_id)                       AS total_orders,
        SUM(o.amount)                           AS lifetime_value,
        ROUND(AVG(o.amount), 2)                 AS avg_order_value,
        MIN(o.order_date)                       AS first_order_date,
        MAX(o.order_date)                       AS last_order_date,
        MAX(o.order_date) - MIN(o.order_date)   AS active_days
    FROM orders o
    WHERE o.status = 'Completed'
    GROUP BY o.customer_id
),
ranked AS (
    SELECT
        cs.*,
        c.customer_name,
        c.city,
        c.region,
        c.segment,
        c.tenure_days,

        -- Tier classification
        CASE
            WHEN cs.lifetime_value > 500000 THEN 'Platinum'
            WHEN cs.lifetime_value > 200000 THEN 'Gold'
            WHEN cs.lifetime_value > 50000  THEN 'Silver'
            ELSE                                 'Bronze'
        END                                     AS customer_tier,

        -- Revenue rank
        RANK() OVER (ORDER BY cs.lifetime_value DESC) AS revenue_rank,

        -- Cumulative % of total revenue
        ROUND(
            cs.lifetime_value * 100.0
            / SUM(cs.lifetime_value) OVER ()
        , 2)                                    AS pct_of_total_revenue

    FROM customer_stats cs
    JOIN customers c ON cs.customer_id = c.customer_id
)

SELECT
    revenue_rank,
    customer_id,
    customer_name,
    city,
    region,
    customer_tier,
    total_orders,
    lifetime_value,
    avg_order_value,
    pct_of_total_revenue,
    first_order_date,
    last_order_date,
    active_days
FROM ranked
ORDER BY revenue_rank
LIMIT 10;
