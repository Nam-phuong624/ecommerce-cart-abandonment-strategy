import duckdb
import pandas as pd
import json

db_path = "data/processed/ecommerce.duckdb"
con = duckdb.connect(db_path, read_only=True)

print("--- TARGET BALANCE (Sessions with Cart) ---")
balance_sql = """
SELECT 
    COUNT(*) as total_cart_sessions,
    SUM(is_abandoned::INT) as abandoned_sessions,
    SUM(is_abandoned::INT)*100.0/COUNT(*) as abandon_rate_pct
FROM fct_session_funnel 
WHERE has_cart = TRUE AND first_event_date != '2019-11-15'
"""
df_balance = con.execute(balance_sql).fetchdf()
print(df_balance.to_markdown(index=False))

print("\n--- TRAIN/VAL/TEST SPLITS ---")
split_sql = """
SELECT 
    CASE 
        WHEN first_event_date BETWEEN '2019-10-01' AND '2019-11-10' THEN '1_Train'
        WHEN first_event_date BETWEEN '2019-11-11' AND '2019-11-20' THEN '2_Val'
        WHEN first_event_date BETWEEN '2019-11-21' AND '2019-11-30' THEN '3_Test'
    END AS split,
    COUNT(*) as sessions,
    SUM(is_abandoned::INT)*100.0/COUNT(*) as abandon_rate_pct
FROM fct_session_funnel
WHERE has_cart = TRUE AND first_event_date != '2019-11-15'
GROUP BY 1 ORDER BY 1
"""
df_split = con.execute(split_sql).fetchdf()
print(df_split.to_markdown(index=False))

print("\n--- FEATURE DISTRIBUTIONS (Rough Stats) ---")
feat_sql = """
SELECT 
    AVG(view_count) as avg_views_before_cart,
    AVG(cart_count) as avg_cart_items,
    AVG(session_duration_sec) as avg_duration_sec,
    AVG(cart_value) as avg_cart_value,
    COUNT(*) FILTER(WHERE has_purchase) as purchased_sessions
FROM fct_session_funnel
WHERE has_cart = TRUE AND first_event_date != '2019-11-15'
"""
df_feat = con.execute(feat_sql).fetchdf()
print(df_feat.to_markdown(index=False))

# Dump a minimal notebook
nb_content = {
 "cells": [
  {"cell_type": "markdown", "metadata": {}, "source": ["# 01 EDA Features\n", "Exploratory Data Analysis for ML Propensity Model"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["import duckdb\n", "import pandas as pd\n", "import matplotlib.pyplot as plt\n", "con = duckdb.connect('../../data/processed/ecommerce.duckdb', read_only=True)"]}
 ],
 "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
 "nbformat": 4, "nbformat_minor": 4
}
with open("05_data_science/notebooks/01_eda_features.ipynb", "w") as f:
    json.dump(nb_content, f)

