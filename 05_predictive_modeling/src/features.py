import duckdb
import pandas as pd
import os

def build_features(db_path, output_dir):
    con = duckdb.connect(db_path, read_only=True)
    con.execute("PRAGMA memory_limit='3.5GB'")
    
    os.makedirs(output_dir, exist_ok=True)
    features_path = os.path.join(output_dir, "features_v1.parquet")
    
    sql = f"""
    COPY (
        WITH oct_history AS (
            SELECT 
                user_id,
                SUM(has_purchase::INT) AS oct_purchase_count,
                SUM((has_cart AND NOT has_purchase)::INT) AS oct_abandon_count,
                SUM(purchase_value) AS oct_total_gmv,
                MAX(session_end) AS last_oct_session
            FROM fct_session_funnel
            WHERE first_event_month = '2019-10-01'
            GROUP BY user_id
        ),
        ml_base AS (
            SELECT 
                f.user_session,
                f.is_abandoned::INT AS target,
                
                -- Time Features
                EXTRACT('hour' FROM f.session_start) AS hour_of_day,
                EXTRACT('isodow' FROM f.session_start) AS day_of_week,
                (f.first_event_date IN ('2019-11-14', '2019-11-16', '2019-11-17', '2019-11-29'))::INT AS is_bf_week,
                
                -- Behavioral Features (Snapshot at end of cart interactions)
                f.view_count,
                f.cart_count,
                f.cart_value,
                COALESCE(f.cart_value / NULLIF(f.cart_count, 0), 0) AS avg_item_price,
                
                -- Price Tier Category
                CASE 
                    WHEN (f.cart_value / NULLIF(f.cart_count, 0)) < 50 THEN '0-50'
                    WHEN (f.cart_value / NULLIF(f.cart_count, 0)) < 200 THEN '50-200'
                    WHEN (f.cart_value / NULLIF(f.cart_count, 0)) < 500 THEN '200-500'
                    WHEN (f.cart_value / NULLIF(f.cart_count, 0)) < 1000 THEN '500-1000'
                    ELSE '1000+'
                END AS price_tier_bucket,
                
                -- Historical User Features
                COALESCE(h.oct_purchase_count, 0) AS oct_purchase_count,
                COALESCE(h.oct_abandon_count, 0) AS oct_abandon_count,
                (h.user_id IS NOT NULL)::INT AS is_returning_user,
                EXTRACT('epoch' FROM (f.session_start - h.last_oct_session))/86400.0 AS days_since_last_oct,
                
                -- Split Routing
                CASE 
                    WHEN f.first_event_date BETWEEN '2019-10-01' AND '2019-11-10' THEN 'train'
                    WHEN f.first_event_date BETWEEN '2019-11-11' AND '2019-11-20' THEN 'val'
                    WHEN f.first_event_date BETWEEN '2019-11-21' AND '2019-11-30' THEN 'test'
                END AS split_group

            FROM fct_session_funnel f
            LEFT JOIN oct_history h ON f.user_id = h.user_id
            WHERE f.has_cart = TRUE AND f.first_event_date != '2019-11-15'
        )
        SELECT * FROM ml_base
    ) TO '{features_path}' (FORMAT PARQUET);
    """
    
    print("Building features and saving to Parquet...")
    con.execute(sql)
    print(f"Saved to {features_path}")
    
    # Check nulls and summary
    df = con.execute(f"SELECT * FROM read_parquet('{features_path}') LIMIT 100000").fetchdf()
    print("\\n--- FEATURE PIPELINE SUMMARY ---")
    print(f"Total Features (excluding IDs & Target): {len(df.columns) - 3}")
    print("\\nNull Rates (sample 100k):")
    null_rates = (df.isnull().sum() / len(df) * 100).round(2)
    print(null_rates[null_rates > 0].to_string())
    
    # Generate NB content
    nb_content = '{"cells": [{"cell_type": "markdown", "metadata": {}, "source": ["# 02 Feature Engineering\\n", "Pipeline to build ML features safely"]}], "metadata": {}, "nbformat": 4, "nbformat_minor": 4}'
    with open("05_data_science/notebooks/02_feature_engineering.ipynb", "w") as f: f.write(nb_content)
    
if __name__ == "__main__":
    build_features("data/processed/ecommerce.duckdb", "05_data_science/data/features")
