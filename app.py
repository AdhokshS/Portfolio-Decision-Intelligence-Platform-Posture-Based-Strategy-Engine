import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import requests
import os

from optimization_engine import optimize_portfolio
from decision_logger import log_decision

st.set_page_config(layout="wide")

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.title("Portfolio Decision Intelligence Engine")
st.caption(
"A deterministic decision intelligence platform that models how priorities change under different strategic postures."
)

st.markdown("""
### What This Tool Does

This engine transforms multi-factor asset signals into posture-sensitive prioritization.

It **does not automate decisions**.  
It highlights where **managerial judgment is required**.

Core Layers

• Deterministic signal scoring  
• Strategy-sensitive ranking  
• Decision confidence analysis  
• Operational bottleneck detection  
• Dependency modeling  
• Executive decision briefing  
• AI strategic interpretation
""")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

df = pd.read_csv("final_metrics.csv")

# ------------------------------------------------
# STRATEGY SELECTION
# ------------------------------------------------

strategy = st.selectbox(
"Select Strategic Posture",
["Growth_First","Risk_First","Balanced"]
)

# ------------------------------------------------
# SCENARIO SIMULATION
# ------------------------------------------------

st.markdown("### Strategy Scenario Simulation")

growth_weight = st.slider(
"Adjust Growth Weight (Growth Strategy Only)",
0.30,
0.70,
0.50,
0.05
)

# ------------------------------------------------
# RANKING LOGIC
# ------------------------------------------------

if strategy == "Growth_First":

    df["Scenario_Growth_First"] = (
        growth_weight * df["Growth_Score"] +
        0.20 * df["Stability_Score"] +
        0.15 * df["Diversification_Score"] +
        0.15 * df["Rollover_Score"]
    )

    ranking_column = "Scenario_Growth_First"

else:

    ranking_column = strategy

ranked_df = df.sort_values(
ranking_column,
ascending=False
).reset_index(drop=True)

ranked_df["Rank"] = ranked_df.index + 1

st.subheader(f"Ranking Under {strategy.replace('_',' ')} Strategy")

display_cols = [
"Rank",
"Property_ID",
"Growth_First",
"Risk_First",
"Balanced",
"Dominant_Strategy",
"Decision_Confidence"
]

st.dataframe(ranked_df[display_cols],use_container_width=True)

# ------------------------------------------------
# STRATEGY SENSITIVITY SNAPSHOT
# ------------------------------------------------

st.markdown("### Strategy Sensitivity Snapshot")

top_assets = ranked_df.head(3)["Property_ID"].tolist()

df["Posture_Delta"] = (
df[["Growth_First","Risk_First","Balanced"]].max(axis=1)
-
df[["Growth_First","Risk_First","Balanced"]].min(axis=1)
)

sensitive = df.sort_values(
"Posture_Delta",
ascending=False
).head(3)["Property_ID"].tolist()

low_conf = df[
df["Decision_Confidence"]=="Low Confidence"
]["Property_ID"].tolist()

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown("**Top 3 Under Current Strategy**")
    for a in top_assets:
        st.write(a)

with c2:
    st.markdown("**Highly Strategy Sensitive Assets**")
    for a in sensitive:
        st.write(a)

with c3:
    st.markdown("**Low Confidence Decisions**")
    for a in low_conf:
        st.write(a)

st.markdown("---")

# ------------------------------------------------
# STRATEGY HEATMAP
# ------------------------------------------------

st.subheader("Strategy Sensitivity Heatmap")

heatmap_df = df.set_index("Property_ID")[[
"Growth_First",
"Risk_First",
"Balanced"
]]

fig,ax = plt.subplots(figsize=(10,6))

sns.heatmap(
heatmap_df,
annot=True,
cmap="viridis",
linewidths=0.5,
ax=ax
)

ax.set_title("Strategy Score Comparison")

st.pyplot(fig)

# ------------------------------------------------
# OPERATIONAL BOTTLENECK MAP
# ------------------------------------------------

st.markdown("---")
st.subheader("Operational Bottleneck Map")

df["Operational_Complexity"] = 100 - df["Stability_Score"]
df["Strategic_Impact"] = df["Growth_Score"]

fig2,ax2 = plt.subplots(figsize=(8,6))

sns.scatterplot(
data=df,
x="Operational_Complexity",
y="Strategic_Impact",
s=120,
color="skyblue",
ax=ax2
)

for _,row in df.iterrows():

    ax2.text(
        row["Operational_Complexity"]+1,
        row["Strategic_Impact"]+1,
        row["Property_ID"],
        fontsize=9
    )

ax2.axhline(df["Strategic_Impact"].median(),linestyle="--")
ax2.axvline(df["Operational_Complexity"].median(),linestyle="--")

ax2.set_title("Strategic Impact vs Operational Complexity")
ax2.set_xlabel("Operational Complexity")
ax2.set_ylabel("Strategic Impact")

st.pyplot(fig2)

# ------------------------------------------------
# DEPENDENCY GRAPH
# ------------------------------------------------

st.markdown("---")
st.subheader("Strategic Initiative Dependencies")

st.caption(
"Arrow Direction: **Prerequisite → Dependent**  (Example: P03 → P01 means P01 depends on P03)"
)

