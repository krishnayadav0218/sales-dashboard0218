# 📊 Sales Analytics Dashboard

> End-to-end data analytics project — from raw CSV to interactive business intelligence dashboard using SQL, Python, and Power BI.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/PostgreSQL-14+-336791?logo=postgresql&logoColor=white)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green)
![Stars](https://img.shields.io/github/stars/yourname/sales-dashboard?style=social)

---

## 📌 Problem Statement

A mid-sized e-commerce company was making decisions based on monthly Excel reports that were:
- Outdated (3-day delay in reporting)
- Inconsistent (5 departments, no unified view)
- Manual (error-prone, time-consuming)

**Goal:** Build a centralized, automated Sales Dashboard that gives real-time KPIs, trend analysis, and actionable insights — reducing reporting time from 3 days to under 30 seconds.

---

## 📁 Project Structure

```
sales-dashboard-project/
│
├── data/
│   ├── raw/                    # Original CSV files (as received)
│   │   ├── orders_raw.csv
│   │   ├── customers_raw.csv
│   │   ├── products_raw.csv
│   │   └── sales_reps_raw.csv
│   │
│   └── cleaned/                # After Python cleaning
│       ├── orders_clean.csv
│       ├── customers_clean.csv
│       ├── products_clean.csv
│       └── sales_reps_clean.csv
│
├── sql/
│   ├── 01_create_tables.sql    # Schema creation
│   ├── 02_insert_data.sql      # Data loading
│   ├── 03_monthly_revenue.sql  # Revenue trend query
│   ├── 04_top_customers.sql    # LTV & segmentation
│   ├── 05_regional_perf.sql    # Region vs target
│   ├── 06_product_analysis.sql # Category breakdown
│   └── 07_churn_analysis.sql   # Customer churn
│
├── python/
│   ├── requirements.txt        # Python dependencies
│   ├── 01_data_cleaning.py     # Full cleaning pipeline
│   ├── 02_eda.py               # Exploratory Data Analysis
│   ├── 03_visualizations.py    # matplotlib/seaborn charts
│   └── 04_etl_pipeline.py      # Automated ETL to PostgreSQL
│
├── dashboard/
│   └── sales_dashboard.html    # Interactive HTML dashboard
│
├── docs/
│   ├── data_dictionary.md      # Column descriptions
│   ├── business_insights.md    # Key findings & recommendations
│   └── screenshots/            # Dashboard images
│
└── README.md
```

---

## 🗄️ Dataset

| Table | Rows | Columns | Source |
|---|---|---|---|
| orders | 45,312 | order_id, customer_id, product_id, amount, date, status | CRM Export |
| customers | 12,847 | customer_id, name, city, region, segment, join_date | CRM Export |
| products | 1,204 | product_id, name, category, cost_price, mrp | ERP System |
| sales_reps | 86 | rep_id, name, region, team, target | HR System |

---

## 🧹 Data Cleaning Steps

1. **Remove Duplicates** — 1,247 duplicate order_ids removed
2. **Handle Missing Values** — NULL regions filled via customer join; 89 NULL amounts dropped
3. **Standardize Dates** — 3 formats unified to ISO 8601
4. **Fix Categorical Issues** — 14 spelling variants in category column standardized
5. **Outlier Treatment** — IQR method; 23 flagged, 18 retained (bulk orders), 5 corrected
6. **Feature Engineering** — Added: profit_margin, order_month, order_quarter, is_repeat_customer

---

## 📊 Key Business Insights

- 📈 Electronics revenue grew **+34% YoY** — highest performing category
- 🗺️ North region achieved **118% of target**; South only 71%
- 👑 Top 5% customers (Platinum) drive **38% of total revenue**
- 📅 December peak: **₹3.2M** (13% of annual revenue)
- 🔄 Churn rate reduced from **8.5% → 6.4%** after loyalty program
- ⚡ Order processing improved: **48 hrs → 22 minutes**

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/yourname/sales-dashboard.git
cd sales-dashboard-project
```

### 2. Install Python Dependencies
```bash
pip install -r python/requirements.txt
```

### 3. Run Data Cleaning
```bash
python python/01_data_cleaning.py
```

### 4. Set Up PostgreSQL Database
```bash
psql -U postgres -f sql/01_create_tables.sql
psql -U postgres -f sql/02_insert_data.sql
```

### 5. Run ETL Pipeline
```bash
python python/04_etl_pipeline.py
```

### 6. Open Dashboard
Open `dashboard/sales_dashboard.html` in any browser — no server required.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python (pandas, matplotlib) | Data cleaning & EDA |
| PostgreSQL | Data warehousing & SQL analysis |
| Power BI | Interactive dashboard |
| HTML/CSS/JS | Web dashboard version |

---

## 📄 License

MIT License — free to use, modify, and distribute with attribution.

---

## 🙋 Author

Built as a portfolio project to demonstrate end-to-end data analytics skills.  
Feel free to ⭐ star the repo if you found it useful!
