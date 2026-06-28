"""
=============================================================
  Sales Dashboard — Step 4: Automated ETL Pipeline
=============================================================
  Reads cleaned CSVs → Loads into PostgreSQL
  Schedule with cron or Windows Task Scheduler for daily refresh
=============================================================
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging
import os
from datetime import datetime

# ── Logging ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s"
)
log = logging.getLogger(__name__)

# ── DB Config — use environment variables in production ──────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     os.getenv("DB_PORT",     5432),
    "database": os.getenv("DB_NAME",     "sales_db"),
    "user":     os.getenv("DB_USER",     "postgres"),
    "password": os.getenv("DB_PASSWORD", "your_password"),
}

CLEANED_DIR = "data/cleaned"


def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    log.info("✅  Connected to PostgreSQL")
    return conn


def load_table(conn, df: pd.DataFrame, table: str, truncate: bool = True):
    """Generic loader — truncates table then bulk-inserts."""
    cursor = conn.cursor()
    if truncate:
        cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
        log.info(f"  Truncated: {table}")

    cols   = list(df.columns)
    values = [tuple(row) for row in df.itertuples(index=False)]
    sql    = f"INSERT INTO {table} ({', '.join(cols)}) VALUES %s ON CONFLICT DO NOTHING"
    execute_values(cursor, sql, values)
    conn.commit()
    log.info(f"  Loaded {len(values):,} rows → {table}")
    cursor.close()


def run_etl():
    log.info("╔══════════════════════════════════════════╗")
    log.info("║  SALES DASHBOARD — ETL START              ║")
    log.info(f"║  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                    ║")
    log.info("╚══════════════════════════════════════════╝")

    conn = get_connection()

    try:
        # 1. Customers
        customers = pd.read_csv(f"{CLEANED_DIR}/customers_clean.csv", parse_dates=["join_date"])
        load_table(conn, customers, "customers")

        # 2. Products
        products = pd.read_csv(f"{CLEANED_DIR}/products_clean.csv")
        load_table(conn, products, "products")

        # 3. Sales Reps
        sales_reps = pd.read_csv(f"{CLEANED_DIR}/sales_reps_clean.csv", parse_dates=["join_date"])
        load_table(conn, sales_reps, "sales_reps")

        # 4. Orders (largest table — load last due to FK constraints)
        orders = pd.read_csv(f"{CLEANED_DIR}/orders_clean.csv", parse_dates=["order_date"])
        load_table(conn, orders, "orders")

        log.info("✅  ETL completed successfully")

    except Exception as e:
        conn.rollback()
        log.error(f"❌  ETL FAILED: {e}")
        raise

    finally:
        conn.close()
        log.info("  DB connection closed")


if __name__ == "__main__":
    run_etl()
