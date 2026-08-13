import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "raw" / "Online Retail.xlsx"

df = pd.read_excel(file_path)

print("=" * 60)
print("DATASET PROFILING")
print("=" * 60)

# 1. Shape
print("\n1. Dataset Shape")
print(df.shape)

# 2. Duplicate rows
print("\n2. Duplicate Rows")
print(df.duplicated().sum())

# 3. Missing values
print("\n3. Missing Values")
print(df.isnull().sum())

# 4. Negative quantities
print("\n4. Negative Quantity Rows")
print((df["Quantity"] < 0).sum())

# 5. Zero quantities
print("\n5. Zero Quantity Rows")
print((df["Quantity"] == 0).sum())

# 6. Zero / negative prices
print("\n6. Zero UnitPrice Rows")
print((df["UnitPrice"] == 0).sum())

print("\n7. Negative UnitPrice Rows")
print((df["UnitPrice"] < 0).sum())

# 7. Unique values
print("\n8. Unique Values")
print(df.nunique())

# 8. Invoice patterns
print("\n9. Invoice Samples")
print(df["InvoiceNo"].head(20).tolist())

# 9. Countries
print("\n10. Number of Countries")
print(df["Country"].nunique())

print("\nTop 10 Countries:")
print(df["Country"].value_counts().head(10))

print("\nProfiling completed.")