import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Initialize session state
if 'df' not in st.session_state:
    # Create simple data
    np.random.seed(42)
    n = 150
    
    data = {
        'Date': [datetime.date(2023, 1, 1) + datetime.timedelta(days=i) for i in range(n)],
        'Product': np.random.choice(['Laptop', 'Phone', 'Tablet'], n),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], n),
        'Sales': np.random.randint(100, 5000, n),
        'Quantity': np.random.randint(1, 20, n),
        'Profit': np.random.randint(-50, 300, n)
    }
    
    st.session_state.df = pd.DataFrame(data)

# App config - SIMPLE
st.set_page_config(page_title="Data App", layout="centered")

# TITLE
st.title("📊 Data Analysis Application")
st.markdown("**Agile Scrum Project | Team: MA, LJ, M, HZ**")
st.divider()

# SIMPLE TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Load", " Clean", "Chart", "Dashboard", " Report"])

# TAB 1: LOAD
with tab1:
    st.header("Data Loading & Validation")
    st.dataframe(st.session_state.df.head(10))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", len(st.session_state.df))
    with col2:
        st.metric("Sales Total", f"${st.session_state.df['Sales'].sum():,}")
    with col3:
        st.metric("Avg Profit", f"${st.session_state.df['Profit'].mean():.2f}")

# TAB 2: CLEAN
with tab2:
    st.header("Data Cleaning")
    
    if st.button("Remove Duplicates"):
        before = len(st.session_state.df)
        st.session_state.df = st.session_state.df.drop_duplicates()
        after = len(st.session_state.df)
        st.success(f"Removed {before-after} duplicates!")
        st.rerun()
    
    if st.button("Reset Data"):
        np.random.seed(42)
        n = 150
        data = {
            'Date': [datetime.date(2023, 1, 1) + datetime.timedelta(days=i) for i in range(n)],
            'Product': np.random.choice(['Laptop', 'Phone', 'Tablet'], n),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], n),
            'Sales': np.random.randint(100, 5000, n),
            'Quantity': np.random.randint(1, 20, n),
            'Profit': np.random.randint(-50, 300, n)
        }
        st.session_state.df = pd.DataFrame(data)
        st.success("Data reset to original!")
        st.rerun()

# TAB 3: CHART (USING STREAMLIT NATIVE - NO MATPLOTLIB!)
with tab3:
    st.header("Data Visualization")
    
    # Streamlit native charts - NO MATPLOTLIB NEEDED!
    st.subheader("Sales by Region")
    region_sales = st.session_state.df.groupby('Region')['Sales'].sum().reset_index()
    st.bar_chart(region_sales.set_index('Region'))
    
    st.subheader("Sales Over Time")
    st.line_chart(st.session_state.df.set_index('Date')['Sales'])
    
    st.subheader("Profit Distribution")
    st.area_chart(st.session_state.df.set_index('Date')['Profit'])

# TAB 4: DASHBOARD
with tab4:
    st.header("KPI Dashboard")
    
    # KPIs in columns
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Sales", f"${st.session_state.df['Sales'].sum():,}")
    with k2:
        st.metric("Total Profit", f"${st.session_state.df['Profit'].sum():,}")
    with k3:
        st.metric("Avg Sale", f"${st.session_state.df['Sales'].mean():.2f}")
    with k4:
        st.metric("Transactions", len(st.session_state.df))
    
    # Export buttons
    st.divider()
    st.subheader("Export Data")
    
    # CSV Export
    csv = st.session_state.df.to_csv(index=False)
    st.download_button(
        "📥 Download CSV",
        data=csv,
        file_name="commercial_data.csv",
        mime="text/csv"
    )
    
    # Show top products
    st.divider()
    st.subheader("Top Products")
    top_products = st.session_state.df.groupby('Product')['Sales'].sum().sort_values(ascending=False)
    st.dataframe(top_products.reset_index())

# TAB 5: REPORT
with tab5:
    st.header("Analytical Report")
    
    # ALWAYS VISIBLE BUTTON
    if st.button("📄 Generate Report", type="primary"):
        report = f"""
        {'='*50}
        COMMERCIAL DATA ANALYSIS REPORT
        {'='*50}
        
        Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        EXECUTIVE SUMMARY:
        • Total Records: {len(st.session_state.df):,}
        • Total Sales: ${st.session_state.df['Sales'].sum():,}
        • Total Profit: ${st.session_state.df['Profit'].sum():,}
        • Average Sale: ${st.session_state.df['Sales'].mean():.2f}
        • Date Range: {st.session_state.df['Date'].min()} to {st.session_state.df['Date'].max()}
        
        PRODUCT PERFORMANCE:
        """
        
        # Add product stats
        product_stats = st.session_state.df.groupby('Product').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).sort_values('Sales', ascending=False)
        
        for product, row in product_stats.iterrows():
            report += f"\n• {product}: Sales=${row['Sales']:,}, Profit=${row['Profit']:,}, Qty={row['Quantity']}"
        
        report += f"""
        
        REGIONAL ANALYSIS:
        """
        
        # Add region stats
        region_stats = st.session_state.df.groupby('Region').agg({
            'Sales': 'sum',
            'Profit': 'mean'
        })
        
        for region, row in region_stats.iterrows():
            report += f"\n• {region}: Sales=${row['Sales']:,}, Avg Profit=${row['Profit']:.2f}"
        
        report += f"""
        
        AGILE SPRINTS COMPLETED:
        1. ✅ Data Loading & Validation
        2. ✅ Data Cleaning & Transformation  
        3. ✅ Data Visualization
        4. ✅ KPI Dashboard
        5. ✅ Analytical Report
        
        RECOMMENDATIONS:
        1. Focus on high-performing products
        2. Expand in profitable regions
        3. Implement automated reporting
        4. Add predictive analytics
        
        {'='*50}
        END OF REPORT
        {'='*50}
        """
        
        # Save report
        st.session_state.report = report
        st.success("✅ Report generated!")
    
    # Show report if exists
    if 'report' in st.session_state:
        st.text_area("Report Preview", st.session_state.report, height=400)
        
        # Download button
        st.download_button(
            "📥 Download Report",
            data=st.session_state.report,
            file_name="analysis_report.txt",
            mime="text/plain"
        )
    else:
        st.info("Click 'Generate Report' button above")

# FOOTER
st.divider()
st.caption("© 2024 Data Analysis App | Built with Streamlit | Agile Scrum Methodology")
