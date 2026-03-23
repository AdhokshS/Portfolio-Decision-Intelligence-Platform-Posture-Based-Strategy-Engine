import pandas as pd
from sklearn.linear_model import LogisticRegression


def generate_risk_scores(metrics_df):

    # Features used for predictive model
    features = metrics_df[
        ["Growth_Score", "Stability_Score", "Diversification_Score", "Rollover_Score"]
    ]

    # Synthetic risk label (for demonstration)
    risk_flag = (metrics_df["Rollover_Score"] < 40).astype(int)

    model = LogisticRegression()
    model.fit(features, risk_flag)

    risk_probability = model.predict_proba(features)[:, 1]

    metrics_df["Risk_Probability"] = risk_probability
    metrics_df["Risk_Score"] = (1 - risk_probability) * 100

    return metrics_df