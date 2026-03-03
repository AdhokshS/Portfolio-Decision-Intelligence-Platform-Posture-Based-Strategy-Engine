import pandas as pd
import numpy as np

df = pd.read_csv("synthetic_portfolio_data.csv")
df["Month"] = pd.to_datetime(df["Month"])
df["Lease_Expiry_Date"] = pd.to_datetime(df["Lease_Expiry_Date"])

today = pd.Timestamp("2024-01-01")
one_year_later = today + pd.DateOffset(months=12)

property_monthly = (
    df.groupby(["Property_ID", "Month"])["Monthly_Rent"]
    .sum()
    .reset_index()
)

results = []

for property_id in property_monthly["Property_ID"].unique():
    
    property_data = property_monthly[property_monthly["Property_ID"] == property_id]
    property_data = property_data.sort_values("Month")
    
    first_value = property_data.iloc[0]["Monthly_Rent"]
    last_value = property_data.iloc[-1]["Monthly_Rent"]
    
    total_growth = (last_value - first_value) / first_value
    property_data["pct_change"] = property_data["Monthly_Rent"].pct_change()
    volatility = property_data["pct_change"].std()
    
    results.append({
        "Property_ID": property_id,
        "Total_Growth": total_growth,
        "Volatility": volatility
    })

metrics_df = pd.DataFrame(results)

latest_month = df["Month"].max()
latest_data = df[df["Month"] == latest_month]

hhi_results = []
rollover_results = []

for property_id in latest_data["Property_ID"].unique():
    
    property_tenants = latest_data[latest_data["Property_ID"] == property_id]
    total_rent = property_tenants["Monthly_Rent"].sum()
    
    shares = property_tenants["Monthly_Rent"] / total_rent
    hhi = (shares ** 2).sum()
    
    expiring_rent = property_tenants[
        property_tenants["Lease_Expiry_Date"] <= one_year_later
    ]["Monthly_Rent"].sum()
    
    rollover_exposure = expiring_rent / total_rent
    
    hhi_results.append({
        "Property_ID": property_id,
        "HHI_Concentration": hhi
    })
    
    rollover_results.append({
        "Property_ID": property_id,
        "Rollover_Exposure": rollover_exposure
    })

hhi_df = pd.DataFrame(hhi_results)
rollover_df = pd.DataFrame(rollover_results)

final_metrics = (
    metrics_df
    .merge(hhi_df, on="Property_ID")
    .merge(rollover_df, on="Property_ID")
)

def min_max_scale(series, inverse=False):
    min_val = series.min()
    max_val = series.max()
    scaled = (series - min_val) / (max_val - min_val)
    if inverse:
        scaled = 1 - scaled
    return scaled * 100

final_metrics["Growth_Score"] = min_max_scale(final_metrics["Total_Growth"])
final_metrics["Stability_Score"] = min_max_scale(final_metrics["Volatility"], inverse=True)
final_metrics["Diversification_Score"] = min_max_scale(final_metrics["HHI_Concentration"], inverse=True)
final_metrics["Rollover_Score"] = min_max_scale(final_metrics["Rollover_Exposure"], inverse=True)

# Strategy Scores
final_metrics["Growth_First"] = (
    0.50 * final_metrics["Growth_Score"] +
    0.20 * final_metrics["Stability_Score"] +
    0.15 * final_metrics["Diversification_Score"] +
    0.15 * final_metrics["Rollover_Score"]
)

final_metrics["Risk_First"] = (
    0.10 * final_metrics["Growth_Score"] +
    0.35 * final_metrics["Stability_Score"] +
    0.30 * final_metrics["Diversification_Score"] +
    0.25 * final_metrics["Rollover_Score"]
)

final_metrics["Balanced"] = (
    0.25 * final_metrics["Growth_Score"] +
    0.25 * final_metrics["Stability_Score"] +
    0.25 * final_metrics["Diversification_Score"] +
    0.25 * final_metrics["Rollover_Score"]
)

# Dominance + Confidence
def analyze_strategy(row):
    scores = {
        "Growth_First": row["Growth_First"],
        "Risk_First": row["Risk_First"],
        "Balanced": row["Balanced"]
    }
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    top_strategy, top_score = sorted_scores[0]
    second_strategy, second_score = sorted_scores[1]
    
    confidence_gap = top_score - second_score
    
    if confidence_gap > 15:
        confidence = "High Confidence"
    elif confidence_gap > 5:
        confidence = "Moderate Confidence"
    else:
        confidence = "Low Confidence"
    
    return pd.Series([top_strategy, confidence])

final_metrics[["Dominant_Strategy", "Decision_Confidence"]] = final_metrics.apply(analyze_strategy, axis=1)

print(final_metrics[[
    "Property_ID",
    "Dominant_Strategy",
    "Decision_Confidence"
]].sort_values("Property_ID"))

final_metrics.to_csv("final_metrics.csv", index=False)