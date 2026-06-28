"""
=============================================================
  Sales Dashboard — Step 2: Exploratory Data Analysis (EDA)
=============================================================
  Run AFTER 01_data_cleaning.py
  Input  : data/cleaned/orders_enriched.csv
  Output : Printed stats + saved plots in docs/screenshots/
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── Style ───────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0F172A",
    "axes.facecolor":   "#1E293B",
    "axes.edgecolor":   "#334155",
    "axes.labelcolor":  "#94A3B8",
    "xtick.color":      "#94A3B8",
    "ytick.color":      "#94A3B8",
    "text.color":       "#F8FAFC",
    "grid.color":       "#334155",
    "grid.linestyle":   "--",
    "grid.linewidth":   0.5,
    "font.family":      "sans-serif",
})

BLUE    = "#3B82F6"
GREEN   = "#10B981"
AMBER   = "#F59E0B"
ROSE    = "#F43F5E"

OUTPUT_DIR = "docs/screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data():
    df = pd.read_csv("data/cleaned/orders_enriched.csv", parse_dates=["order_date"])
    df = df[df["status"] == "Completed"]   # only completed for revenue analysis
    print(f"✅  Loaded {len(df):,} completed orders")
    return df


# ── 1. Basic Stats ──────────────────────────────────────────
def basic_stats(df):
    print("\n" + "═"*50)
    print("  BASIC STATISTICS")
    print("═"*50)
    print(f"  Total Revenue   : ₹{df['amount'].sum():,.0f}")
    print(f"  Total Orders    : {len(df):,}")
    print(f"  Avg Order Value : ₹{df['amount'].mean():,.2f}")
    print(f"  Median Order    : ₹{df['amount'].median():,.2f}")
    print(f"  Max Order       : ₹{df['amount'].max():,.0f}")
    print(f"  Date Range      : {df['order_date'].min().date()} → {df['order_date'].max().date()}")
    print(f"  Unique Customers: {df['customer_id'].nunique():,}")
    print(f"  Unique Products : {df['product_id'].nunique():,}")
    print("═"*50 + "\n")


# ── 2. Monthly Revenue Trend ────────────────────────────────
def plot_monthly_revenue(df):
    monthly = (
        df.groupby(df["order_date"].dt.to_period("M"))["amount"]
        .sum()
        .reset_index()
    )
    monthly["order_date"] = monthly["order_date"].astype(str)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(monthly["order_date"], monthly["amount"] / 1e5,
           color=BLUE, alpha=0.85, width=0.6)
    ax.plot(monthly["order_date"], monthly["amount"] / 1e5,
            color=GREEN, linewidth=2, marker="o", markersize=4)
    ax.set_title("Monthly Revenue (in Lakhs)", fontsize=14, pad=16, color="#F8FAFC")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (₹ Lakhs)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/01_monthly_revenue.png", dpi=150)
    plt.close()
    print("  Saved: 01_monthly_revenue.png")


# ── 3. Revenue by Category ──────────────────────────────────
def plot_category_revenue(df):
    cat = df.groupby("category")["amount"].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = [BLUE, GREEN, AMBER, ROSE, "#8B5CF6"]
    bars = ax.barh(cat.index, cat.values / 1e5, color=colors[:len(cat)], height=0.5)
    for bar, val in zip(bars, cat.values):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"₹{val/1e5:.1f}L", va="center", fontsize=10, color="#F8FAFC")
    ax.set_title("Revenue by Category (₹ Lakhs)", fontsize=14, pad=16)
    ax.set_xlabel("Revenue (₹ Lakhs)")
    plt.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/02_category_revenue.png", dpi=150)
    plt.close()
    print("  Saved: 02_category_revenue.png")


# ── 4. Regional Performance ─────────────────────────────────
def plot_regional(df):
    region = df.groupby("region")["amount"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    bar_colors = [GREEN if i == 0 else BLUE for i in range(len(region))]
    ax.bar(region.index, region.values / 1e5, color=bar_colors, width=0.5)
    ax.set_title("Revenue by Region (₹ Lakhs)", fontsize=14, pad=16)
    ax.set_ylabel("Revenue (₹ Lakhs)")
    plt.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/03_regional_revenue.png", dpi=150)
    plt.close()
    print("  Saved: 03_regional_revenue.png")


# ── 5. Top 10 Customers ─────────────────────────────────────
def plot_top_customers(df):
    top = (
        df.groupby("customer_id")["amount"]
        .sum()
        .nlargest(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(top.index, top.values / 1000, color=AMBER, height=0.6)
    ax.set_title("Top 10 Customers by Revenue (₹K)", fontsize=14, pad=16)
    ax.set_xlabel("Revenue (₹ Thousands)")
    plt.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/04_top_customers.png", dpi=150)
    plt.close()
    print("  Saved: 04_top_customers.png")


# ── 6. Order Amount Distribution ────────────────────────────
def plot_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df["amount"], bins=40, color=BLUE, alpha=0.8, edgecolor="#0F172A")
    ax.axvline(df["amount"].mean(),   color=GREEN, linestyle="--", linewidth=1.5, label=f"Mean ₹{df['amount'].mean():,.0f}")
    ax.axvline(df["amount"].median(), color=AMBER, linestyle="--", linewidth=1.5, label=f"Median ₹{df['amount'].median():,.0f}")
    ax.set_title("Order Amount Distribution", fontsize=14, pad=16)
    ax.set_xlabel("Order Amount (₹)")
    ax.set_ylabel("Frequency")
    ax.legend()
    plt.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/05_amount_distribution.png", dpi=150)
    plt.close()
    print("  Saved: 05_amount_distribution.png")


# ── MAIN ─────────────────────────────────────────────────────
def main():
    print("\n╔══════════════════════════════════════════╗")
    print("║  SALES DASHBOARD — EDA                   ║")
    print("╚══════════════════════════════════════════╝\n")

    df = load_data()
    basic_stats(df)

    print("Generating charts...")
    plot_monthly_revenue(df)
    plot_category_revenue(df)
    plot_regional(df)
    plot_top_customers(df)
    plot_distribution(df)

    print(f"\n✅  All charts saved to '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    main()
