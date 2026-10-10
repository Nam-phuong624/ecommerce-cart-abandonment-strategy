
WITH oct_direct AS (
    SELECT DISTINCT user_id FROM fct_session_funnel
    WHERE first_event_month = '2019-10-01' AND has_purchase = TRUE AND has_cart = FALSE
),
oct_cart AS (
    SELECT DISTINCT user_id FROM fct_session_funnel
    WHERE first_event_month = '2019-10-01' AND has_purchase = TRUE AND has_cart = TRUE
),
overlap AS (
    SELECT COUNT(*) AS count FROM oct_direct d JOIN oct_cart c ON d.user_id = c.user_id
),
nov_active AS (
    SELECT DISTINCT user_id FROM fct_session_funnel
    WHERE first_event_month = '2019-11-01' AND first_event_date != '2019-11-15'
),
direct_in_nov AS (
    SELECT COUNT(*) AS count FROM oct_direct d JOIN nov_active n ON d.user_id = n.user_id
)
SELECT
    (SELECT COUNT(*) FROM oct_direct) AS direct_native_users,
    (SELECT COUNT(*) FROM oct_cart) AS cart_native_users,
    (SELECT count FROM overlap) AS overlap_users,
    (SELECT count FROM direct_in_nov) AS direct_active_in_nov,
    (SELECT COUNT(*) FROM oct_direct) - (SELECT count FROM direct_in_nov) AS direct_not_active_in_nov
