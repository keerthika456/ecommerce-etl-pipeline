# eda.py — Exploratory Data Analysis
# Run this BEFORE writing any ETL code
# Purpose: Understand the raw data completely

import pandas as pd

# ─── Load Data ───────────────────────────────────────────────
df = pd.read_csv("data/data.csv", encoding='latin-1')

# ─── 1. Basic Shape ──────────────────────────────────────────
print("=" * 60)
print("1. SHAPE — How many rows and columns?")
print(f"   Rows    : {df.shape[0]}")
print(f"   Columns : {df.shape[1]}")

# ─── 2. Column Names & Data Types ────────────────────────────
print("=" * 60)
print("2. COLUMNS & DATA TYPES")
print(df.dtypes)

# ─── 3. First 5 Rows ─────────────────────────────────────────
print("=" * 60)
print("3. FIRST 5 ROWS — What does the data look like?")
print(df.head())

# ─── 4. Last 5 Rows ──────────────────────────────────────────
print("=" * 60)
print("4. LAST 5 ROWS")
print(df.tail())

# ─── 5. Missing Values ───────────────────────────────────────
print("=" * 60)
print("5. MISSING VALUES — Which columns have nulls?")
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Missing Count': missing,
    'Missing %': missing_pct
})
print(missing_df[missing_df['Missing Count'] > 0])

# ─── 6. Duplicate Rows ───────────────────────────────────────
print("=" * 60)
print("6. DUPLICATE ROWS")
print(f"   Total duplicates: {df.duplicated().sum()}")

# ─── 7. Basic Statistics ─────────────────────────────────────
print("=" * 60)
print("7. BASIC STATISTICS — Numbers only")
print(df.describe())

# ─── 8. Unique Values Per Column ─────────────────────────────
print("=" * 60)
print("8. UNIQUE VALUES PER COLUMN")
print(df.nunique())

# ─── 9. Sample Values Per Column ─────────────────────────────
print("=" * 60)
print("9. SAMPLE VALUES — What's inside each column?")
for col in df.columns:
    print(f"\n   [{col}] — Sample: {df[col].dropna().unique()[:5]}")

# ─── 10. Negative or Zero Values ─────────────────────────────
print("=" * 60)
print("10. NEGATIVE VALUES — Data quality check")
for col in df.select_dtypes(include='number').columns:
    neg_count = (df[col] < 0).sum()
    if neg_count > 0:
        print(f"   {col}: {neg_count} negative values")

# ─── 11. Check Cancelled Orders (C prefix) ───────────────
print("=" * 60)
print("11. CANCELLED ORDERS — InvoiceNo starting with C")
cancelled = df[df['InvoiceNo'].str.startswith('C')]
print(f"Total cancelled invoices: {len(cancelled)}")
print(cancelled.head(10))

print("=" * 60)
print("EDA COMPLETE — Now we know exactly what to clean!")