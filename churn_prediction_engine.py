"""
SaaS Churn Risk Scoring & Retention Engine
Author: Puneet Goswami
Description: Evaluates product telemetry and trains an anomaly/churn classification
             model to identify enterprise accounts showing disengagement signals.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score


def generate_saas_telemetry(n_accounts: int = 12000) -> pd.DataFrame:
    """Generates synthetic product engagement logs."""
    np.random.seed(42)

    account_ids = [f"ACC-{10000 + i}" for i in range(n_accounts)]
    plan_tier = np.random.choice(["Starter", "Professional", "Enterprise"], size=n_accounts, p=[0.50, 0.35, 0.15])
    contract_age_months = np.random.randint(1, 36, size=n_accounts)
    
    # Feature 1: License seat utilization (0.10 to 1.0)
    seat_utilization = np.round(np.random.uniform(0.15, 1.0, size=n_accounts), 2)
    
    # Feature 2: Weekly active days in last 30 days (0 to 28)
    active_days_l30 = np.random.randint(1, 29, size=n_accounts)
    
    # Feature 3: Unresolved high-priority support tickets
    escalated_tickets = np.random.poisson(lam=0.7, size=n_accounts)

    # Churn probability calculation based on realistic engagement drops
    risk_score = (
        0.05
        + 0.40 * (seat_utilization < 0.40)
        + 0.35 * (active_days_l30 < 8)
        + 0.20 * (escalated_tickets >= 3)
    )
    churn_flag = (np.random.rand(n_accounts) < np.clip(risk_score, 0.02, 0.95)).astype(int)

    return pd.DataFrame({
        "account_id": account_ids,
        "plan_tier": plan_tier,
        "contract_age_months": contract_age_months,
        "seat_utilization": seat_utilization,
        "active_days_l30": active_days_l30,
        "escalated_tickets": escalated_tickets,
        "is_churned": churn_flag
    })


def run_pipeline():
    print("Loading SaaS product telemetry...")
    df = generate_saas_telemetry(12000)
    print(f"Total Accounts: {len(df):,} | Baseline Churn Rate: {df['is_churned'].mean()*100:.2f}%\n")

    # One-hot encode categorical tier
    df_encoded = pd.get_dummies(df, columns=["plan_tier"], drop_first=True)

    features = [
        "contract_age_months", 
        "seat_utilization", 
        "active_days_l30", 
        "escalated_tickets",
        "plan_tier_Professional", 
        "plan_tier_Enterprise"
    ]
    
    X = df_encoded[features]
    y = df_encoded["is_churned"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    probs = clf.predict_proba(X_test)[:, 1]

    print("--- Model Performance ---")
    print(classification_report(y_test, preds, target_names=["Retained", "Churned"]))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, probs):.4f}")

    # Feature Importance for Product Managers
    importance = pd.Series(clf.feature_importances_, index=features).sort_values(ascending=False)
    print("\nTop Churn Drivers (Feature Importance):")
    for feat, imp in importance.items():
        print(f" - {feat:25s}: {imp*100:.1f}%")


if __name__ == "__main__":
    run_pipeline()