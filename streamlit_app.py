import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# App Config
st.set_page_config(page_title="Commercial Data Tool", layout="wide")
st.title("Data Visualization & Analysis Application")

# --- SPRINT 1: LOADING & VALIDATION ---
st.header("Step 1: Data Loading & Validation (US1 & US2)")
uploaded_file = st.file_uploader("Upload your Commercial CSV file", type="csv")

if uploaded_file is not None:
    # Universal Loading Fix
    try:
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='latin-1')
        
    st.success("File successfully loaded!")
    st.write("### Data Preview", df.head(10))

    with st.expander("Show Data Validation Report"):
        st.write("**Missing Values:**", df.isnull().sum())
        st.write("**Duplicate Rows:**", df.duplicated().sum())

    # --- SPRINT 2: CLEANING & TRANSFORMATION ---
    st.divider()
    st.header("Step 2: Cleaning & Transformation (US3 & US4)")
    if st.button("🧼 Run Auto-Clean"):
        df = df.drop_duplicates().fillna(0)
        st.success("Data cleaned: Duplicates removed and missing values filled.")

    # Filtering Logic
    cols = df.columns.tolist()
    filter_col = st.selectbox("Select column to filter by:", cols)
    selected_vals = st.multiselect(f"Values in {filter_col}:", df[filter_col].unique())
    if selected_vals:
        df = df[df[filter_col].isin(selected_vals)]

    # --- SPRINT 4: KPI DASHBOARD ---
    st.divider()
    st.header("Step 3: KPI Dashboard (US7)")
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    if num_cols:
        kpi1, kpi2 = st.columns(2)
        kpi1.metric("Total Transactions", len(df))
        kpi2.metric(f"Total {num_cols[0]}", f"{df[num_cols[0]].sum():,.2f}")

    # --- SPRINT 3: VISUALIZATION ---
    st.header("Step 4: Visual Analytics (US5 & US6)")
    if len(num_cols) > 0:
        chart_type = st.radio("Choose Graph Type:", ["Bar", "Line", "Scatter"])
        x_axis = st.selectbox("X-Axis:", cols)
        y_axis = st.selectbox("Y-Axis:", num_cols)
        
        fig, ax = plt.subplots()
        if chart_type == "Bar": 
            sns.barplot(data=df, x=x_axis, y=y_axis, ax=ax)
        elif chart_type == "Line": 
            sns.lineplot(data=df, x=x_axis, y=y_axis, ax=ax)
        else: 
            sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # --- SPRINT 5: ANALYTICAL REPORT ---
    st.divider()
    st.header("Step 5: Export & Report (US9 & US10)")
    if st.button("Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Commercial Analysis Summary", ln=1, align='C')
        pdf.cell(200, 10, txt=f"Total Records: {len(df)}", ln=2)
        
        pdf_report = pdf.output(dest='S').encode('latin-1')
        st.download_button("Download PDF", pdf_report, "analysis_report.pdf", "application/pdf")

    st.download_button("Export Filtered Data (CSV)", df.to_csv(index=False), "filtered_data.csv", "text/csv")
else:
    st.info("Please upload a CSV file to begin.")
