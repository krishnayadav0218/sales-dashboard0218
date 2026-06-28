-- =============================================================
--  Sales Dashboard — 05: Regional Performance vs Target
-- =============================================================
--  Powers: Regional page — map + achievement table
-- =============================================================

WITH regional_sales AS (
    SELECT
        c.region,
        COUNT(DISTINCT o.customer_id)           AS unique_customers,
        COUNT(o.order_id)                       AS total_orders,
        SUM(o.amount)                           AS actual_revenue,
        ROUND(AVG(o.amount), 2)                 AS avg_order_value
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE
        o.status = 'Completed'
        AND o.order_date BETWEEN '2024-01-01' AND '2024-12-31'
    GROUP BY c.region
),
regional_targets AS (
    SELECT
        region,
        SUM(annual_target) AS total_target,
        COUNT(rep_id)      AS rep_count
    FROM sales_reps
    GROUP BY region
)

SELECT
    rs.region,
    rs.unique_customers,
    rs.total_orders,
    rs.actual_revenue,
    rs.avg_order_value,
    rt.total_target                             AS target_revenue,
    rt.rep_count,

    -- Achievement %
    ROUND(
        rs.actual_revenue * 100.0
        / NULLIF(rt.total_target, 0)
    , 1)                                        AS achievement_pct,

    -- Gap (positive = above target, negative = below)
    rs.actual_revenue - rt.total_target         AS target_gap,

    -- Region rank by actual revenue
    RANK() OVER (ORDER BY rs.actual_revenue DESC) AS revenue_rank,

    -- % share of total company revenue
    ROUND(
        rs.actual_revenue * 100.0
        / SUM(rs.actual_revenue) OVER ()
    , 2)                                        AS revenue_share_pct

FROM regional_sales rs
JOIN regional_targets rt ON rs.region = rt.region
ORDER BY actual_revenue DESC;
