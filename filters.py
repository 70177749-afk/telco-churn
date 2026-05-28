"""
filters.py — Filter and data processing functions for Telco Churn Dashboard
"""

import pandas as pd
import numpy as np


DATA_PATH = "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"


def load_data() -> pd.DataFrame:
    """Load and clean the Telco Customer Churn dataset."""
    df = pd.read_csv(DATA_PATH)

    # Clean TotalCharges (some blanks exist)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

    # Encode SeniorCitizen as readable label
    df["SeniorCitizenLabel"] = df["SeniorCitizen"].map({0: "Non-Senior", 1: "Senior"})

    # Tenure groups for line/area charts
    bins = [0, 12, 24, 36, 48, 60, 72]
    labels = ["0-12 mo", "13-24 mo", "25-36 mo", "37-48 mo", "49-60 mo", "61-72 mo"]
    df["TenureGroup"] = pd.cut(df["tenure"], bins=bins, labels=labels, include_lowest=True)

    return df


def apply_filters(
    df: pd.DataFrame,
    gender: list,
    contract: list,
    internet_service: list,
    senior: list,
    tenure_range: tuple,
    monthly_range: tuple,
    search_text: str,
) -> pd.DataFrame:
    """Apply all sidebar filters to the dataframe and return filtered copy."""
    filtered = df.copy()

    if gender:
        filtered = filtered[filtered["gender"].isin(gender)]
    if contract:
        filtered = filtered[filtered["Contract"].isin(contract)]
    if internet_service:
        filtered = filtered[filtered["InternetService"].isin(internet_service)]
    if senior:
        filtered = filtered[filtered["SeniorCitizenLabel"].isin(senior)]

    filtered = filtered[
        (filtered["tenure"] >= tenure_range[0]) & (filtered["tenure"] <= tenure_range[1])
    ]
    filtered = filtered[
        (filtered["MonthlyCharges"] >= monthly_range[0])
        & (filtered["MonthlyCharges"] <= monthly_range[1])
    ]

    if search_text:
        mask = filtered.apply(
            lambda row: row.astype(str).str.contains(search_text, case=False).any(), axis=1
        )
        filtered = filtered[mask]

    return filtered


def compute_kpis(df: pd.DataFrame) -> dict:
    """Return key performance indicators from (filtered) dataframe."""
    total = len(df)
    churned = (df["Churn"] == "Yes").sum()
    churn_rate = churned / total * 100 if total else 0
    avg_monthly = df["MonthlyCharges"].mean() if total else 0
    avg_tenure = df["tenure"].mean() if total else 0
    avg_total = df["TotalCharges"].mean() if total else 0

    return {
        "Total Customers": total,
        "Churned": churned,
        "Churn Rate (%)": round(churn_rate, 2),
        "Avg Monthly Charges ($)": round(avg_monthly, 2),
        "Avg Tenure (months)": round(avg_tenure, 1),
        "Avg Total Charges ($)": round(avg_total, 2),
    }
