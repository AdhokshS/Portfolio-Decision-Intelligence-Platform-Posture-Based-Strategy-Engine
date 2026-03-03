import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(layout="wide")

# -------------------------
# Header
# -------------------------

st.title("Portfolio Decision Intelligence Engine")

st.markdown("""
### What This Tool Does

This engine transforms multi-factor asset signals into posture-sensitive prioritization.

It does **not automate decisions**.  
It surfaces how rankings change under different strategic postures and highlights where managerial judgment is required.

Core Layers:
- Deterministic signal scoring
- Strategy-sensitive ranking
- Explicit decision confidence
- AI-assisted executive interpretation
""")

# -------------------------
# Load Data
# -------------------------

df = pd.read_csv("final_metrics.csv")

# -------------------------
# Strategy Selection
# -------------------------

strategy = st.selectbox(
    "Select Strategic Posture",
    ["Growth_First", "Risk_First", "Balanced"]
)

st.subheader(f"Ranking Under {strategy.replace('_', ' ')} Strategy")

ranked_df = df.sort_values(strategy, ascending=False).reset_index(drop=True)
ranked_df["Rank"] = ranked_df.index + 1

# Highlight Top 3
def highlight_top(row):
    if row["Rank"] <= 3:
        return ["background-color: #1f77b4; color: white"] * len(row)
    else:
        return [""] * len(row)

display_columns = [
    "Rank",
    "Property_ID",
    "Growth_First",
    "Risk_First",
    "Balanced",
    "Dominant_Strategy",
    "Decision_Confidence"
]

styled_df = ranked_df[display_columns].style.apply(highlight_top, axis=1)

st.dataframe(styled_df, width="stretch")

# -------------------------
# Strategy Sensitivity Snapshot
# -------------------------

st.markdown("### Strategy Sensitivity Snapshot")

# Top 3 assets under selected posture
top_assets = ranked_df.head(3)["Property_ID"].tolist()

# Posture sensitivity calculation
df["Posture_Delta"] = df[["Growth_First", "Risk_First", "Balanced"]].max(axis=1) - \
                      df[["Growth_First", "Risk_First", "Balanced"]].min(axis=1)

sensitive_assets = df.sort_values("Posture_Delta", ascending=False).head(3)["Property_ID"].tolist()

# Low confidence assets
low_conf_assets = df[df["Decision_Confidence"] == "Low Confidence"]["Property_ID"].tolist()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Top 3 Under Current Posture**")
    for asset in top_assets:
        st.markdown(f"- {asset}")

with col2:
    st.markdown("**Highly Posture-Sensitive Assets**")
    for asset in sensitive_assets:
        st.markdown(f"- {asset}")

with col3:
    st.markdown("**Low Confidence Assets**")
    if low_conf_assets:
        for asset in low_conf_assets:
            st.markdown(f"- {asset}")
    else:
        st.markdown("None")

st.markdown("---")

# -------------------------
# Signal Breakdown
# -------------------------

st.subheader("Signal Score Breakdown")

signal_cols = [
    "Property_ID",
    "Growth_Score",
    "Stability_Score",
    "Diversification_Score",
    "Rollover_Score"
]

st.dataframe(df[signal_cols], width="stretch")

st.markdown("---")

# -------------------------
# AI Interpretation Layer
# -------------------------

st.subheader("AI Strategic Interpretation")

if st.button("Generate AI Strategic Brief"):

    try:
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")

        if not GROQ_API_KEY:
            st.warning("Groq API key not found. Please set environment variable.")
        else:

            # Compact portfolio summary for model
            summary_rows = []
            for _, row in df.iterrows():
                summary_rows.append(
                    f"{row['Property_ID']} | "
                    f"G:{round(row['Growth_Score'],1)} | "
                    f"S:{round(row['Stability_Score'],1)} | "
                    f"D:{round(row['Diversification_Score'],1)} | "
                    f"R:{round(row['Rollover_Score'],1)} | "
                    f"GF:{round(row['Growth_First'],1)} | "
                    f"RF:{round(row['Risk_First'],1)} | "
                    f"B:{round(row['Balanced'],1)} | "
                    f"Dom:{row['Dominant_Strategy']} | "
                    f"Conf:{row['Decision_Confidence']}"
                )

            portfolio_summary = "\n".join(summary_rows)

            prompt = f"""
You are a senior portfolio strategy analyst.

Use ONLY the structured scores provided below.

Metric Definitions:
G = Growth_Score
S = Stability_Score
D = Diversification_Score
R = Rollover_Score
GF = Growth_First score
RF = Risk_First score
B = Balanced score
Dom = Dominant_Strategy
Conf = Decision_Confidence

Strict Rules:
- Do NOT reinterpret abbreviations.
- Do NOT invent or rename metrics.
- Do NOT expand abbreviations into new financial terms.
- Do NOT recompute any values.
- Do NOT introduce external assumptions.
- Focus on ranking shifts, posture sensitivity, and decision implications.
- Avoid unnecessary repetition of numeric ranges.
- Write in executive tone, not mechanical repetition.

Selected Strategy: {strategy}

Return output in this structure:

## Executive Scan Summary
• 5–7 concise bullets explaining posture sensitivity and top asset shifts.

## Detailed Strategic Interpretation

### {strategy.replace('_', ' ')} Posture View
Explain why the top 3 ranked assets surface under this posture.

### Cross-Strategy Sensitivity
Explain where rankings materially change under alternative postures.

### Strategy Convergence & Low Confidence
Identify Low Confidence assets and explain implications.

### Governance Implications
Explain where managerial judgment is required beyond numeric scoring.

Portfolio Data:
{portfolio_summary}
"""

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Be structured, concise, analytical, and governance-focused."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.2
                }
            )

            result = response.json()

            if "choices" in result:
                ai_output = result["choices"][0]["message"]["content"]

                st.markdown("---")
                st.markdown("## Executive AI Interpretation")
                st.markdown(ai_output)
            else:
                st.error("AI response error.")
                st.write(result)

    except Exception as e:
        st.error(f"AI layer failed: {e}")
        st.info("Core deterministic engine remains fully functional.")