G = nx.DiGraph()

dependencies = [
("P03","P01"),
("P04","P02"),
("P06","P03"),
("P07","P04"),
("P09","P05")
]

G.add_edges_from(dependencies)

fig3,ax3 = plt.subplots(figsize=(10,7))

pos = nx.spring_layout(G,k=1.5,seed=42)

nx.draw_networkx_nodes(G,pos,node_size=2500,node_color="lightblue",ax=ax3)
nx.draw_networkx_labels(G,pos,font_size=12,font_weight="bold",ax=ax3)
nx.draw_networkx_edges(G,pos,arrowstyle="->",arrowsize=20,width=2,ax=ax3)

edge_labels = {edge:"prerequisite" for edge in dependencies}

nx.draw_networkx_edge_labels(
G,pos,
edge_labels=edge_labels,
font_color="darkred",
font_size=10,
ax=ax3
)

ax3.set_title("Dependency Flow (Prerequisite → Dependent)")
ax3.axis("off")

st.pyplot(fig3)

# ------------------------------------------------
# SIGNAL BREAKDOWN
# ------------------------------------------------

st.markdown("---")
st.subheader("Signal Score Breakdown")

signal_cols = [
"Property_ID",
"Growth_Score",
"Stability_Score",
"Diversification_Score",
"Rollover_Score",
"Risk_Score"
]

st.dataframe(df[signal_cols],use_container_width=True)

# ------------------------------------------------
# RESOURCE OPTIMIZATION
# ------------------------------------------------

st.markdown("---")
st.subheader("Resource Allocation Optimization")

max_assets = st.slider(
"Maximum number of assets that can be prioritized",
1,
5,
3
)

if st.button("Run Optimization"):

    selected = optimize_portfolio(df,strategy,max_assets)

    log_decision(strategy,selected,growth_weight)

    st.markdown("### Optimal Asset Selection")

    for a in selected:
        st.write(a)

# ------------------------------------------------
# EXECUTIVE DECISION BRIEF
# ------------------------------------------------

st.markdown("---")
st.subheader("Executive Decision Intelligence Brief")

generate = st.button("Generate Executive Decision Brief")

if generate:

    bottlenecks = df.sort_values(
        "Operational_Complexity",
        ascending=False
    ).head(3)["Property_ID"].tolist()

    st.markdown("### Strategic Priorities")
    st.write(", ".join(top_assets))

    st.markdown("### Operational Bottlenecks")
    st.write(", ".join(bottlenecks))

    st.markdown("### Strategy Sensitive Assets")
    st.write(", ".join(sensitive))

    st.markdown("### Low Confidence Decisions")
    st.write(", ".join(low_conf))

    st.markdown("### Governance Insight")

    st.write("""
Portfolio prioritization indicates concentration around high-growth assets.

Several initiatives show elevated operational complexity which may delay execution timelines.

Strategy-sensitive assets require leadership review before final resource allocation.

Executives should monitor dependency chains to avoid execution bottlenecks.
""")

# ------------------------------------------------
# AI STRATEGIC INTERPRETATION
# ------------------------------------------------

st.markdown("---")
st.subheader("AI Executive Strategy Narrative")

generate_ai = st.button("Generate AI Strategic Brief")

if generate_ai:

    try:

        GROQ_API_KEY = os.getenv("GROQ_API_KEY")

        if not GROQ_API_KEY:
            st.error("GROQ_API_KEY not set in terminal.")
            st.stop()

        summary_rows = []

        for _,row in df.iterrows():

            summary_rows.append(
                f"{row['Property_ID']} | "
                f"G:{round(row['Growth_Score'],1)} | "
                f"S:{round(row['Stability_Score'],1)} | "
                f"D:{round(row['Diversification_Score'],1)} | "
                f"R:{round(row['Rollover_Score'],1)} | "
                f"Risk:{round(row['Risk_Score'],1)}"
            )

        portfolio_summary = "\n".join(summary_rows)

        prompt = f"""
You are a senior portfolio strategy analyst.

Strict Rules:
- Use ONLY the metrics provided.
- Do NOT invent new financial terms or metrics.
- Do NOT reinterpret abbreviations.
- Do NOT assume external financial data.

Selected Strategy: {strategy}

Top Priorities: {", ".join(top_assets)}
Strategy Sensitive Assets: {", ".join(sensitive)}
Low Confidence Decisions: {", ".join(low_conf)}

Portfolio Metrics:
{portfolio_summary}

Provide an executive interpretation covering:
- portfolio priorities
- risk exposure
- operational bottlenecks
- dependency implications
- governance recommendations
"""

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model":"llama-3.1-8b-instant",
                "messages":[
                    {"role":"system","content":"Be analytical and concise."},
                    {"role":"user","content":prompt}
                ],
                "temperature":0.2
            },
            timeout=20
        )

        result = response.json()

        if "choices" in result:

            ai_output = result["choices"][0]["message"]["content"]

            st.markdown("### AI Executive Strategy Analysis")
            st.markdown(ai_output)

        else:

            st.error("AI response failed.")
            st.write(result)

    except Exception as e:

        st.error(f"AI interpretation failed: {e}")
