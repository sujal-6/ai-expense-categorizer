import streamlit as st
import pandas as pd
import os
from datetime import datetime
from datahandling.process_data import process_data
from categorization.categorizer import categorize_expenses
from anomalydetection.anomaly_detection import detect_anomalies
from reports.reports import generate_summary

# Create data folder if not exists
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

st.set_page_config(page_title="AI Expense Categorizer", layout="wide")
st.title("AI Expense Categorizer")

# Error handling for encoding
def load_csv(file_path):
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="ISO-8859-1")
    return df

# For handling file upload
def handle_file_upload(file):
    if file is None:
        st.error("No file uploaded. Please upload a valid CSV file.")
        return None, None

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.name}"
        file_path = os.path.join(DATA_FOLDER, filename)

        # Save uploaded file
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        st.success(f"File saved successfully: {filename}")

        df = load_csv(file_path)

        return df, filename
    
    except ValueError as e:
        st.error(f"Error: {e}")
        return None, None

    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None, None

file = st.file_uploader("Upload Expense CSV", type=["csv"])

if file is not None:

    df, filename = handle_file_upload(file)

    if df is not None:

        st.subheader("Raw Data")
        st.dataframe(df)

        # Custom Categories Input
        editable_categories = st.text_input("Enter categories (comma separated)",value="Travel, Meals, Software, Utilities, Other")
        categories_list = [cat.strip() for cat in editable_categories.split(",") if cat.strip()]

        # Data processing
        df = process_data(df)
        # Categorization
        df = categorize_expenses(df, categories_list)
        # For Anmaly detection
        df = detect_anomalies(df)

        processed_filename = f"processed_{filename}"
        processed_path = os.path.join(DATA_FOLDER, processed_filename)
        df.to_csv(processed_path, index=False)
        st.success(f"Processed file saved as: {processed_filename}")

        # Summary
        summary, monthly_trend = generate_summary(df)

        # Display category summary
        st.subheader("Category Summary")
        st.dataframe(summary)

        # Display monthly trend
        if not monthly_trend.empty:
            st.subheader("Monthly Trend")
            st.line_chart(monthly_trend.set_index("month_year")["amount"])
        else:
            st.warning("No data available to display monthly trend.")

        # Full transactions in expander
        with st.expander("Show All Categorized Expenses"):
            st.dataframe(df)