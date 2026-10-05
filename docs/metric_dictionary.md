# Commercial Business Metric Dictionary

This document defines all primary commercial and operational KPIs used throughout the analytics platform, SQL analytical views, and AI copilot.

---

### 1. Gross Merchandise Value (GMV)
- **Definition**: Total monetary value of merchandise sold over a specified period before deductions (returns, discounts, cancellations).
- **Formula**: `SUM(price)` for non-cancelled / delivered orders.
- **SQL Implementation**:
  ```sql
  SELECT SUM(price) AS gmv
  FROM order_items oi
  JOIN orders o ON oi.order_id = o.order_id
  WHERE o.order_status NOT IN ('canceled', 'unavailable');
  ```
- **Business Interpretation**: Primary top-line revenue indicator reflecting commercial transaction volume.
- **Known Limitations**: Excludes freight/shipping fees and does not account for post-delivery refunds unless specifically captured in returns logs.

---

### 2. Average Order Value (AOV)
- **Definition**: Average revenue generated per distinct order.
- **Formula**: `GMV / Total Orders`
- **SQL Implementation**:
  ```sql
  SELECT SUM(oi.price) / COUNT(DISTINCT o.order_id) AS aov
  FROM orders o
  JOIN order_items oi ON o.order_id = oi.order_id
  WHERE o.order_status = 'delivered';
  ```
- **Business Interpretation**: Measures purchasing basket size; higher AOV indicates effective cross-selling or higher-ticket product mixes.
- **Known Limitations**: Sensitive to outlier high-value single transactions in low-volume categories.

---

### 3. Repeat-Purchase Rate
- **Definition**: Percentage of unique customers who placed more than one order across the dataset lifespan.
- **Formula**: `(Customers with > 1 orders) / (Total Unique Customers) * 100`
- **SQL Implementation**:
  ```sql
  WITH customer_orders AS (
      SELECT customer_unique_id, COUNT(DISTINCT order_id) AS order_cnt
      FROM customers c
      JOIN orders o ON c.customer_id = o.customer_id
      WHERE o.order_status = 'delivered'
      GROUP BY customer_unique_id
  )
  SELECT
      COUNT(CASE WHEN order_cnt > 1 THEN 1 END) * 100.0 / COUNT(*) AS repeat_purchase_rate
  FROM customer_orders;
  ```
- **Business Interpretation**: Core loyalty and customer lifetime value (LTV) metric.
- **Known Limitations**: In marketplace e-commerce platforms like Olist, repeat purchase rates are typically low (around 3–5%) due to customer acquisition driven by broad search rather than brand loyalty.

---

### 4. On-Time Delivery Rate
- **Definition**: Percentage of delivered orders that reached the customer on or before the estimated delivery date.
- **Formula**: `(Delivered orders where order_delivered_customer_date <= order_estimated_delivery_date) / (Total Delivered Orders) * 100`
- **SQL Implementation**:
  ```sql
  SELECT
      COUNT(CASE WHEN order_delivered_customer_date <= order_estimated_delivery_date THEN 1 END) * 100.0
      / COUNT(*) AS on_time_delivery_rate
  FROM orders
  WHERE order_status = 'delivered'
    AND order_delivered_customer_date IS NOT NULL
    AND order_estimated_delivery_date IS NOT NULL;
  ```
- **Business Interpretation**: Logistics and fulfillment health indicator; late deliveries directly depress review scores.
- **Known Limitations**: Does not measure whether the delivery estimate itself was unrealistically wide.

---

### 5. Freight Ratio
- **Definition**: Proportion of freight charges relative to the total order merchandise value.
- **Formula**: `SUM(freight_value) / SUM(price)`
- **SQL Implementation**:
  ```sql
  SELECT SUM(freight_value) / NULLIF(SUM(price), 0) AS freight_ratio
  FROM order_items;
  ```
- **Business Interpretation**: Assesses logistics friction. High freight ratios in distant states (e.g., North/Northeast Brazil) suppress conversion.
- **Known Limitations**: Freight costs vary significantly with volumetric weight, not just item price.

---

### 6. Workload Index (Account Management)
- **Definition**: Synthetic composite score measuring account manager operational load across their assigned sellers.
- **Formula**: `(0.4 * Normalized Seller Count) + (0.35 * Normalized GMV) + (0.25 * Normalized Order Volume)`
- **SQL Implementation**: Computed in analytical view `v_territory_summary`.
- **Business Interpretation**: Balances commercial attention so high-volume or high-complexity seller portfolios are evenly distributed.
- **Known Limitations**: Does not include subjective factors like seller relationship difficulty or ticket resolution time.
