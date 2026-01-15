import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# Initialize session state
if 'df' not in st.session_state:
    np.random.seed(42)
    n = 200
    dates = pd.date_range('2023-01-01', periods=n, freq='D')
    
    data = {
        'Date': dates,
        'Product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Monitor', 'Printer'], n),
        'Category': np.random.choice(['Electronics', 'Office', 'Accessories'], n),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], n),
        'Sales': np.random.randint(100, 5000, n),
        'Quantity': np.random.randint(1, 20, n),
        'Profit': np.random.randint(-100, 500, n)
    }
    
    st.session_state.df = pd.DataFrame(data)

# App config
st.set_page_config(page_title="Data Analysis App", layout="wide")

# Title
st.title("📊 Data Analysis Application")
st.markdown("**Agile Scrum Project | Team: MA, LJ, M, HZ**")
st.divider()

# Tabs for sprints
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📥 Sprint 1: Load & Validate",
    "🧹 Sprint 2: Clean & Transform", 
    "📈 Sprint 3: Visualize",
    "📊 Sprint 4: Dashboard",
    "📄 Sprint 5: Report"
])

# TAB 1: Load & Validate
with tab1:
    st.header("Data Loading & Validation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Preview")
        st.dataframe(st.session_state.df.head(10))
        st.write(f"**Total Rows:** {len(st.session_state.df)}")
    
    with col2:
        st.subheader("Validation Report")
        
        # Missing values
        missing = st.session_state.df.isnull().sum().sum()
        st.metric("Missing Values", missing)
        
        # Duplicates
        duplicates = st.session_state.df.duplicated().sum()
        st.metric("Duplicate Rows", duplicates)

# TAB 2: Clean & Transform
with tab2:
    st.header("Data Cleaning & Transformation")
    
    # Cleaning
    st.subheader("Cleaning Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Remove Duplicates", key="btn_dup"):
            before = len(st.session_state.df)
            st.session_state.df = st.session_state.df.drop_duplicates()
            after = len(st.session_state.df)
            st.success(f"Removed {before - after} duplicates!")
            st.rerun()
    
    with col2:
        if st.button("Fill Missing Values", key="btn_missing"):
            st.session_state.df = st.session_state.df.fillna(0)
            st.success("Missing values filled with 0!")
            st.rerun()
    
    # Filtering
    st.subheader("Filter Data")
    filter_col = st.selectbox("Filter by column:", st.session_state.df.columns, key="filter1")
    
    if filter_col:
        unique_vals = st.session_state.df[filter_col].unique()
        selected = st.multiselect("Select values:", unique_vals[:10], key="vals1")
        
        if selected:
            filtered = st.session_state.df[st.session_state.df[filter_col].isin(selected)]
            st.dataframe(filtered.head())
            st.write(f"**Filtered Rows:** {len(filtered)}")

