"""
FUTURE_DS_02: Customer Retention & Churn Analysis
Module: Data Preprocessing & Feature Engineering Pipeline
Author: Future Interns - Data Science & Analytics Track
"""

import os
import pandas as pd
import numpy as np


def clean_and_engineer_churn_data(raw_path: str, clean_path: str = None) -> pd.DataFrame:
    """
    Ingests raw customer churn data, cleans fields, derives retention cohorts,
    tenure brackets, risk scores, and customer lifetime value.
    """
    print(f"[*] Ingesting raw churn data from: {raw_path}")
    df = pd.read_csv(raw_path)

    # 1. Clean strings and formats
    categorical_cols = [
        'Gender', 'Partner', 'Dependents', 'Contract_Type',
        'PaperlessBilling', 'PaymentMethod', 'InternetService',
        'OnlineSecurity', 'TechSupport', 'StreamingServices', 'Churn', 'ChurnReason'
    ]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 2. Numeric validation & sanitization
    df['Tenure_Months'] = pd.to_numeric(df['Tenure_Months'], errors='coerce').fillna(1).astype(int)
    df['MonthlyCharges'] = pd.to_numeric(df['MonthlyCharges'], errors='coerce').fillna(0.0).round(2)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    # If total charges missing, impute from monthly charges * tenure
    df['TotalCharges'] = df['TotalCharges'].fillna(df['MonthlyCharges'] * df['Tenure_Months']).round(2)
    df['SupportTickets'] = pd.to_numeric(df['SupportTickets'], errors='coerce').fillna(0).astype(int)

    # 3. Churn binary flag
    df['Churn_Binary'] = (df['Churn'] == 'Yes').astype(int)

    # 4. Tenure brackets
    bins = [0, 6, 12, 24, 48, 72]
    labels = ['0-6 Months', '7-12 Months', '13-24 Months', '25-48 Months', '49-72 Months']
    df['Tenure_Bracket'] = pd.cut(df['Tenure_Months'], bins=bins, labels=labels, include_lowest=True)

    # 5. Cohort Date Parsing
    df['Signup_Date'] = pd.to_datetime(df['Signup_Date'], errors='coerce')
    df['Signup_YearMonth'] = df['Signup_Date'].dt.strftime('%Y-%m')
    df['Signup_Year'] = df['Signup_Date'].dt.year

    # 6. Customer Lifetime Value (CLV) Calculation
    # CLV = Total realized spend + estimated remaining expected value based on contract
    contract_factor = {'Month-to-Month': 3.0, 'One Year': 12.0, 'Two Year': 24.0}
    df['Estimated_Remaining_Months'] = np.where(
        df['Churn_Binary'] == 1,
        0,
        df['Contract_Type'].map(contract_factor).fillna(6.0)
    )
    df['Customer_Lifetime_Value'] = (df['TotalCharges'] + (df['MonthlyCharges'] * df['Estimated_Remaining_Months'])).round(2)

    # 7. Churn Risk Score Modeling (0 - 100)
    risk_score = np.zeros(len(df))
    # Month to month contract risk
    risk_score += np.where(df['Contract_Type'] == 'Month-to-Month', 35, 5)
    # Low tenure (<12 months)
    risk_score += np.where(df['Tenure_Months'] <= 6, 25, np.where(df['Tenure_Months'] <= 12, 15, 0))
    # Lack of tech support
    risk_score += np.where(df['TechSupport'] == 'No', 15, 0)
    # Electronic check
    risk_score += np.where(df['PaymentMethod'] == 'Electronic check', 10, 0)
    # Support tickets > 2
    risk_score += np.where(df['SupportTickets'] >= 3, 15, 0)
    df['Risk_Score'] = np.clip(risk_score, 0, 100).astype(int)

    # Risk Tier
    df['Risk_Tier'] = pd.cut(
        df['Risk_Score'],
        bins=[-1, 35, 65, 100],
        labels=['Low Risk', 'Moderate Risk', 'Critical Risk']
    )

    if clean_path:
        os.makedirs(os.path.dirname(clean_path), exist_ok=True)
        df.to_csv(clean_path, index=False)
        print(f"[+] Cleaned churn dataset exported to: {clean_path} ({len(df):,} records)")

    return df


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_csv = os.path.join(base_dir, 'data', 'raw_customer_churn_data.csv')
    clean_csv = os.path.join(base_dir, 'data', 'cleaned_customer_churn_data.csv')
    clean_and_engineer_churn_data(raw_csv, clean_csv)
