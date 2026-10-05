# FUTURE_DS_02: Customer Retention & Churn Analysis

[![Track: Data Science & Analytics](https://img.shields.io/badge/Track-Data%20Science%20%26%20Analytics-blue.svg)](https://futureinterns.com/)
[![Project: Task 02](https://img.shields.io/badge/Task-02%20Retention%20%26%20Churn-red.svg)](https://futureinterns.com/data-science-analytics-task-2-2026/)
[![Internship: Future Interns](https://img.shields.io/badge/Organization-Future%20Interns-orange.svg)](https://futureinterns.com/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)

---

## 📌 Executive Overview
Customer retention and churn modeling represent mission-critical business imperatives for subscription models, SaaS platforms, and telecommunications providers. In this data analytics project, a benchmark dataset of **7,043 subscriber accounts** was analyzed to diagnose attrition patterns, evaluate tenure hazard dynamics, quantify revenue at risk, and establish a data-driven retention roadmap.

---

## 📊 Core Performance Metrics (Executive Scorecard)

| Key Metric | Audited Figure | Strategic Assessment |
| :--- | :--- | :--- |
| **Total Tracked Accounts** | **7,043 Customers** | Full subscriber audit population |
| **Active Retained Customers** | **4,357 Customers (61.9%)** | Healthy ongoing core recurring cash flow |
| **Cumulative Churned Accounts** | **2,686 Customers (38.1%)** | Significant addressable revenue leakage |
| **Total Monthly Recurring Revenue (MRR)** | **\$460,230.00 / mo** | Baseline portfolio monthly billing |
| **Monthly Revenue Lost to Churn** | **\$197,840.00 / mo** | Direct annualized cash flow risk (\$2.37M) |
| **Average Account Tenure** | **22.8 Months** | Across subscriber lifecycles |
| **Average Customer Lifetime Value (CLV)** | **\$2,674.50** | Average lifetime monetization per customer |

---

## 🔍 Key Findings & Analytical Highlights

1. **Contract Structure Vulnerability:**
   - **Month-to-Month** contracts exhibit an alarming **53.4% churn rate**, generating over 77% of all total cancellations.
   - In contrast, **One-Year (21.2%)** and **Two-Year (11.8%)** contracts exhibit 2.5x to 4.5x greater retention stability.

2. **The 90-Day "Onboarding Cliff":**
   - Subscribers in their **first 6 months** suffer a **58.2% churn rate**.
   - Accounts crossing the 12-month milestone stabilize rapidly, dropping to **19.8% churn** by months 25–48.

3. **Protective Influence of Add-On Services:**
   - Subscribers equipped with **Tech Support** exhibit a **15.4% churn rate**, compared to **41.2%** for accounts without support.
   - **Online Security** provides a similar 65% reduction in churn probability.

4. **Pricing Sensitivity:**
   - Standalone unbundled accounts paying **\$70 – \$95/month** represent the highest churn density, driven by competitor price-matching pressures.

---

## 📁 Repository Structure

```text
FUTURE_DS_02/
├── dashboards/
│   ├── interactive_dashboard.html          # Executive web dashboard with interactive Chart.js
│   ├── customer_retention_workbook.xlsx    # Multi-tab styled Excel financial model
│   └── churn_metrics.json                  # Aggregated retention & risk KPI metrics
├── data/
│   ├── raw_customer_churn_data.csv         # Raw customer account & service records
│   └── cleaned_customer_churn_data.csv     # Cleaned, segmented & risk-scored dataset
├── notebooks/
│   └── customer_retention_analysis.ipynb   # Exploratory data analysis & statistical modeling
├── reports/
│   ├── retention_analysis_report.md        # C-suite executive strategic retention report
│   └── figures/
│       ├── 01_churn_distribution_and_kpis.png
│       ├── 02_churn_by_contract_type.png
│       ├── 03_tenure_cohort_survival_curve.png
│       ├── 04_monthly_charges_vs_churn_kde.png
│       ├── 05_top_churn_reasons_pareto.png
│       └── 06_tech_support_security_impact.png
├── src/
│   ├── data_preprocessing.py               # Feature engineering, risk scoring & cleaning
│   ├── retention_analytics.py              # Cohort and retention KPI calculations
│   ├── generate_visualizations.py          # Publication-ready visualizations
│   └── build_excel_dashboard.py            # Openpyxl multi-tab workbook builder
├── requirements.txt                        # Project dependencies
└── README.md                               # Project documentation & execution guide
```

---

## 🚀 Setup & Reproduction Guide

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/<your-username>/FUTURE_DS_02.git
cd FUTURE_DS_02
pip install -r requirements.txt
```

### 2. Run Data Cleaning & Analytics Pipeline
```bash
python src/data_preprocessing.py
python src/retention_analytics.py
python src/generate_visualizations.py
python src/build_excel_dashboard.py
```

### 3. View the Interactive Dashboard
Launch `dashboards/interactive_dashboard.html` in any web browser to explore interactive churn metrics, cohort survival curves, and strategic playbooks.

---

## 🎯 5-Point Strategic Churn Reduction Playbook
1. **Annual Plan Migration Incentive:** Convert Month-to-Month accounts with an attractive "Pay 10 Months, Get 2 Free" annual subscription.
2. **First 90-Day Onboarding Guarantee:** Deliver automated touchpoints at Day 14, 45, and 75 to navigate the highest-risk early attrition phase.
3. **Default Bundling of Tech Support:** Bundle 6 months of complimentary Tech Support on all fiber optic connections to cut churn by 60%.
4. **VIP Multi-Ticket Escalation:** Trigger immediate proactive outreach upon submission of a second customer support ticket within 30 days.

---
**Future Interns Data Science & Analytics Internship (2026)**  
Official Submission for Task 2: Customer Retention & Churn Analysis
