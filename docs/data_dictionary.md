# 📖 Data Dictionary

Complete column-level documentation for all tables in the Sales Dashboard project.

---

## Table: `orders`

| Column | Type | Description | Example |
|---|---|---|---|
| order_id | VARCHAR | Unique order identifier | ORD-0001 |
| customer_id | VARCHAR | FK → customers table | CUST-101 |
| product_id | VARCHAR | FK → products table | PROD-501 |
| sales_rep_id | VARCHAR | FK → sales_reps table | REP-01 |
| amount | NUMERIC | Final selling price (INR) | 29990.00 |
| order_date | DATE | Date order was placed | 2024-12-28 |
| status | VARCHAR | Completed / Pending / Cancelled | Completed |
| order_month | SMALLINT | Extracted month number (1–12) | 12 |
| order_quarter | SMALLINT | Extracted quarter (1–4) | 4 |
| order_year | SMALLINT | Extracted year | 2024 |
| order_day_of_week | VARCHAR | Day name | Friday |
| is_repeat_customer | SMALLINT | 1 if customer has >1 order, else 0 | 1 |

---

## Table: `customers`

| Column | Type | Description | Example |
|---|---|---|---|
| customer_id | VARCHAR | Unique customer identifier | CUST-101 |
| customer_name | VARCHAR | Full name | Rahul Sharma |
| city | VARCHAR | City of residence | Delhi |
| region | VARCHAR | North / South / East / West | North |
| segment | VARCHAR | Premium / Standard / Budget | Premium |
| join_date | DATE | Date customer registered | 2022-03-01 |
| email | VARCHAR | Email address | rahul@email.com |
| tenure_days | INTEGER | Days since join_date (as of cleaning date) | 1002 |
| tenure_years | NUMERIC | tenure_days / 365 | 2.7 |

---

## Table: `products`

| Column | Type | Description | Example |
|---|---|---|---|
| product_id | VARCHAR | Unique product identifier | PROD-501 |
| product_name | VARCHAR | Full product name | Sony WH-1000XM5 |
| category | VARCHAR | Electronics / Clothing / Home Goods / Sports | Electronics |
| cost_price | NUMERIC | Procurement cost (INR) | 18000.00 |
| mrp | NUMERIC | Maximum retail price (INR) | 29990.00 |
| brand | VARCHAR | Brand name | Sony |
| profit_margin_pct | NUMERIC | (mrp - cost_price) / mrp × 100 | 39.98 |

---

## Table: `sales_reps`

| Column | Type | Description | Example |
|---|---|---|---|
| rep_id | VARCHAR | Unique rep identifier | REP-01 |
| rep_name | VARCHAR | Full name | Arvind Kapoor |
| region | VARCHAR | Assigned region | North |
| team | VARCHAR | Team name | Team A |
| annual_target | NUMERIC | Annual revenue target (INR) | 5000000.00 |
| join_date | DATE | Date rep joined | 2021-01-01 |

---

## Engineered Features (added during cleaning)

| Feature | Source Table | Formula |
|---|---|---|
| profit_margin_pct | products | (mrp − cost_price) / mrp × 100 |
| tenure_days | customers | TODAY − join_date |
| tenure_years | customers | tenure_days / 365 |
| order_month | orders | EXTRACT(MONTH FROM order_date) |
| order_quarter | orders | EXTRACT(QUARTER FROM order_date) |
| is_repeat_customer | orders | COUNT(orders per customer) > 1 |
| profit_amount | orders (enriched) | amount − cost_price |
