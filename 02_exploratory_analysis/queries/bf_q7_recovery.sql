
WITH user_sessions AS (
    SELECT 
        user_id, is_abandoned, session_end, has_purchase, first_event_month,
        LEAD(session_start) OVER(PARTITION BY user_id ORDER BY session_start) AS next_start,
        LEAD(has_purchase) OVER(PARTITION BY user_id ORDER BY session_start) AS next_purchased
    FROM fct_session_funnel
),
nov_returns AS (
    SELECT 
        next_start - session_end AS time_to_return,
        next_purchased
    FROM user_sessions
    WHERE is_abandoned AND first_event_month = '2019-11-01' AND next_start IS NOT NULL
)
SELECT 
    (SELECT COUNT(*) FROM fct_session_funnel WHERE is_abandoned AND first_event_month = '2019-11-01') AS total_ab,
    COUNT(*) AS total_returns,
    COUNT(*) FILTER(WHERE time_to_return <= INTERVAL 1 HOUR) AS r_1h,
    COUNT(*) FILTER(WHERE time_to_return <= INTERVAL 24 HOUR) AS r_24h,
    COUNT(*) FILTER(WHERE time_to_return <= INTERVAL 72 HOUR) AS r_72h,
    SUM(next_purchased::INT) AS recovered
FROM nov_returns;
