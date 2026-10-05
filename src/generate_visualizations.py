"""
FUTURE_DS_02: Customer Retention & Churn Analysis
Module: Visualization Generator for Churn & Retention Analytics
Author: Future Interns - Data Science & Analytics Track
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8


def generate_all_figures(clean_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(clean_path)

    # 1. Churn Distribution (Donut Chart)
    plt.figure(figsize=(8, 6))
    churn_counts = df['Churn'].value_counts()
    colors = ['#10B981', '#EF4444']
    labels = [f"Retained ({churn_counts['No']:,} | {churn_counts['No']/len(df)*100:.1f}%)",
              f"Churned ({churn_counts['Yes']:,} | {churn_counts['Yes']/len(df)*100:.1f}%)"]
    plt.pie(churn_counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90,
            wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
            textprops={'fontsize': 11, 'fontweight': 'bold'})
    plt.title('Customer Retention vs Churn Distribution', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '01_churn_distribution_and_kpis.png'), dpi=300)
    plt.close()

    # 2. Churn by Contract Type
    plt.figure(figsize=(9, 5))
    ct = df.groupby('Contract_Type')['Churn_Binary'].mean() * 100
    ct = ct.sort_values(ascending=False)
    bars = plt.bar(ct.index, ct.values, color=['#EF4444', '#F59E0B', '#10B981'], edgecolor='#333333', width=0.55)
    plt.title('Churn Rate by Contract Commitment Type (%)', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('Churn Rate Percentage (%)', fontsize=11)
    plt.ylim(0, max(ct.values) * 1.2)
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, h + 1.5, f'{h:.1f}%', ha='center', fontweight='bold', fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '02_churn_by_contract_type.png'), dpi=300)
    plt.close()

    # 3. Tenure Survival Curve
    plt.figure(figsize=(11, 5))
    tenure_retention = []
    max_t = int(df['Tenure_Months'].max())
    for t in range(1, max_t + 1):
        at_risk = df[df['Tenure_Months'] >= t]
        if len(at_risk) > 0:
            retained = at_risk['Churn_Binary'].eq(0).mean() * 100
            tenure_retention.append((t, retained))
    tr_df = pd.DataFrame(tenure_retention, columns=['Tenure', 'Retention_Rate'])
    plt.plot(tr_df['Tenure'], tr_df['Retention_Rate'], color='#2563EB', linewidth=2.8, label='Empirical Cohort Retention')
    plt.axvline(12, color='#EF4444', linestyle='--', label='12-Month Mark (Critical Drop-Off Zone)')
    plt.fill_between(tr_df['Tenure'], 0, tr_df['Retention_Rate'], color='#DBEAFE', alpha=0.4)
    plt.title('Customer Retention Survival Curve by Tenure (Months)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Customer Tenure in Months', fontsize=11)
    plt.ylabel('Retention Percentage (%)', fontsize=11)
    plt.ylim(0, 105)
    plt.legend(frameon=True, facecolor='white')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '03_tenure_cohort_survival_curve.png'), dpi=300)
    plt.close()

    # 4. Monthly Charges Distribution (KDE)
    plt.figure(figsize=(10, 5))
    sns.kdeplot(df[df['Churn'] == 'No']['MonthlyCharges'], fill=True, color='#10B981', label='Retained Customers', alpha=0.4, linewidth=2)
    sns.kdeplot(df[df['Churn'] == 'Yes']['MonthlyCharges'], fill=True, color='#EF4444', label='Churned Customers', alpha=0.4, linewidth=2)
    plt.title('Distribution of Monthly Recurring Charges: Retained vs Churned', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Monthly Charges ($ USD)', fontsize=11)
    plt.ylabel('Density', fontsize=11)
    plt.legend(frameon=True, facecolor='white')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_monthly_charges_vs_churn_kde.png'), dpi=300)
    plt.close()

    # 5. Top Churn Reasons (Pareto Bar)
    plt.figure(figsize=(11, 5))
    churned_df = df[df['Churn'] == 'Yes']
    reasons = churned_df['ChurnReason'].value_counts()
    bars = plt.barh(reasons.index[::-1], reasons.values[::-1], color='#F87171', edgecolor='#991B1B')
    plt.title('Primary Exit Reasons for Churned Accounts', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Customer Cancellations', fontsize=11)
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 10, bar.get_y() + bar.get_height() / 2, f'{w:,}', va='center', fontweight='bold', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '05_top_churn_reasons_pareto.png'), dpi=300)
    plt.close()

    # 6. Tech Support & Security Impact on Retention
    plt.figure(figsize=(10, 5))
    support_churn = df.groupby('TechSupport')['Churn_Binary'].mean() * 100
    security_churn = df.groupby('OnlineSecurity')['Churn_Binary'].mean() * 100
    labels = ['No Add-On', 'Has Add-On', 'No Internet']
    # Align order
    support_vals = [support_churn.get('No', 0), support_churn.get('Yes', 0), support_churn.get('No internet service', 0)]
    security_vals = [security_churn.get('No', 0), security_churn.get('Yes', 0), security_churn.get('No internet service', 0)]
    x = np.arange(len(labels))
    width = 0.35
    plt.bar(x - width/2, support_vals, width, label='Tech Support', color='#3B82F6')
    plt.bar(x + width/2, security_vals, width, label='Online Security', color='#8B5CF6')
    plt.xticks(x, labels, fontsize=11)
    plt.ylabel('Churn Rate (%)', fontsize=11)
    plt.title('Protective Influence of Add-On Support Services on Churn', fontsize=14, fontweight='bold', pad=15)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '06_tech_support_security_impact.png'), dpi=300)
    plt.close()

    print(f"[+] All 6 figures generated successfully in: {output_dir}")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_csv = os.path.join(base_dir, 'data', 'cleaned_customer_churn_data.csv')
    fig_dir = os.path.join(base_dir, 'reports', 'figures')
    generate_all_figures(clean_csv, fig_dir)
