import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="E-Commerce Sales Dashboard", layout="wide")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/online_retail_cleaned.csv", encoding="latin1")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["TotalRevenue"] = df["Quantity"] * df["UnitPrice"]
    return df

df = load_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔍 Filters")

# Country Filter
countries = ["All"] + sorted(df["Country"].unique().tolist())
selected_country = st.sidebar.selectbox("🌍 Select Country", countries)

# Month Filter
df["Month"] = df["InvoiceDate"].dt.month_name()
months = ["All"] + sorted(df["Month"].unique().tolist())
selected_month = st.sidebar.selectbox("📅 Select Month", months)

# Filter Data
filtered_df = df.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]
if selected_month != "All":
    filtered_df = filtered_df[filtered_df["Month"] == selected_month]

# ---------- KPI CALCULATIONS ----------
total_revenue = filtered_df["TotalRevenue"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
total_customers = filtered_df["CustomerID"].nunique()
total_products = filtered_df["StockCode"].nunique()

# ---------- KPI CARDS ----------
st.title("📊 E-Commerce Sales Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("📦 Total Orders", f"{total_orders:,}")
col3.metric("👥 Total Customers", f"{total_customers:,}")
col4.metric("🏷️ Total Products", f"{total_products:,}")

st.markdown("---")

# ---------- ROW 1: Charts ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 Revenue by Country")
    country_rev = filtered_df.groupby("Country")["TotalRevenue"].sum().sort_values(ascending=False).head(10).reset_index()
    fig1 = px.bar(country_rev, x="TotalRevenue", y="Country", orientation="h", text_auto=True, color_discrete_sequence=["#1f77b4"])
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🏆 Top 10 Products by Revenue")
    top_products = filtered_df.groupby("Description")["TotalRevenue"].sum().sort_values(ascending=False).head(10).reset_index()
    fig2 = px.bar(top_products, x="TotalRevenue", y="Description", orientation="h", text_auto=True, color_discrete_sequence=["#ff7f0e"])
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

# ---------- ROW 2: Charts ----------
col3, col4 = st.columns(2)

with col3:
    st.subheader("📈 Monthly Revenue Trend")
    monthly_rev = filtered_df.groupby(filtered_df["InvoiceDate"].dt.to_period("M"))["TotalRevenue"].sum().reset_index()
    monthly_rev["InvoiceDate"] = monthly_rev["InvoiceDate"].astype(str)
    fig3 = px.line(monthly_rev, x="InvoiceDate", y="TotalRevenue", markers=True, color_discrete_sequence=["#2ca02c"])
    fig3.update_layout(height=350)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("📦 Monthly Units Sold")
    monthly_units = filtered_df.groupby(filtered_df["InvoiceDate"].dt.to_period("M"))["Quantity"].sum().reset_index()
    monthly_units["InvoiceDate"] = monthly_units["InvoiceDate"].astype(str)
    fig4 = px.bar(monthly_units, x="InvoiceDate", y="Quantity", color_discrete_sequence=["#d62728"])
    fig4.update_layout(height=350)
    st.plotly_chart(fig4, use_container_width=True)

# ---------- ROW 3: Customer Analysis ----------
st.markdown("---")
st.subheader("👥 Customer Revenue Analysis")

customer_rev = filtered_df.groupby("CustomerID")["TotalRevenue"].sum().reset_index()
repeat_customers = customer_rev[customer_rev["TotalRevenue"] > 0].shape[0]
one_time_customers = customer_rev[customer_rev["TotalRevenue"] <= 0].shape[0]
repeat_customers_rev = customer_rev[customer_rev["TotalRevenue"] > 0]["TotalRevenue"].sum()
one_time_customers_rev = customer_rev[customer_rev["TotalRevenue"] <= 0]["TotalRevenue"].sum()

col5, col6 = st.columns(2)

with col5:
    st.metric("🔄 Repeat Customers", f"{repeat_customers:,}")
    st.metric("💰 Repeat Revenue", f"${repeat_customers_rev:,.2f}")

with col6:
    st.metric("⏳ One-Time Customers", f"{one_time_customers:,}")
    st.metric("💰 One-Time Revenue", f"${one_time_customers_rev:,.2f}")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("📊 Data Source: Online Retail Dataset | Dashboard by Data Analyst")