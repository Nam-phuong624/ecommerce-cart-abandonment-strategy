-- Cast + filter raw_events. Views are free — no materialization cost.
SELECT
    event_time,
    event_type,
    product_id,
    category_id,
    NULLIF(TRIM(category_code), '')  AS category_code,
    NULLIF(LOWER(TRIM(brand)), '')   AS brand,
    price,
    user_id,
    user_session,
    CAST(event_time AS DATE) AS event_date,
    date_trunc('month', event_time) AS event_month,
    EXTRACT('hour' FROM event_time) AS event_hour,
    EXTRACT('dow' FROM event_time) AS day_of_week
FROM {{ source('raw', 'events') }}
WHERE
    event_time IS NOT NULL
    AND user_id IS NOT NULL
    AND user_session IS NOT NULL
    AND event_type IN ('view', 'cart', 'remove_from_cart', 'purchase')
    AND price >= 0
