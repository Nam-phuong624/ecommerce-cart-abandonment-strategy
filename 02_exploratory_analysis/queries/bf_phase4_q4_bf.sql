
WITH oct_direct_users AS (
    SELECT DISTINCT user_id FROM fct_session_funnel
    WHERE first_event_month = '2019-10-01' AND has_purchase = TRUE AND has_cart = FALSE
),
oct_behavior AS (
    SELECT AVG(purchase_count) AS avg_items_oct 
    FROM fct_session_funnel 
    WHERE first_event_month = '2019-10-01' AND has_purchase = TRUE AND has_cart = FALSE
      AND user_id IN (SELECT user_id FROM oct_direct_users)
)
SELECT 
    CASE WHEN first_event_date IN ('2019-11-14', '2019-11-16', '2019-11-17', '2019-11-29') THEN 'BF Week' ELSE 'Non-BF Week' END AS period,
    COUNT(*) FILTER(WHERE is_abandoned)*100.0/NULLIF(COUNT(*) FILTER(WHERE has_cart),0) AS abandon_rate_pct,
    AVG(session_duration_sec) FILTER(WHERE is_abandoned) AS avg_time_to_abandon_sec,
    AVG(cart_count) FILTER(WHERE has_cart) AS avg_items_per_cart,
    (SELECT avg_items_oct FROM oct_behavior) AS reference_oct_items
FROM fct_session_funnel
WHERE first_event_month = '2019-11-01' AND first_event_date != '2019-11-15'
  AND user_id IN (SELECT user_id FROM oct_direct_users)
GROUP BY 1
