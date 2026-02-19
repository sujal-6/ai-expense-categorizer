import pandas as pd

def generate_summary(df: pd.DataFrame):

    required_columns = {"category", "amount", "date"}
    missing_cols = required_columns - set(df.columns)

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    df = df.copy()

    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop rows with invalid dates
    df = df.dropna(subset=["date"])

    # Category Summary
    summary = (df.groupby("category")["amount"].sum().reset_index().sort_values("amount", ascending=False))

    # Total spending
    total_spending = summary["amount"].sum()
    summary["percentage"] = ((summary["amount"] / total_spending) * 100 if total_spending > 0 else 0).round(2)

    # Categories with anomalies
    if "anomaly" in df.columns:
        anomaly_categories = df[df["anomaly"] == True]["category"].unique()
        summary["has_anomalies"] = summary["category"].isin(anomaly_categories)
    else:
        summary["has_anomalies"] = False

    # Monthly Trend
    df["month_year"] = df["date"].dt.to_period("M").astype(str)
    monthly_trend = (
        df.groupby("month_year")["amount"]
        .sum()
        .reset_index()
        .sort_values("month_year")
    )

    return summary, monthly_trend