import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Paths
input_path = BASE_DIR / "data" / "raw" / "Online Retail.xlsx"
output_path = BASE_DIR / "data" / "cleaned" / "online_retail_cleaned.csv"

# Load raw data
df = pd.read_excel(input_path)

print("=" * 60)
print("DATA CLEANING")
print("=" * 60)

print("\nOriginal shape:", df.shape)

# --------------------------------------------------
# 1. Remove duplicate rows
# --------------------------------------------------

before = len(df)

df = df.drop_duplicates()

after = len(df)

print("\nDuplicates removed:", before - after)
print("Shape after duplicate removal:", df.shape)

# --------------------------------------------------
# 2. Clean Description
# --------------------------------------------------

df["Description"] = df["Description"].str.strip()

# --------------------------------------------------
# 3. Convert CustomerID to nullable integer
# --------------------------------------------------

df["CustomerID"] = df["CustomerID"].astype("Int64")

# --------------------------------------------------
# 4. Create transaction type
# --------------------------------------------------

df["TransactionType"] = "Sale"

df.loc[df["Quantity"] < 0, "TransactionType"] = "Return"

# --------------------------------------------------
# 5. Create Revenue
# --------------------------------------------------

df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# --------------------------------------------------
# 6. Remove invalid prices
# --------------------------------------------------

df = df[df["UnitPrice"] >= 0]

# --------------------------------------------------
# 7. Save cleaned dataset
# --------------------------------------------------

df.to_csv(output_path, index=False)

print("\nFinal shape:", df.shape)

print("\nTransaction Types:")
print(df["TransactionType"].value_counts())

print("\nCleaned dataset saved to:")
print(output_path)

print("\nDATA CLEANING COMPLETED")