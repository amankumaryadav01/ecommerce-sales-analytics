import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Cleaned dataset
input_path = BASE_DIR / "data" / "cleaned" / "online_retail_cleaned.csv"

# Load cleaned data
df = pd.read_csv(input_path)

print("=" * 60)
print("EDA - DATA VALIDATION")
print("=" * 60)

# Convert date column
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Basic information
print("\n1. Dataset Shape")
print(df.shape)

print("\n2. Columns")
print(df.columns.tolist())

# Revenue validation
print("\n3. Revenue Summary")
print("Total Revenue:", df["Revenue"].sum())
print("Sales Revenue:", df.loc[df["TransactionType"] == "Sale", "Revenue"].sum())
print("Return Value:", df.loc[df["TransactionType"] == "Return", "Revenue"].sum())

# Date range
print("\n4. Date Range")
print("Start:", df["InvoiceDate"].min())
print("End:", df["InvoiceDate"].max())

# Transaction types
print("\n5. Transaction Types")
print(df["TransactionType"].value_counts())

# Revenue by transaction type
print("\n6. Revenue by Transaction Type")
print(
    df.groupby("TransactionType")["Revenue"]
    .agg(["sum", "count", "mean"])
)

# Missing values after cleaning
print("\n7. Missing Values")
print(df.isnull().sum())

print("\nEDA validation completed.")

# --------------------------------------------------
# 8. Monthly Revenue Analysis
# --------------------------------------------------

df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

monthly_revenue = (
    df.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

print("\n8. Monthly Revenue")
print(monthly_revenue.to_string(index=False))

# Best month
best_month = monthly_revenue.loc[
    monthly_revenue["Revenue"].idxmax()
]

print("\nBest Revenue Month:")
print(best_month)

# Worst month
worst_month = monthly_revenue.loc[
    monthly_revenue["Revenue"].idxmin()
]

print("\nLowest Revenue Month:")
print(worst_month)
print("\nEDA validation completed.")


# --------------------------------------------------
# 9. Top Products by Revenue
# --------------------------------------------------

product_revenue = (
    df[df["TransactionType"] == "Sale"]
    .groupby(["StockCode", "Description"])["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

print("\n9. Top 10 Products by Revenue")
print(product_revenue.head(10).to_string(index=False))

# Top products by quantity
product_quantity = (
    df[df["TransactionType"] == "Sale"]
    .groupby(["StockCode", "Description"])["Quantity"]
    .sum()
    .reset_index()
    .sort_values("Quantity", ascending=False)
)

print("\nTop 10 Products by Quantity Sold")
print(product_quantity.head(10).to_string(index=False))
# --------------------------------------------------
# 10. Country Revenue Analysis
# --------------------------------------------------

country_revenue = (
    df[df["TransactionType"] == "Sale"]
    .groupby("Country")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

print("\n10. Top 10 Countries by Revenue")
print(country_revenue.head(10).to_string(index=False))


# Number of orders by country
country_orders = (
    df[df["TransactionType"] == "Sale"]
    .groupby("Country")["InvoiceNo"]
    .nunique()
    .reset_index(name="Orders")
    .sort_values("Orders", ascending=False)
)

print("\nTop 10 Countries by Number of Orders")
print(country_orders.head(10).to_string(index=False))