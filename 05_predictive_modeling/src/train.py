import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, precision_score, recall_score, f1_score
import json
import uuid
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 1. Load Data
df = pd.read_parquet("05_data_science/data/features/features_v1.parquet")

# 2. Preprocessing
# Fill nulls for trees (use -1 so it's a distinct branch for missing users)
df['days_since_last_oct'] = df['days_since_last_oct'].fillna(-1)

# One-hot encode price_tier_bucket
df = pd.get_dummies(df, columns=['price_tier_bucket'], drop_first=True)

# Define features
features = [c for c in df.columns if c not in ['user_session', 'target', 'split_group']]

# 3. Splits
X_train = df[df['split_group'] == 'train'][features]
y_train = df[df['split_group'] == 'train']['target']

X_val = df[df['split_group'] == 'val'][features]
y_val = df[df['split_group'] == 'val']['target']

# 4. Train Baselines
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Random Forest (Fast)": RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1),
    "XGBoost": xgb.XGBClassifier(eval_metric='auc', random_state=42, use_label_encoder=False)
}

results = []
log_entries = []

for name, model in models.items():
    print(f"Training {name}...")
    start_time = datetime.now()
    model.fit(X_train, y_train)
    train_time = (datetime.now() - start_time).total_seconds()
    
    # Predict
    y_val_prob = model.predict_proba(X_val)[:, 1]
    y_val_pred = (y_val_prob >= 0.5).astype(int)
    
    # Metrics
    auc = roc_auc_score(y_val, y_val_prob)
    pr_auc = average_precision_score(y_val, y_val_prob)
    f1 = f1_score(y_val, y_val_pred)
    
    results.append({
        "Model": name,
        "Val ROC-AUC": round(auc, 4),
        "Val PR-AUC": round(pr_auc, 4),
        "Val F1": round(f1, 4),
        "Time (s)": round(train_time, 1)
    })
    
    # Log to jsonl
    log_entry = {
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "model_type": name,
        "hyperparams": "default baseline",
        "features_used": features,
        "n_train": len(X_train),
        "n_val": len(X_val),
        "val_metrics": {"auc": auc, "pr_auc": pr_auc, "f1": f1},
        "training_time_sec": train_time
    }
    log_entries.append(log_entry)

# Print Comparison
res_df = pd.DataFrame(results).sort_values(by="Val ROC-AUC", ascending=False)
print("\n--- BASELINE MODELS COMPARISON ---")
print(res_df.to_markdown(index=False))

# Append to training log
with open("05_data_science/logs/training_log.jsonl", "a") as f:
    for entry in log_entries:
        f.write(json.dumps(entry) + "\n")

# Generate NB content
nb_content = '{"cells": [{"cell_type": "markdown", "metadata": {}, "source": ["# 03 Baseline Models\\n", "Comparison of LR, RF, and XGBoost"]}], "metadata": {}, "nbformat": 4, "nbformat_minor": 4}'
with open("05_data_science/notebooks/03_baseline_models.ipynb", "w") as f: f.write(nb_content)

