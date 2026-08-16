"""
Data Cleaning & Visualization Project
Dataset: Retail Sales (practice dataset with intentional data-quality issues)

Run:
    pip install pandas matplotlib seaborn
    python analysis.py
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE = Path(__file__).resolve().parent
RAW = BASE / "data" / "raw_retail_sales.csv"
OUT = BASE / "data" / "cleaned_retail_sales.csv"
VIS = BASE / "visuals"
VIS.mkdir(exist_ok=True)

# Load raw data
df = pd.read_csv(RAW)

print("RAW DATA SHAPE:", df.shape)
print("\nMISSING VALUES BEFORE CLEANING:")
print(df.isna().sum())
print("\nDUPLICATES BEFORE CLEANING:", df.duplicated().sum())

# Standardize text
for col in ["Product", "Category", "Region"]:
    df[col] = df[col].astype("string").str.strip().str.title()

# Convert data types
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
for col in ["Quantity", "Unit_Price", "Total_Sales"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove duplicate orders
df = df.drop_duplicates(subset=["Order_ID"], keep="first")

# Treat invalid numeric values as missing
df.loc[df["Quantity"] <= 0, "Quantity"] = pd.NA
df.loc[df["Unit_Price"] <= 0, "Unit_Price"] = pd.NA

# Fill missing values
df["Customer_ID"] = df["Customer_ID"].fillna("Unknown")
df["Region"] = df["Region"].fillna("Unknown")
df["Category"] = df["Category"].fillna("Unknown")
df["Product"] = df["Product"].fillna("Unknown")
df["Unit_Price"] = df.groupby("Product")["Unit_Price"].transform(
    lambda s: s.fillna(s.median())
)
df["Unit_Price"] = df["Unit_Price"].fillna(df["Unit_Price"].median())
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median()).round().astype(int)

# Recalculate sales
df["Total_Sales"] = df["Quantity"] * df["Unit_Price"]

# IQR outlier capping
q1 = df["Total_Sales"].quantile(0.25)
q3 = df["Total_Sales"].quantile(0.75)
iqr = q3 - q1
lower = max(0, q1 - 1.5 * iqr)
upper = q3 + 1.5 * iqr
df["Total_Sales"] = df["Total_Sales"].clip(lower, upper)

df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
df.to_csv(OUT, index=False)

print("\nCLEANED DATA SHAPE:", df.shape)
print("\nMISSING VALUES AFTER CLEANING:")
print(df.isna().sum())
print("\nDUPLICATES AFTER CLEANING:", df.duplicated().sum())

# Visualizations
sns.set_theme(style="whitegrid")

monthly = df.groupby("Month", as_index=False)["Total_Sales"].sum()
plt.figure(figsize=(10, 6))
sns.lineplot(data=monthly, x="Month", y="Total_Sales", marker="o")
plt.title("Monthly Sales Trend")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(VIS / "monthly_sales.png", dpi=150)
plt.close()

category = df.groupby("Category", as_index=False)["Total_Sales"].sum()
plt.figure(figsize=(10, 6))
sns.barplot(data=category, x="Category", y="Total_Sales")
plt.title("Sales by Category")
plt.tight_layout()
plt.savefig(VIS / "category_sales.png", dpi=150)
plt.close()

product = df.groupby("Product", as_index=False)["Total_Sales"].sum().sort_values("Total_Sales", ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(data=product, x="Total_Sales", y="Product")
plt.title("Sales by Product")
plt.tight_layout()
plt.savefig(VIS / "product_sales.png", dpi=150)
plt.close()

region = df.groupby("Region", as_index=False)["Total_Sales"].sum()
plt.figure(figsize=(10, 6))
sns.barplot(data=region, x="Region", y="Total_Sales")
plt.title("Sales by Region")
plt.tight_layout()
plt.savefig(VIS / "region_sales.png", dpi=150)
plt.close()

print("\nTOP PRODUCTS:")
print(product.head(5).to_string(index=False))

print("\nPROJECT COMPLETE.")
