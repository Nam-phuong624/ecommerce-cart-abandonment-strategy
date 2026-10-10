SELECT 
    CAST(first_event_date AS DATE) AS date,
    COUNT(*) FILTER(WHERE has_cart) AS sessions_cart,
    COUNT(*) FILTER(WHERE has_purchase) AS sessions_purchase,
    COUNT(*) FILTER(WHERE is_abandoned) AS sessions_abandoned,
    SUM(purchase_value) AS GMV_purchased,
    SUM(cart_value) FILTER(WHERE is_abandoned) AS GMV_at_risk,
    ROUND((COUNT(*) FILTER(WHERE is_abandoned) * 100.0) / NULLIF(COUNT(*) FILTER(WHERE has_cart), 0), 2) AS abandonment_rate
FROM fct_session_funnel
WHERE first_event_month = '2019-11-01'
GROUP BY first_event_date
ORDER BY first_event_date;
