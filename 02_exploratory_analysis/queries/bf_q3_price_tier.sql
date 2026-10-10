
WITH tiered AS (
    SELECT 
        first_event_month,
        CASE 
            WHEN cart_value < 50 THEN 1
            WHEN cart_value < 200 THEN 2
            WHEN cart_value < 500 THEN 3
            WHEN cart_value < 1000 THEN 4
            ELSE 5 END AS sort_order,
        CASE 
            WHEN cart_value < 50 THEN '[$0-50]'
            WHEN cart_value < 200 THEN '[$50-200]'
            WHEN cart_value < 500 THEN '[$200-500]'
            WHEN cart_value < 1000 THEN '[$500-1000]'
            ELSE '[$1000+]' END AS cart_tier,
        COUNT(*) AS carts,
        COUNT(*) FILTER(WHERE is_abandoned) AS abandons,
        SUM(cart_value) FILTER(WHERE is_abandoned) AS gmv_risk
    FROM fct_session_funnel WHERE has_cart
    GROUP BY 1, 2, 3
)
SELECT 
    COALESCE(o.sort_order, n.sort_order) AS sort_order,
    COALESCE(o.cart_tier, n.cart_tier) AS cart_tier,
    o.carts AS carts_oct, o.abandons AS ab_oct, (o.abandons*100.0/NULLIF(o.carts,0)) AS rate_oct,
    n.carts AS carts_nov, n.abandons AS ab_nov, (n.abandons*100.0/NULLIF(n.carts,0)) AS rate_nov,
    (n.abandons*100.0/NULLIF(n.carts,0)) - (o.abandons*100.0/NULLIF(o.carts,0)) AS delta_pp,
    n.gmv_risk AS gmv_at_risk_nov
FROM (SELECT * FROM tiered WHERE first_event_month = '2019-10-01') o
FULL OUTER JOIN (SELECT * FROM tiered WHERE first_event_month = '2019-11-01') n ON o.sort_order = n.sort_order
ORDER BY sort_order;