# TAB 3: Visualize - FIXED GRAPHS
with tab3:
    st.header("Data Visualization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Chart Settings")
        
        # Chart type
        chart_type = st.selectbox(
            "Chart Type:", 
            ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"],
            key="chart_type_select"
        )
        
        # X-axis
        x_col = st.selectbox("X-axis:", st.session_state.df.columns, key="x_select")
        
        # Y-axis (for some charts)
        y_col = None
        if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot"]:
            num_cols = st.session_state.df.select_dtypes(include=[np.number]).columns
            if len(num_cols) > 0:
                y_col = st.selectbox("Y-axis:", num_cols, key="y_select")
        
        # Generate button
        if st.button("Generate Chart", type="primary", key="gen_chart"):
            st.session_state.chart_type = chart_type
            st.session_state.x_col = x_col
            st.session_state.y_col = y_col
            st.rerun()
    
    with col2:
        st.subheader("Chart Display")
        
        # Check if we have chart settings
        if hasattr(st.session_state, 'chart_type'):
            
            fig, ax = plt.subplots(figsize=(10, 5))
            
            try:
                if st.session_state.chart_type == "Bar Chart" and st.session_state.y_col:
                    # Group data for bar chart
                    bar_data = st.session_state.df.groupby(st.session_state.x_col)[st.session_state.y_col].mean()
                    bar_data.plot(kind='bar', ax=ax, color='skyblue')
                    ax.set_ylabel(st.session_state.y_col)
                    ax.set_title(f"Average {st.session_state.y_col} by {st.session_state.x_col}")
                
                elif st.session_state.chart_type == "Line Chart" and st.session_state.y_col:
                    line_data = st.session_state.df.groupby(st.session_state.x_col)[st.session_state.y_col].mean()
                    line_data.plot(kind='line', ax=ax, marker='o', color='green')
                    ax.set_ylabel(st.session_state.y_col)
                    ax.set_title(f"Average {st.session_state.y_col} by {st.session_state.x_col}")
                
                elif st.session_state.chart_type == "Scatter Plot" and st.session_state.y_col:
                    ax.scatter(st.session_state.df[st.session_state.x_col], 
                              st.session_state.df[st.session_state.y_col], 
                              alpha=0.5)
                    ax.set_xlabel(st.session_state.x_col)
                    ax.set_ylabel(st.session_state.y_col)
                    ax.set_title(f"{st.session_state.y_col} vs {st.session_state.x_col}")
                
                elif st.session_state.chart_type == "Histogram":
                    st.session_state.df[st.session_state.x_col].hist(ax=ax, bins=20, color='purple')
                    ax.set_xlabel(st.session_state.x_col)
                    ax.set_ylabel('Frequency')
                    ax.set_title(f"Histogram of {st.session_state.x_col}")
                
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                
                # Download button for chart
                buf = io.BytesIO()
                fig.savefig(buf, format="png", dpi=100)
                buf.seek(0)
                
                st.download_button(
                    label="📥 Download Chart",
                    data=buf,
                    file_name="chart.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.error(f"Error creating chart: {str(e)}")
        else:
            st.info("👈 Select chart settings and click 'Generate Chart'")

# TAB 4: Dashboard
with tab4:
    st.header("KPI Dashboard & Export")
    
    # KPIs
    st.subheader("Key Performance Indicators")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.metric("Total Sales", f"${st.session_state.df['Sales'].sum():,}")
    
    with kpi2:
        st.metric("Avg Profit", f"${st.session_state.df['Profit'].mean():.2f}")
    
    with kpi3:
        st.metric("Total Quantity", st.session_state.df['Quantity'].sum())
    
    with kpi4:
        st.metric("Unique Products", st.session_state.df['Product'].nunique())
    
    # Export
    st.subheader("Export Data")
    
    # CSV Export
    csv = st.session_state.df.to_csv(index=False)
    st.download_button(
        "📥 Download CSV", 
        data=csv, 
        file_name="data_export.csv",
        mime="text/csv",
        key="csv_download"
    )

# TAB 5: Report - FIXED REPORT BUTTON
with tab5:
    st.header("Analytical Report")
    
    # Report configuration
    st.subheader("Report Configuration")
    
    report_title = st.text_input("Report Title:", "Commercial Data Analysis Report")
    
    # Generate Report Button - ALWAYS VISIBLE
    if st.button("📄 Generate Report", type="primary", key="report_btn"):
        # Create report content
        report_content = f"""
        {'='*60}
        {report_title}
        {'='*60}
        
        Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        DATASET SUMMARY:
        • Total Records: {len(st.session_state.df):,}
        • Total Columns: {len(st.session_state.df.columns)}
        • Date Range: {st.session_state.df['Date'].min().date()} to {st.session_state.df['Date'].max().date()}
        • Memory Usage: {st.session_state.df.memory_usage().sum() / 1024:.1f} KB
        
        KEY METRICS:
        • Total Sales: ${st.session_state.df['Sales'].sum():,}
        • Average Profit: ${st.session_state.df['Profit'].mean():.2f}
        • Total Quantity Sold: {st.session_state.df['Quantity'].sum():,}
        • Number of Products: {st.session_state.df['Product'].nunique()}
        • Number of Regions: {st.session_state.df['Region'].nunique()}
        
        AGILE SPRINTS COMPLETED:
        1. ✅ Sprint 1: Data Loading & Validation
        2. ✅ Sprint 2: Data Cleaning & Transformation
        3. ✅ Sprint 3: Data Visualization
        4. ✅ Sprint 4: KPI Dashboard & Export
        5. ✅ Sprint 5: Analytical Report Generation
        
        TECHNICAL IMPLEMENTATION:
        • Built with Python and Streamlit
        • Uses Pandas for data processing
        • Matplotlib for visualization
        • Agile Scrum methodology
        • Jira for project tracking
        
        RECOMMENDATIONS:
        1. Implement automated data validation
        2. Add predictive analytics features
        3. Create user authentication system
        4. Add real-time data integration
        5. Develop mobile-responsive version
        
        {'='*60}
        End of Report
        {'='*60}
        """
        
        # Save to session state
        st.session_state.report_content = report_content
        st.session_state.report_generated = True
        st.success("✅ Report generated successfully!")
    
    # Show report if generated
    if hasattr(st.session_state, 'report_generated') and st.session_state.report_generated:
        st.subheader("Report Preview")
        
        # Show report in text area
        st.text_area("Report Content", 
                    st.session_state.report_content, 
                    height=400,
                    key="report_display")
        
        # Download button for report
        st.download_button(
            label="📥 Download Report (.txt)",
            data=st.session_state.report_content,
            file_name="data_analysis_report.txt",
            mime="text/plain",
            key="report_download"
        )
    else:
        st.info("Click 'Generate Report' button above to create your report")

# Footer
st.divider()
st.caption("Built with Streamlit | Agile Scrum Project | 👥 Team: MA, LJ, M, HZ")
