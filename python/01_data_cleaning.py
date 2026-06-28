"""
=============================================================
  Sales Dashboard — Step 1: Data Cleaning Pipeline
=============================================================
  Author  : Your Name
  Purpose : Clean raw CSV files and produce analysis-ready data
  Input   : data/raw/*.csv
  Output  : data/cleaned/*.csv
=============================================================
"""

import pandas as pd
import numpy as np
import os
import logging
from datetime import datetime

# ── Logging setup ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)

RAW_DIR     = "data/raw"
CLEANED_DIR = "data/cleaned"
os.makedirs(CLEANED_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════
#  ORDERS CLEANING
# ═══════════════════════════════════════════════════════════
def clean_orders(path: str) -> pd.DataFrame:
    log.info("── Cleaning orders ──────────────────────────")
    df = pd.read_csv(path)
    log.info(f"  Raw shape      : {df.shape}")

    # Step 1 — Remove duplicates
    before = len(df)
    df.drop_duplicates(subset=["order_id"], keep="last", inplace=True)
    log.info(f"  Duplicates removed  : {before - len(df)}")

    # Step 2 — Drop rows with NULL amount (cannot impute)
    null_amount = df["amount"].isna().sum()
    df.dropna(subset=["amount"], inplace=True)
    log.info(f"  NULL amounts dropped: {null_amount}")

    # Step 3 — Standardize date to ISO 8601
    df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True, errors="coerce")
    invalid_dates = df["order_date"].isna().sum()
    df.dropna(subset=["order_date"], inplace=True)
    log.info(f"  Invalid dates dropped: {invalid_dates}")

    # Step 4 — Standardize status column
    df["status"] = df["status"].str.strip().str.title()

    # Step 5 — Outlier detection (IQR method on amount)
    Q1 = df["amount"].quantile(0.25)
    Q3 = df["amount"].quantile(0.75)
    IQR = Q3 - Q1
    upper_fence = Q3 + 1.5 * IQR
    outliers = df[df["amount"] > upper_fence]
    log.info(f"  Outliers detected (>{upper_fence:.0f}): {len(outliers)} rows — review manually")

    # Step 6 — Feature engineering
    df["order_month"]       = df["order_date"].dt.month
    df["order_quarter"]     = df["order_date"].dt.quarter
    df["order_year"]        = df["order_date"].dt.year
    df["order_day_of_week"] = df["order_date"].dt.day_name()

    log.info(f"  Clean shape    : {df.shape}")
    return df


# ═══════════════════════════════════════════════════════════
#  CUSTOMERS CLEANING
# ═══════════════════════════════════════════════════════════
def clean_customers(path: str) -> pd.DataFrame:
    log.info("── Cleaning customers ───────────────────────")
    df = pd.read_csv(path)
    log.info(f"  Raw shape      : {df.shape}")

    # Step 1 — Standardize region (case + whitespace)
    df["region"] = df["region"].str.strip().str.title()

    # Step 2 — Fill missing region (will be filled via order join later)
    null_region = df["region"].isna().sum()
    log.info(f"  NULL regions   : {null_region} (filled as 'Unknown')")
    df["region"].fillna("Unknown", inplace=True)

    # Step 3 — Standardize segment
    df["segment"] = df["segment"].str.strip().str.title()

    # Step 4 — Parse join_date
    df["join_date"] = pd.to_datetime(df["join_date"], dayfirst=True, errors="coerce")

    # Step 5 — Feature engineering
    df["tenure_days"] = (pd.Timestamp.today() - df["join_date"]).dt.days
    df["tenure_years"] = (df["tenure_days"] / 365).round(1)

    log.info(f"  Clean shape    : {df.shape}")
    return df


# ═══════════════════════════════════════════════════════════
#  PRODUCTS CLEANING
# ═══════════════════════════════════════════════════════════

CATEGORY_MAP = {
    "electronics": "Electronics",
    "electrnics":  "Electronics",   # typo fix
    "ELECTRONICS": "Electronics",
    "clothing":    "Clothing",
    "home goods":  "Home Goods",
    "sports":      "Sports",
}

