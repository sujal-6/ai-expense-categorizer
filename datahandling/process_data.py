import pandas as pd
import re
from datetime import datetime

# List of date patterns and their corresponding formats
date_patterns = [
    (r"\d{4}-\d{2}-\d{2}", "%Y-%m-%d"),  # YYYY-MM-DD
    (r"\d{2}/\d{2}/\d{4}", "%d/%m/%Y"),  # DD/MM/YYYY
    (r"\d{2}-\d{2}-\d{4}", "%d-%m-%Y"),  # DD-MM-YYYY
    (r"\d{2}/\d{2}/\d{2}", "%d/%m/%y"),  # DD/MM/YY
]

def parse_date(date_str):
    if pd.isna(date_str):
        return pd.NaT
    
    date_str = str(date_str).strip()
    
    for pattern, fmt in date_patterns:
        if re.fullmatch(pattern, date_str):
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue
    try:
        return pd.to_datetime(date_str, errors="coerce")
    except:
        return pd.NaT

def process_data(df):
    # Handles data cleaning and preprocessing:
    # For required columns are present or not
    required_columns = ["date", "amount", "description"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Drop rows with missing required columns
    df = df.dropna(subset=["date", "amount", "description"])

    # For multiple formats
    df["date"] = df["date"].apply(parse_date)
    
    # Clean amount
    df["amount"] = df["amount"].replace({r'[\$,€,\s]': '', r',': ''}, regex=True)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    
    # Clean text
    df["description"] = df["description"].str.lower().str.strip()

    df = df.dropna()
    
    return df


