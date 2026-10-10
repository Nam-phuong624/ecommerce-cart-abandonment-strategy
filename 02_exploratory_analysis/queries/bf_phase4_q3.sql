
WITH oct_direct_users AS (
    SELECT DISTINCT user_id FROM fct_session_funnel
    WHERE first_event_month = '2019-10-01' AND has_purchase = TRUE AND has_cart = FALSE
),
nov_rev AS (
    SELECT 
        SUM(purchase_value) FILTER(WHERE has_cart = FALSE AND has_purchase = TRUE) AS gmv_direct,
        SUM(purchase_value) FILTER(WHERE has_cart = TRUE AND has_purchase = TRUE) AS gmv_cart,
        SUM(cart_value) FILTER(WHERE is_abandoned = TRUE) AS gmv_risk
    FROM fct_session_funnel
    WHERE first_event_month = '2019-11-01' AND first_event_date != '2019-11-15'
      AND user_id IN (SELECT user_id FROM oct_direct_users)
),
aov_oct AS (
    SELECT SUM(purchase_value)/NULLIF(COUNT(*),0) AS aov_oct
    FROM fct_session_funnel
    WHERE first_event_month = '2019-10-01' AND has_purchase = TRUE
      AND user_id IN (SELECT user_id FROM oct_direct_users)
),
aov_nov AS (
    SELECT SUM(purchase_value)/NULLIF(COUNT(*),0) AS aov_nov
    FROM fct_session_funnel
    WHERE first_event_month = '2019-11-01' AND has_purchase = TRUE AND first_event_date != '2019-11-15'
      AND user_id IN (SELECT user_id FROM oct_direct_users)
)
SELECT 
    n.gmv_direct AS nov_gmv_direct_retained,
    n.gmv_cart AS nov_gmv_cart_migrated,
    n.gmv_risk AS nov_gmv_at_risk_migrated,
    o.aov_oct AS oct_cohort_aov,
    an.aov_nov AS nov_cohort_aov,
    an.aov_nov - o.aov_oct AS aov_delta_abs
FROM nov_rev n CROSS JOIN aov_oct o CROSS JOIN aov_nov an
