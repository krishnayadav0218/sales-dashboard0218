-- =============================================================
--  Sales Dashboard — 06: Product Category Analysis
-- =============================================================
--  Powers: Products page — category breakdown + margin table
-- =============================================================

SELECT
    p.category,
    COUNT(DISTINCT p.product_id)                AS product_count,
    COUNT(o.order_id)                           AS total_orders,
    SUM(o.amount)                               AS total_revenue,
    ROUND(AVG(o.amount), 2)                     AS avg_selling_price,
    ROUND(AVG(p.profit_margin_pct), 2)          AS avg_margin_pct,
    SUM(o.amount - p.cost_price)                AS total_profit,

    -- Revenue rank
    RANK() OVER (ORDER BY SUM(o.amount) DESC)   AS revenue_rank,

    -- % of total revenue
    ROUND(
        SUM(o.amount) * 100.0
        / SUM(SUM(o.amount)) OVER ()
    , 2)                                        AS revenue_share_pct,

    -- Best-selling product in category
    (
        SELECT p2.product_name
        FROM orders o2
        JOIN products p2 ON o2.product_id = p2.product_id
        WHERE p2.category = p.category AND o2.status = 'Completed'
        GROUP BY p2.product_name
        ORDER BY SUM(o2.amount) DESC
        LIMIT 1
    )                                           AS top_product

FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'Completed'
GROUP BY p.category
ORDER BY total_revenue DESC;
