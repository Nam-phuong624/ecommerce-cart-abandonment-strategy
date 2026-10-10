
SELECT 
    first_event_month,
    COUNT(*) AS total_sessions,
    COUNT(*) FILTER(WHERE has_cart) AS sessions_cart,
    COUNT(*) FILTER(WHERE has_purchase) AS sessions_purchase,
    SUM(purchase_value) AS gmv_purchased,
    SUM(cart_value) FILTER(WHERE is_abandoned) AS gmv_at_risk,
    COUNT(*) FILTER(WHERE has_cart)*100.0/NULLIF(COUNT(*) FILTER(WHERE has_view),0) AS view_to_cart,
    COUNT(*) FILTER(WHERE has_purchase)*100.0/NULLIF(COUNT(*) FILTER(WHERE has_cart),0) AS cart_to_purchase
FROM fct_session_funnel
GROUP BY 1 ORDER BY 1;
