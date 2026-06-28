-- =============================================================
--  Sales Dashboard — 03: Monthly Revenue Trend
-- =============================================================
--  Powers: "Monthly Revenue" bar chart on Overview page
-- =============================================================

SELECT
    DATE_TRUNC('month', order_date)               AS month,
    TO_CHAR(order_date, 'Mon YYYY')               AS month_label,
    COUNT(order_id)                               AS total_orders,
    SUM(amount)                                   AS total_revenue,
    ROUND(AVG(amount), 2)                         AS avg_order_value,

    -- Month-over-Month absolute change
    SUM(amount) - LAG(SUM(amount))
        OVER (ORDER BY DATE_TRUNC('month', order_date))
                                                  AS mom_change,

    -- Month-over-Month % growth
    ROUND(
        (SUM(amount) - LAG(SUM(amount))
            OVER (ORDER BY DATE_TRUNC('month', order_date)))
        * 100.0
        / NULLIF(LAG(SUM(amount))
            OVER (ORDER BY DATE_TRUNC('month', order_date)), 0)
    , 2)                                          AS mom_growth_pct,

    -- Running total for the year
    SUM(SUM(amount))
        OVER (
            PARTITION BY EXTRACT(YEAR FROM order_date)
            ORDER BY DATE_TRUNC('month', order_date)
        )                                         AS ytd_revenue

FROM orders
WHERE
    status = 'Completed'
    AND order_date BETWEEN '2024-01-01' AND '2024-12-31'

GROUP BY
    DATE_TRUNC('month', order_date),
    TO_CHAR(order_date, 'Mon YYYY')

ORDER BY month;
