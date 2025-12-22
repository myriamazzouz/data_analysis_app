import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Commercial Data Tool", layout="wide")

st.title(" Data Visualization & Analysis Application")
st.markdown("---")

# --- SPRINT 1: DATA LOADING & VALIDATION ---
st.header("Step 1: Data Loading (US1 & US2)")
uploaded_file = st.file_uploader("Upload your Commercial CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File successfully loaded!")
    
    # Show Data Table
    st.subheader("Raw Data Preview")
    st.dataframe(df.head(10))

    # Validation Report
    with st.expander("Show Data Validation Report"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Missing Values:**")
            st.write(df.isnull().sum())
        with col2:
            st.write("**Duplicate Rows:**")
            st.write(df.duplicated().sum())

    # --- SPRINT 2: CLEANING & TRANSFORMATION ---
    st.markdown("---")
    st.header("Step 2: Cleaning & Filtering (US3 & US4)")
    
    col_clean, col_filter = st.columns(2)
    
    with col_clean:
        if st.button("🧹 Run Auto-Clean"):
            df = df.drop_duplicates()
            # Fill numbers with average, text with 'N/A'
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].fillna('N/A')
                else:
                    df[col] = df[col].fillna(df[col].mean())
            st.success("Data Standardized!")
    
    with col_filter:
        columns = df.columns.tolist()
        select_col = st.selectbox("Filter results by column:", columns)
        unique_vals = df[select_col].unique()
        selected_vals = st.multiselect(f"Select values for {select_col}:", unique_vals)
        
        if selected_vals:
            df = df[df[select_col].isin(selected_vals)]

    # --- SPRINT 3: VISUALIZATION ---
    st.markdown("---")
    st.header("Step 3: Visual Analytics (US5, US6, US7)")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) >= 1:
        chart_type = st.radio("Select Chart Type:", ["Bar Chart", "Line Chart", "Scatter Plot"])
        x_axis = st.selectbox("Select X-Axis:", columns)
        y_axis = st.selectbox("Select Y-Axis:", numeric_cols)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        if chart_type == "Bar Chart":
            sns.barplot(data=df, x=x_axis, y=y_axis, ax=ax)
        elif chart_type == "Line Chart":
            sns.lineplot(data=df, x=x_axis, y=y_axis, ax=ax)
        else:
            sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
            
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("Please upload a file with numeric data to see charts.")

else:
    st.info("Please upload a CSV file to begin.")
