import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# App Setup
st.set_page_config(page_title="Commercial Data Tool", layout="wide")
st.title("Data Visualization & Analysis Application")

# SPRINT 1: LOADING (US1 & US2)
uploaded_file = st.file_uploader("Upload your Commercial CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File Loaded!")
    st.write("### Data Preview", df.head(10)) # US1

    with st.expander("Validation Report"): # US2
        st.write("Missing Values:", df.isnull().sum())
        st.write("Duplicates:", df.duplicated().sum())

    # SPRINT 2: CLEANING & FILTERS (US3 & US4)
    if st.sidebar.button("Clean Data"): # US3
        df = df.drop_duplicates().fillna(0)
        st.sidebar.success("Cleaned!")

    # US8: Advanced Filtering
    cols = df.columns.tolist()
    filter_col = st.sidebar.selectbox("Filter by:", cols)
    vals = st.sidebar.multiselect("Select Values:", df[filter_col].unique())
    if vals:
        df = df[df[filter_col].isin(vals)]

    # SPRINT 4: KPI DASHBOARD (US7)
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    if num_cols:
        st.header("KPI Dashboard")
        c1, c2 = st.columns(2)
        c1.metric("Total Records", len(df))
        c2.metric(f"Sum of {num_cols[0]}", f"{df[num_cols[0]].sum():,.0f}")

    # SPRINT 3: VISUALS (US5 & US6)
    st.header("Visual Analytics")
    if len(num_cols) > 0:
        x = st.selectbox("X-Axis", cols)
        y = st.selectbox("Y-Axis", num_cols)
        fig, ax = plt.subplots()
        sns.barplot(data=df, x=x, y=y, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig) # US5

    # SPRINT 5: PDF (US10) & EXPORT (US9)
    if st.button("Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Commercial Report", ln=1, align='C')
        pdf.cell(200, 10, txt=f"Total Records: {len(df)}", ln=2)
        st.download_button("Download PDF", pdf.output(dest='S').encode('latin-1'), "report.pdf")

    st.download_button("Export CSV", df.to_csv(index=False), "data.csv")
