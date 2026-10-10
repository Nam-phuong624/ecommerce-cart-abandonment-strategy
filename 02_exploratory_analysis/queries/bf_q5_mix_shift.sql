
WITH cart_items AS (
    SELECT 
        e.category_code,
        e.brand,
        f.first_event_month AS month,
        e.price
    FROM events e
    JOIN fct_session_funnel f ON e.user_session = f.user_session
    WHERE e.event_type = 'cart' AND f.is_abandoned
),
agg AS (
    SELECT 
        COALESCE(category_code, 'unknown') AS cat,
        month,
        SUM(price) AS gmv_risk
    FROM cart_items
    GROUP BY 1, 2
)
SELECT 
    COALESCE(o.cat, n.cat) AS category,
    o.gmv_risk AS gmv_risk_oct,
    n.gmv_risk AS gmv_risk_nov,
    (n.gmv_risk - o.gmv_risk) / NULLIF(o.gmv_risk, 0) * 100 AS delta_pct
FROM (SELECT * FROM agg WHERE month = '2019-10-01') o
FULL OUTER JOIN (SELECT * FROM agg WHERE month = '2019-11-01') n ON o.cat = n.cat
ORDER BY n.gmv_risk DESC NULLS LAST
LIMIT 10;
