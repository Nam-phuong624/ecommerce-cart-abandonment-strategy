
WITH peak_day AS (
    SELECT 
        EXTRACT('hour' FROM session_start) AS hour_of_day,
        COUNT(*) FILTER(WHERE has_cart) AS carts,
        COUNT(*) FILTER(WHERE is_abandoned) AS abandons,
        SUM(cart_value) FILTER(WHERE is_abandoned) AS gmv_risk
    FROM fct_session_funnel
    WHERE first_event_date = '2019-11-15'
    GROUP BY 1
)
SELECT 
    hour_of_day, carts, abandons, 
    ROUND(abandons*100.0/NULLIF(carts,0),2) AS abandon_rate,
    gmv_risk
FROM peak_day ORDER BY hour_of_day;
