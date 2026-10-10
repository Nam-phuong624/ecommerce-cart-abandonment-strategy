import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_recall_curve, average_precision_score, brier_score_loss, confusion_matrix
from sklearn.calibration import calibration_curve
import os
import warnings
warnings.filterwarnings('ignore')

print("Loading Data and Model...")
# Load data
df = pd.read_parquet("05_data_science/data/features/features_v1.parquet")
df['days_since_last_oct'] = df['days_since_last_oct'].fillna(-1)
df = pd.get_dummies(df, columns=['price_tier_bucket'], drop_first=True)
features = [c for c in df.columns if c not in ['user_session', 'target', 'split_group']]
X_test = df[df['split_group'] == 'test'][features]
y_test = df[df['split_group'] == 'test']['target']

# Load model
with open("05_data_science/models/xgb_best.pkl", "rb") as f:
    model = pickle.load(f)

test_probs = model.predict_proba(X_test)[:, 1]
os.makedirs("05_data_science/reports/plots", exist_ok=True)

# 1. PR Curve
print("Generating PR Curve...")
precision, recall, thresholds_pr = precision_recall_curve(y_test, test_probs)
pr_auc = average_precision_score(y_test, test_probs)
plt.figure()
plt.plot(recall, precision, label=f'PR AUC = {pr_auc:.3f}', color='blue')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend()
plt.savefig('05_data_science/reports/plots/pr_curve.png')
plt.close()

# 2. Calibration Curve
print("Generating Calibration Curve...")
prob_true, prob_pred = calibration_curve(y_test, test_probs, n_bins=10)
brier = brier_score_loss(y_test, test_probs)
plt.figure()
plt.plot(prob_pred, prob_true, marker='o', label='XGBoost', color='orange')
plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfectly calibrated')
plt.xlabel('Mean predicted probability')
plt.ylabel('Fraction of positives')
plt.title(f'Calibration Curve (Brier: {brier:.3f})')
plt.legend()
plt.savefig('05_data_science/reports/plots/calibration_curve.png')
plt.close()

# 3. Profit Curve (ROI)
print("Generating ROI/Profit Curve...")
thresholds = np.linspace(0.1, 0.9, 100)
profits = []

for t in thresholds:
    preds = (test_probs >= t).astype(int)
    tp = np.sum((preds == 1) & (y_test == 1))
    fp = np.sum((preds == 1) & (y_test == 0))
    # Margin=$30, Discount=$10, Conv=20% -> Expected Value of Intervention per TP = +$4, Loss per FP = -$10
    profit = (tp * 4) - (fp * 10)
    profits.append(profit)

best_idx = np.argmax(profits)
best_thresh = thresholds[best_idx]
best_profit = profits[best_idx]

plt.figure()
plt.plot(thresholds, profits, label='Expected Delta Profit ($)', color='green')
plt.axvline(best_thresh, color='red', linestyle='--', label=f'Optimal Cut-off: {best_thresh:.2f}')
plt.axhline(0, color='gray', linestyle='-')
plt.xlabel('Decision Threshold (Probability)')
plt.ylabel('Incremental Profit ($)')
plt.title('Business ROI vs Model Threshold')
plt.legend()
plt.savefig('05_data_science/reports/plots/profit_curve.png')
plt.close()

best_preds = (test_probs >= best_thresh).astype(int)
cm = confusion_matrix(y_test, best_preds)

print(f"\n--- DEEP EVALUATION RESULTS ---")
print(f"PR-AUC: {pr_auc:.4f}")
print(f"Brier Score: {brier:.4f}")
print(f"Optimal Threshold: {best_thresh:.2f}")
print(f"Expected Delta Profit (Test set only): ${best_profit:,.2f}")
print(f"Confusion Matrix at Threshold {best_thresh:.2f}:")
print(f"TN: {cm[0,0]} | FP: {cm[0,1]}")
print(f"FN: {cm[1,0]} | TP: {cm[1,1]}")

