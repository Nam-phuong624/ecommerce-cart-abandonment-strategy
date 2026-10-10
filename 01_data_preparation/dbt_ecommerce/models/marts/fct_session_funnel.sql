{{ config(materialized='table') }}

WITH single_pass_agg AS (
    SELECT
        user_session,
        user_id,
        MIN(event_time) AS session_start,
        MAX(event_time) AS session_end,
        MIN(event_month) AS first_event_month,
        MIN(event_date) AS first_event_date,
        COUNT(*) AS total_events,
        
        -- Event counts
        COUNT(*) FILTER (WHERE event_type = 'view') AS view_count,
        COUNT(*) FILTER (WHERE event_type = 'cart') AS cart_count,
        COUNT(*) FILTER (WHERE event_type = 'remove_from_cart') AS remove_count,
        COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchase_count,
        
        -- Unique dimension proxies (Approximate for memory safety on 110M rows)
        APPROX_COUNT_DISTINCT(product_id) AS unique_products,
        APPROX_COUNT_DISTINCT(category_code) AS unique_categories,

        -- Values
        COALESCE(SUM(price) FILTER (WHERE event_type = 'cart'), 0) AS cart_value,
        COALESCE(SUM(price) FILTER (WHERE event_type = 'purchase'), 0) AS purchase_value,

        -- First event times
        MIN(event_time) FILTER (WHERE event_type = 'view') AS first_view_time,
        MIN(event_time) FILTER (WHERE event_type = 'cart') AS first_cart_time,
        MIN(event_time) FILTER (WHERE event_type = 'purchase') AS first_purchase_time
    FROM {{ ref('stg_events') }}
    GROUP BY user_session, user_id
)

SELECT
    user_session,
    user_id,
    session_start,
    session_end,
    DATEDIFF('second', session_start, session_end) AS session_duration_sec,
    first_event_month,
    first_event_date,
    total_events,
    view_count,
    cart_count,
    remove_count,
    purchase_count,
    unique_products,
    unique_categories,

    -- Funnel flags
    (view_count > 0)      AS has_view,
    (cart_count > 0)      AS has_cart,
    (purchase_count > 0)  AS has_purchase,

    -- Values
    cart_value,
    purchase_value,

    -- Time deltas from first view (seconds)
    DATEDIFF('second', first_view_time, first_cart_time)      AS secs_view_to_cart,
    DATEDIFF('second', first_view_time, first_purchase_time)  AS secs_view_to_purchase,
    DATEDIFF('second', first_cart_time, first_purchase_time)  AS secs_cart_to_purchase,

    -- Sessions where user explicitly removed all cart items (remove_count >= cart_count)
    (cart_count > 0 AND purchase_count = 0
     AND remove_count >= cart_count)          AS is_full_clear,

    -- True abandonment: had cart, no purchase, did NOT fully clear the cart
    (cart_count > 0 AND purchase_count = 0
     AND remove_count < cart_count)           AS is_abandoned

FROM single_pass_agg
