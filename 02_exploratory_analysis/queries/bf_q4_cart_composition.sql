
WITH cart_events AS (
    SELECT 
        user_session,
        MIN(event_time) AS first_cart,
        MAX(event_time) AS last_cart,
        COUNT(DISTINCT category_code) AS cart_categories
    FROM events
    WHERE event_type = 'cart'
    GROUP BY user_session
),
cart_sessions AS (
    SELECT 
        f.first_event_month AS month,
        f.cart_count,
        (f.cart_count >= 3)::INT AS is_3plus,
        (c.cart_categories >= 2)::INT AS is_multi_cat,
        EXTRACT('epoch' FROM (c.last_cart - c.first_cart)) AS browse_time_sec
    FROM fct_session_funnel f
    JOIN cart_events c ON f.user_session = c.user_session
    WHERE f.has_cart
)
SELECT 
    month,
    AVG(cart_count) AS avg_items,
    QUANTILE_CONT(cart_count, 0.25) AS p25,
    QUANTILE_CONT(cart_count, 0.50) AS p50,
    QUANTILE_CONT(cart_count, 0.75) AS p75,
    QUANTILE_CONT(cart_count, 0.90) AS p90,
    QUANTILE_CONT(cart_count, 0.95) AS p95,
    AVG(is_3plus)*100 AS pct_3plus_items,
    AVG(is_multi_cat)*100 AS pct_multi_cat,
    AVG(browse_time_sec) AS avg_cart_browse_sec
FROM cart_sessions
GROUP BY 1 ORDER BY 1;
