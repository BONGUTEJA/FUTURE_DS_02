"""
FUTURE_DS_02: Customer Retention & Churn Analysis
Module: Retention Analytics Engine & Metric Aggregations
Author: Future Interns - Data Science & Analytics Track
"""

import os
import json
import pandas as pd
import numpy as np


class RetentionAnalyticsEngine:
    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)

    def compute_executive_kpis(self) -> dict:
        """Computes top-level subscription and retention KPIs."""
        total_customers = int(len(self.df))
        churned_customers = int(self.df['Churn_Binary'].sum())
        retained_customers = total_customers - churned_customers
        churn_rate = round((churned_customers / total_customers) * 100, 2)
        retention_rate = round(100.0 - churn_rate, 2)

        avg_tenure = round(float(self.df['Tenure_Months'].mean()), 1)
        avg_monthly_charges = round(float(self.df['MonthlyCharges'].mean()), 2)
        total_mrr = round(float(self.df['MonthlyCharges'].sum()), 2)
        mrr_at_risk = round(float(self.df[self.df['Churn_Binary'] == 1]['MonthlyCharges'].sum()), 2)
        avg_clv = round(float(self.df['Customer_Lifetime_Value'].mean()), 2)

        return {
            "total_customers": total_customers,
            "retained_customers": retained_customers,
            "churned_customers": churned_customers,
            "churn_rate_pct": churn_rate,
            "retention_rate_pct": retention_rate,
            "avg_tenure_months": avg_tenure,
            "avg_monthly_charges": avg_monthly_charges,
            "total_mrr": total_mrr,
            "mrr_lost_to_churn": mrr_at_risk,
            "avg_clv": avg_clv
        }

    def analyze_churn_by_contract(self) -> pd.DataFrame:
        """Analyzes churn rates across Contract types."""
        ct = self.df.groupby('Contract_Type').agg(
            Total=('CustomerID', 'count'),
            Churned=('Churn_Binary', 'sum'),
            Avg_Monthly_Charges=('MonthlyCharges', 'mean'),
            Avg_Tenure=('Tenure_Months', 'mean')
        ).reset_index()
        ct['Churn_Rate_Pct'] = ((ct['Churned'] / ct['Total']) * 100).round(2)
        ct['Avg_Monthly_Charges'] = ct['Avg_Monthly_Charges'].round(2)
        ct['Avg_Tenure'] = ct['Avg_Tenure'].round(1)
        return ct.sort_values('Churn_Rate_Pct', ascending=False)

    def analyze_tenure_brackets(self) -> pd.DataFrame:
        """Evaluates customer attrition across tenure cohorts."""
        tb = self.df.groupby('Tenure_Bracket', observed=False).agg(
            Total=('CustomerID', 'count'),
            Churned=('Churn_Binary', 'sum'),
            Total_Revenue=('TotalCharges', 'sum')
        ).reset_index()
        tb['Churn_Rate_Pct'] = ((tb['Churned'] / tb['Total']) * 100).round(2)
        tb['Total_Revenue'] = tb['Total_Revenue'].round(2)
        return tb

    def analyze_service_features(self) -> pd.DataFrame:
        """Examines the impact of value-added support services on churn."""
        records = []
        for feat in ['TechSupport', 'OnlineSecurity', 'InternetService', 'PaymentMethod']:
            grouped = self.df.groupby(feat).agg(
                Total=('CustomerID', 'count'),
                Churned=('Churn_Binary', 'sum')
            ).reset_index()
            grouped['Feature'] = feat
            grouped.rename(columns={feat: 'Feature_Value'}, inplace=True)
            grouped['Churn_Rate_Pct'] = ((grouped['Churned'] / grouped['Total']) * 100).round(2)
            records.append(grouped)
        return pd.concat(records, ignore_index=True)

    def analyze_churn_reasons(self) -> pd.DataFrame:
        """Audits stated reasons for customer cancellations."""
        churned_df = self.df[self.df['Churn'] == 'Yes']
        reasons = churned_df['ChurnReason'].value_counts().reset_index()
        reasons.columns = ['Reason', 'Count']
        reasons['Share_Pct'] = ((reasons['Count'] / len(churned_df)) * 100).round(2)
        return reasons

    def export_metrics_json(self, output_path: str):
        """Dumps aggregated metrics to JSON for dashboards."""
        kpis = self.compute_executive_kpis()
        contract_df = self.analyze_churn_by_contract()
        tenure_df = self.analyze_tenure_brackets()
        reasons_df = self.analyze_churn_reasons()

        data = {
            **kpis,
            "contracts": contract_df['Contract_Type'].tolist(),
            "contract_totals": contract_df['Total'].tolist(),
            "contract_churn_rates": contract_df['Churn_Rate_Pct'].tolist(),
            "tenure_brackets": tenure_df['Tenure_Bracket'].astype(str).tolist(),
            "tenure_churn_rates": tenure_df['Churn_Rate_Pct'].tolist(),
            "tenure_totals": tenure_df['Total'].tolist(),
            "top_reasons": reasons_df['Reason'].tolist(),
            "top_reasons_count": reasons_df['Count'].tolist(),
            "top_reasons_share": reasons_df['Share_Pct'].tolist()
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"[+] Churn metrics exported to: {output_path}")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_csv = os.path.join(base_dir, 'data', 'cleaned_customer_churn_data.csv')
    json_path = os.path.join(base_dir, 'dashboards', 'churn_metrics.json')
    engine = RetentionAnalyticsEngine(clean_csv)
    engine.export_metrics_json(json_path)
