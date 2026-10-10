
WITH oct_direct_users AS (
    SELECT DISTINCT user_id FROM fct_session_funnel
    WHERE first_event_month = '2019-10-01' AND has_purchase = TRUE AND has_cart = FALSE
),
nov_behavior AS (
    SELECT 
        user_id,
        MAX((first_event_date IN ('2019-11-14', '2019-11-16', '2019-11-17', '2019-11-29'))::INT) AS in_bf,
        MAX((first_event_date NOT IN ('2019-11-14', '2019-11-16', '2019-11-17', '2019-11-29'))::INT) AS in_non_bf,
        MAX((has_purchase AND NOT has_cart)::INT) AS purc_direct,
        MAX((has_purchase AND has_cart)::INT) AS purc_cart,
        MAX((has_cart AND NOT has_purchase)::INT) AS abandon_cart,
        MAX((NOT has_cart AND NOT has_purchase)::INT) AS view_only
    FROM fct_session_funnel
    WHERE first_event_month = '2019-11-01' AND first_event_date != '2019-11-15'
      AND user_id IN (SELECT user_id FROM oct_direct_users)
    GROUP BY user_id
)
SELECT 
    'Entire Nov (Active Users)' AS segment,
    COUNT(*) AS active_users,
    SUM(purc_direct)*100.0/COUNT(*) AS pct_purc_direct,
    SUM(purc_cart)*100.0/COUNT(*) AS pct_purc_cart,
    SUM(abandon_cart)*100.0/COUNT(*) AS pct_abandon_cart,
    SUM(view_only)*100.0/COUNT(*) AS pct_view_only
FROM nov_behavior
UNION ALL
SELECT 
    'BF Week Active Users' AS segment,
    SUM(in_bf) AS active_users,
    SUM(purc_direct * in_bf)*100.0/NULLIF(SUM(in_bf),0) AS pct_purc_direct,
    SUM(purc_cart * in_bf)*100.0/NULLIF(SUM(in_bf),0) AS pct_purc_cart,
    SUM(abandon_cart * in_bf)*100.0/NULLIF(SUM(in_bf),0) AS pct_abandon_cart,
    SUM(view_only * in_bf)*100.0/NULLIF(SUM(in_bf),0) AS pct_view_only
FROM nov_behavior
UNION ALL
SELECT 
    'Non-BF Week Active Users' AS segment,
    SUM(in_non_bf) AS active_users,
    SUM(purc_direct * in_non_bf)*100.0/NULLIF(SUM(in_non_bf),0) AS pct_purc_direct,
    SUM(purc_cart * in_non_bf)*100.0/NULLIF(SUM(in_non_bf),0) AS pct_purc_cart,
    SUM(abandon_cart * in_non_bf)*100.0/NULLIF(SUM(in_non_bf),0) AS pct_abandon_cart,
    SUM(view_only * in_non_bf)*100.0/NULLIF(SUM(in_non_bf),0) AS pct_view_only
FROM nov_behavior
