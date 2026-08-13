import pandas as pd
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Raw dataset path
file_path = BASE_DIR / "data" / "raw" / "Online Retail.xlsx"

print("Loading:", file_path)

# Load Excel dataset
df = pd.read_excel(file_path)

print("\nDataset loaded successfully!")
print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())