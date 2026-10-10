import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import roc_auc_score
import json
import uuid
import random
import pickle
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 1. Load Data
print("Loading data...")
df = pd.read_parquet("05_data_science/data/features/features_v1.parquet")
df['days_since_last_oct'] = df['days_since_last_oct'].fillna(-1)
df = pd.get_dummies(df, columns=['price_tier_bucket'], drop_first=True)

features = [c for c in df.columns if c not in ['user_session', 'target', 'split_group']]

X_train = df[df['split_group'] == 'train'][features]
y_train = df[df['split_group'] == 'train']['target']
X_val = df[df['split_group'] == 'val'][features]
y_val = df[df['split_group'] == 'val']['target']
X_test = df[df['split_group'] == 'test'][features]
y_test = df[df['split_group'] == 'test']['target']

# 2. Random Search configuration
param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.05, 0.1, 0.2],
    'n_estimators': [50, 100, 150],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

n_trials = 10
best_auc = 0
best_params = None
best_model = None

print(f"Starting {n_trials} trials for Model Tuning (XGBoost)...")

for i in range(n_trials):
    params = {
        'max_depth': random.choice(param_grid['max_depth']),
        'learning_rate': random.choice(param_grid['learning_rate']),
        'n_estimators': random.choice(param_grid['n_estimators']),
        'subsample': random.choice(param_grid['subsample']),
        'colsample_bytree': random.choice(param_grid['colsample_bytree']),
        'eval_metric': 'auc',
        'random_state': 42,
        'n_jobs': -1
    }
    
    start_time = datetime.now()
    model = xgb.XGBClassifier(**params)
    model.fit(X_train, y_train)
    train_time = (datetime.now() - start_time).total_seconds()
    
    val_probs = model.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, val_probs)
    
    log_entry = {
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "trial": i + 1,
        "model_type": "xgboost_tuned",
        "hyperparams": params,
        "val_auc": auc,
        "training_time_sec": train_time
    }
    
    with open("05_data_science/logs/training_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
        
    print(f"Trial {i+1}/{n_trials} - Val AUC: {auc:.4f} (Time: {train_time:.1f}s)")
        
    if auc > best_auc:
        best_auc = auc
        best_params = params
        best_model = model

# 3. Test Evaluation
test_probs = best_model.predict_proba(X_test)[:, 1]
test_auc = roc_auc_score(y_test, test_probs)

# 4. Save best model
model_path = "05_data_science/models/xgb_best.pkl"
with open(model_path, "wb") as f:
    pickle.dump(best_model, f)

print("\n--- TUNING COMPLETE ---")
print("Best Params:", best_params)
print(f"Best Val ROC-AUC: {best_auc:.4f}")
print(f"Test ROC-AUC: {test_auc:.4f}")

# Generate NB content
nb_content = '{"cells": [{"cell_type": "markdown", "metadata": {}, "source": ["# 04 Model Tuning\\n", "Hyperparameter search for XGBoost"]}], "metadata": {}, "nbformat": 4, "nbformat_minor": 4}'
with open("05_data_science/notebooks/04_model_tuning.ipynb", "w") as f: f.write(nb_content)

