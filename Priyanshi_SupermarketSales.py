import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide")

st.title("🛒 Supermarket Sales Analysis & Executive Dashboard")
st.markdown("### IBM SkillsBuild Data Analytics with AI Academic Internship")
st.markdown("---")

# 2. Data Loading
@st.cache_data
def load_data():
    # Kaggle Dataset Read
    df = pd.read_csv('SuperMarket Analysis.csv')
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Error: 'SuperMarket Analysis' file nahi mili. Kripya file ko same folder mein rakhein.")
    st.stop()

# 3. Sidebar Filters
st.sidebar.header("Filter Options")
city_filter = st.sidebar.multiselect("Select City:", options=df['City'].unique(), default=df['City'].unique())
product_filter = st.sidebar.multiselect("Select Product Line:", options=df['Product line'].unique(), default=df['Product line'].unique())

df_filtered = df[(df['City'].isin(city_filter)) & (df['Product line'].isin(product_filter))]

# 4. Key Metrics (KPIs)
st.subheader("📌 Key Executive Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.2f}")
c2.metric("Items Sold", f"{df_filtered['Quantity'].sum():,}")
c3.metric("Transactions", f"{len(df_filtered):,}")
c4.metric("Avg Rating", f"{df_filtered['Rating'].mean():.2f} ⭐")

st.markdown("---")

# 5. Interactive Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Sales Revenue by Product Line")
    product_sales = df_filtered.groupby('Product line')['Sales'].sum().reset_index()
    fig_bar = px.bar(
        product_sales, 
        x='Sales', 
        y='Product line', 
        orientation='h', 
        color='Sales',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("💳 Sales Share by Payment Method")
    fig_pie = px.pie(
        df_filtered, 
        names='Payment', 
        values='Sales', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# 6. Executive Insights
st.subheader("💡 Executive Insights & Recommendations")
st.markdown("""
* **Observations:** Food & Beverages and Electronic accessories generated high sales share.
* **Insights:** E-wallet and Cash are widely used across all major branches.
* **Recommendations:** Target promotional offers toward popular payment modes and stock high-performing product lines in key city branches.
""")
