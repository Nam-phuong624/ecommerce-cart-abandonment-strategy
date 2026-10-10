
WITH base AS (
    SELECT 
        first_event_month,
        COUNT(*) AS total_purc,
        COUNT(*) FILTER(WHERE has_cart=FALSE) AS direct_purc,
        COUNT(*) FILTER(WHERE has_cart=TRUE) AS cart_purc,
        SUM(purchase_value) FILTER(WHERE has_cart=FALSE) AS direct_gmv,
        SUM(purchase_value) FILTER(WHERE has_cart=TRUE) AS cart_gmv,
        SUM(purchase_value) AS total_gmv
    FROM fct_session_funnel
    WHERE has_purchase = TRUE 
      AND (first_event_month = '2019-10-01' OR 
          (first_event_month = '2019-11-01' AND first_event_date != '2019-11-15'))
    GROUP BY 1
)
SELECT 
    'October 2019' AS period,
    total_purc,
    direct_purc,
    ROUND(direct_purc * 100.0 / total_purc, 2) AS direct_pct,
    cart_purc,
    ROUND(cart_purc * 100.0 / total_purc, 2) AS cart_pct,
    direct_gmv,
    cart_gmv,
    total_gmv
FROM base WHERE first_event_month = '2019-10-01'
UNION ALL
SELECT 
    'November 2019 (excl Nov 15)' AS period,
    total_purc,
    direct_purc,
    ROUND(direct_purc * 100.0 / total_purc, 2) AS direct_pct,
    cart_purc,
    ROUND(cart_purc * 100.0 / total_purc, 2) AS cart_pct,
    direct_gmv,
    cart_gmv,
    total_gmv
FROM base WHERE first_event_month = '2019-11-01'