def clean_products(path: str) -> pd.DataFrame:
    log.info("── Cleaning products ────────────────────────")
    df = pd.read_csv(path)
    log.info(f"  Raw shape      : {df.shape}")

    # Step 1 — Fix category inconsistencies
    df["category_raw"] = df["category"]   # keep original for audit
    df["category"] = (
        df["category"]
        .str.strip()
        .str.lower()
        .map(lambda x: CATEGORY_MAP.get(x, x.title()))
    )
    variants_fixed = (df["category"] != df["category_raw"]).sum()
    log.info(f"  Category variants fixed: {variants_fixed}")

    # Step 2 — Calculate profit margin
    df["profit_margin_pct"] = (
        (df["mrp"] - df["cost_price"]) / df["mrp"] * 100
    ).round(2)

    log.info(f"  Clean shape    : {df.shape}")
    return df


# ═══════════════════════════════════════════════════════════
#  SALES REPS CLEANING
# ═══════════════════════════════════════════════════════════
def clean_sales_reps(path: str) -> pd.DataFrame:
    log.info("── Cleaning sales_reps ──────────────────────")
    df = pd.read_csv(path)
    log.info(f"  Raw shape      : {df.shape}")

    df["region"]    = df["region"].str.strip().str.title()
    df["join_date"] = pd.to_datetime(df["join_date"], dayfirst=True, errors="coerce")

    log.info(f"  Clean shape    : {df.shape}")
    return df


# ═══════════════════════════════════════════════════════════
#  ENRICHMENT — join orders with customers & products
# ═══════════════════════════════════════════════════════════
def enrich_orders(orders, customers, products):
    log.info("── Enriching orders ─────────────────────────")

    merged = orders.merge(
        customers[["customer_id", "customer_name", "region", "segment"]],
        on="customer_id", how="left"
    )
    merged = merged.merge(
        products[["product_id", "product_name", "category", "cost_price", "profit_margin_pct"]],
        on="product_id", how="left"
    )

    # Fix NULL regions using customer join
    still_null = merged["region"].isna().sum()
    log.info(f"  Remaining NULL regions after join: {still_null}")

    # is_repeat_customer flag
    order_counts = merged.groupby("customer_id")["order_id"].transform("count")
    merged["is_repeat_customer"] = (order_counts > 1).astype(int)

    # profit per order
    merged["profit_amount"] = merged["amount"] - merged.get("cost_price", 0)

    log.info(f"  Enriched shape : {merged.shape}")
    return merged


# ═══════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════
def main():
    log.info("╔══════════════════════════════════════════╗")
    log.info("║  SALES DASHBOARD — DATA CLEANING START   ║")
    log.info("╚══════════════════════════════════════════╝")
    start = datetime.now()

    orders    = clean_orders(f"{RAW_DIR}/orders_raw.csv")
    customers = clean_customers(f"{RAW_DIR}/customers_raw.csv")
    products  = clean_products(f"{RAW_DIR}/products_raw.csv")
    sales_reps = clean_sales_reps(f"{RAW_DIR}/sales_reps_raw.csv")

    enriched  = enrich_orders(orders, customers, products)

    # ── Save cleaned files ──
    orders.to_csv(f"{CLEANED_DIR}/orders_clean.csv", index=False)
    customers.to_csv(f"{CLEANED_DIR}/customers_clean.csv", index=False)
    products.to_csv(f"{CLEANED_DIR}/products_clean.csv", index=False)
    sales_reps.to_csv(f"{CLEANED_DIR}/sales_reps_clean.csv", index=False)
    enriched.to_csv(f"{CLEANED_DIR}/orders_enriched.csv", index=False)

    elapsed = (datetime.now() - start).seconds
    log.info(f"✅  All files saved to '{CLEANED_DIR}/' in {elapsed}s")
    log.info("════════════════════════════════════════════")


if __name__ == "__main__":
    main()
