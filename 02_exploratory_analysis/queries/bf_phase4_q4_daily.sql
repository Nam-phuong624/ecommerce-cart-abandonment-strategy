
WITH oct_direct_users AS (
    SELECT DISTINCT user_id FROM fct_session_funnel
    WHERE first_event_month = '2019-10-01' AND has_purchase = TRUE AND has_cart = FALSE
)
SELECT 
    CAST(first_event_date AS DATE) AS date,
    COUNT(*) AS cohort_sessions,
    COUNT(*) FILTER(WHERE has_cart = TRUE) AS cart_sessions,
    COUNT(*) FILTER(WHERE has_cart = TRUE)*100.0/NULLIF(COUNT(*),0) AS migration_rate_pct
FROM fct_session_funnel
WHERE first_event_month = '2019-11-01' AND first_event_date != '2019-11-15'
  AND user_id IN (SELECT user_id FROM oct_direct_users)
GROUP BY 1 ORDER BY 1
