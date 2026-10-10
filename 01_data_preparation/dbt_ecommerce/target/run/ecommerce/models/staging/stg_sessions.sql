
  
  create view "ecommerce"."main"."stg_sessions__dbt_tmp" as (
    -- Session-level enrichment. One row per user_session.
-- Partitioned by first event's month so sessions that span months
-- are bucketed by when they started.
SELECT
    user_session,
    user_id,
    MIN(event_time)                             AS session_start,
    MAX(event_time)                             AS session_end,
    DATEDIFF('second', MIN(event_time), MAX(event_time)) AS session_duration_sec,
    MIN(event_month)                            AS first_event_month,
    MIN(event_date)                             AS first_event_date,
    COUNT(*)                                    AS total_events,
    COUNT(*) FILTER (WHERE event_type = 'view')              AS view_count,
    COUNT(*) FILTER (WHERE event_type = 'cart')              AS cart_count,
    COUNT(*) FILTER (WHERE event_type = 'remove_from_cart')  AS remove_count,
    COUNT(*) FILTER (WHERE event_type = 'purchase')          AS purchase_count,
    COUNT(DISTINCT product_id)                  AS unique_products,
    COUNT(DISTINCT category_code)               AS unique_categories
FROM "ecommerce"."main"."stg_events"
GROUP BY user_session, user_id
  );
