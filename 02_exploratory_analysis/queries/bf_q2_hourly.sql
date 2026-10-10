
WITH hourly AS (
    SELECT 
        EXTRACT('hour' FROM session_start) AS hour_bin,
        first_event_month,
        COUNT(*) FILTER(WHERE has_cart) AS cart_sessions,
        COUNT(*) FILTER(WHERE is_abandoned) AS abandoned_sessions
    FROM fct_session_funnel
    GROUP BY 1, 2
)
SELECT 
    COALESCE(o.hour_bin, n.hour_bin) AS hour,
    o.cart_sessions AS cart_oct,
    n.cart_sessions AS cart_nov,
    (n.cart_sessions * 1.0 / NULLIF(o.cart_sessions, 0)) AS traffic_multiplier,
    (o.abandoned_sessions * 100.0 / NULLIF(o.cart_sessions, 0)) AS abandon_rate_oct,
    (n.abandoned_sessions * 100.0 / NULLIF(n.cart_sessions, 0)) AS abandon_rate_nov,
    (n.abandoned_sessions * 100.0 / NULLIF(n.cart_sessions, 0)) - 
    (o.abandoned_sessions * 100.0 / NULLIF(o.cart_sessions, 0)) AS delta_pp
FROM (SELECT * FROM hourly WHERE first_event_month = '2019-10-01') o
FULL OUTER JOIN (SELECT * FROM hourly WHERE first_event_month = '2019-11-01') n ON o.hour_bin = n.hour_bin
ORDER BY hour;
