# Dataset Guide: Olist Brazilian E-Commerce & Synthetic Commercial Layer

This project uses the public **Brazilian E-Commerce Public Dataset by Olist** supplemented by an explicitly labeled **Synthetic Account Management & Territory Layer**.

---

## 1. Real-World Data: Olist Public Dataset

### Dataset Overview
- **Source**: [Kaggle Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **Timeframe**: ~100,000 orders from 2016 to 2018 across Brazilian marketplaces.
- **Nature**: Anonymized real transaction data containing orders, order items, reviews, payments, customers, sellers, products, and geolocation.

### How to Download Manually
1. Visit the Kaggle dataset page: `https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce`
2. Download and unzip the archive.
3. Place the CSV files into `data/raw/`:
   - `olist_customers_dataset.csv`
   - `olist_geolocation_dataset.csv`
   - `olist_order_items_dataset.csv`
   - `olist_order_payments_dataset.csv`
   - `olist_order_reviews_dataset.csv`
   - `olist_orders_dataset.csv`
   - `olist_products_dataset.csv`
   - `olist_sellers_dataset.csv`
   - `product_category_name_translation.csv`

---

## 2. Synthetic Data: Account Management & Territory Layer

To model enterprise B2B commercial operations (such as account executive workload, quota management, and territory balancing), a synthetic commercial layer is generated deterministically using a fixed random seed (`seed=42`).

### Synthetic Tables
- `account_managers` (manager ID, name, email, region, quota, experience level, `is_synthetic = TRUE`)
- `seller_territory_assignments` (seller ID, assigned manager ID, assignment date, assignment status, `is_synthetic = TRUE`)
- `territory_quotas` (territory code, region, quarterly sales target, `is_synthetic = TRUE`)

### Labeling Policy
- Every record and table in the synthetic layer contains the flag `is_synthetic = TRUE`.
- Never claim or represent this synthetic layer as client or proprietary enterprise data.

---

## 3. Directory Layout

```
data/
├── README.md               <-- Dataset documentation (this file)
├── raw/                    <-- Original unedited CSV files (ignored by Git)
└── processed/              <-- Cleaned tables, engineered features, SQLite fallback db
```
