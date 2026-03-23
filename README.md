# Decision Intelligence Platform (Posture-Sensitive Prioritization Engine)

A deterministic decision intelligence platform that models how organizations prioritize initiatives under different strategic conditions while explicitly surfacing trade-offs, operational constraints, and decision confidence.

This system combines structured analytics, predictive modeling, optimization, and AI-assisted interpretation — while keeping decision logic fully auditable and human-controlled.

---

## 🔍 What This Tool Does

This platform transforms multi-factor signals into structured prioritization.

It does **not automate decisions**.  
Instead, it:

- Surfaces how rankings change under different strategic postures  
- Highlights trade-offs across competing priorities  
- Identifies operational bottlenecks and dependencies  
- Quantifies decision confidence  
- Provides structured executive-level interpretation  

---

## 🚀 Key Capabilities

- Strategy-based prioritization (Growth / Risk / Balanced)
- Strategy sensitivity detection (Posture Delta)
- Predictive risk scoring (logistic regression)
- Resource allocation optimization under constraints
- Operational bottleneck identification
- Dependency graph modeling (critical path visibility)
- Deterministic executive decision brief
- AI-based strategic interpretation (Groq Llama 3.1)

---

## 🧠 Why This Matters

Traditional dashboards show metrics.

This platform shows:

- How priorities shift under different strategies  
- Where decisions are sensitive and require judgment  
- Where execution bottlenecks may occur  
- How constraints affect optimal decisions  
- How to interpret results in an executive-friendly format  

It bridges the gap between **data visibility and decision-making**.

---

## 🏗 Architecture Overview

### 1. Signal Layer
- Growth Score  
- Stability Score  
- Diversification Score  
- Rollover Score  
- Risk Score (predictive)

### 2. Strategy Layer
- Growth_First  
- Risk_First  
- Balanced  

### 3. Decision Layer
- Dominant Strategy Detection  
- Decision Confidence Scoring  
- Strategy Sensitivity (Posture Delta)

### 4. Optimization Layer
- Resource allocation under constraints  
- Portfolio selection based on strategy  

### 5. Insight Layer
- Operational bottleneck mapping  
- Dependency graph modeling  

### 6. Interpretation Layer
- Deterministic executive decision brief  
- AI-generated strategic narrative  

---

## 🔒 Design Principle

The system separates deterministic decision modeling from AI interpretation.

- All prioritization logic is **deterministic and auditable**
- AI does **not influence or override decisions**
- AI is used only for **structured explanation**

This ensures strong governance and makes the system suitable for **high-stakes environments such as healthcare and operations**.

---

## 📊 Sample Outputs

### Ranking & Strategy Prioritization
![Ranking](ranking.png)

### Operational Bottleneck Identification
![Bottleneck](bottleneck.png)

### AI Strategic Interpretation
![AI Output](ai_output.png)

---

## ⚙️ Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn (Logistic Regression)
- Streamlit
- Matplotlib / Seaborn
- NetworkX
- PuLP (Optimization)
- Groq API (Llama 3.1 8B Instant)

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
