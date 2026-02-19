import pandas as pd
import numpy as np

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:

    required_columns = {"category", "amount", "date", "description"}
    missing_cols = required_columns - set(df.columns)

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    df = df.copy()

    # Initialize columns
    df["anomaly"] = False
    df["anomaly_reason"] = ""

    # Statistical Detection (Mean ± 2*Std)
    df["mean"] = df.groupby("category")["amount"].transform("mean")
    df["std"] = df.groupby("category")["amount"].transform("std").fillna(0)

    statistical_anomaly = (
        df["std"] > 0
    ) & (np.abs(df["amount"] - df["mean"]) > 2 * df["std"])

    # Out-of-pattern Spending (>50% deviation)
    deviation_anomaly = (
        (df["amount"] > df["mean"] * 1.5) |
        (df["amount"] < df["mean"] * 0.5)
    )

    # Duplicate Detection
    duplicate_anomaly = df.duplicated(
        subset=["date", "amount", "description"],
        keep=False
    )

    # Results
    df.loc[statistical_anomaly, "anomaly"] = True
    df.loc[statistical_anomaly, "anomaly_reason"] += "Statistical outlier; "

    df.loc[deviation_anomaly, "anomaly"] = True
    df.loc[deviation_anomaly, "anomaly_reason"] += "Out-of-pattern spending; "

    df.loc[duplicate_anomaly, "anomaly"] = True
    df.loc[duplicate_anomaly, "anomaly_reason"] += "Duplicate entry; "

    # Clean up helper columns
    df.drop(columns=["mean", "std"], inplace=True)

    # Remove trailing "; "
    df["anomaly_reason"] = df["anomaly_reason"].str.rstrip("; ")

    return df