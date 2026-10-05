# Database Schema Reference

This reference documents the relational tables and analytical views available for Text-to-SQL query generation and business analytics.

---

## 1. Primary Base Tables (Olist Public Dataset)

### `orders`
- `order_id` (VARCHAR(32), Primary Key): Unique order identifier.
- `customer_id` (VARCHAR(32), Foreign Key -> customers.customer_id): Key to the customer record for this order.
- `order_status` (VARCHAR(20)): 'delivered', 'shipped', 'canceled', 'invoiced', 'processing', 'unavailable'.
- `order_purchase_timestamp` (DATETIME): Timestamp when order was placed.
- `order_approved_at` (DATETIME): Payment approval timestamp.
- `order_delivered_carrier_date` (DATETIME): Timestamp when package was handed to carrier.
- `order_delivered_customer_date` (DATETIME): Actual delivery date to the customer.
- `order_estimated_delivery_date` (DATETIME): Promised delivery date shown to customer.

### `order_items`
- `order_id` (VARCHAR(32), Composite PK, FK -> orders.order_id): Order identifier.
- `order_item_id` (INT, Composite PK): Sequential item number within order.
- `product_id` (VARCHAR(32), FK -> products.product_id): Product identifier.
- `seller_id` (VARCHAR(32), FK -> sellers.seller_id): Seller fulfilling the item.
- `shipping_limit_date` (DATETIME): Seller shipping deadline.
- `price` (DECIMAL(10,2)): Item price in BRL.
- `freight_value` (DECIMAL(10,2)): Shipping cost for item.

### `customers`
- `customer_id` (VARCHAR(32), Primary Key): Per-order customer identifier.
- `customer_unique_id` (VARCHAR(32)): Real-world unique individual identifier.
- `customer_zip_code_prefix` (VARCHAR(10)): 5-digit postal code.
- `customer_city` (VARCHAR(100)): City name.
- `customer_state` (VARCHAR(2)): 2-letter state code (e.g. SP, RJ, MG).

### `products`
- `product_id` (VARCHAR(32), Primary Key): Product identifier.
- `product_category_name` (VARCHAR(100)): Category in Portuguese.
- `product_category_name_english` (VARCHAR(100)): Translated category in English.
- `product_weight_g` (FLOAT): Weight in grams.
- `product_length_cm` (FLOAT), `product_height_cm` (FLOAT), `product_width_cm` (FLOAT): Dimensions.

### `sellers`
- `seller_id` (VARCHAR(32), Primary Key): Seller identifier.
- `seller_zip_code_prefix` (VARCHAR(10)): Postal code.
- `seller_city` (VARCHAR(100)): Seller city.
- `seller_state` (VARCHAR(2)): Seller state code.

### `order_payments`
- `order_id` (VARCHAR(32), FK -> orders.order_id): Order identifier.
- `payment_sequential` (INT): Payment sequence index.
- `payment_type` (VARCHAR(20)): 'credit_card', 'boleto', 'voucher', 'debit_card'.
- `payment_installments` (INT): Number of installments.
- `payment_value` (DECIMAL(10,2)): Amount paid.

### `order_reviews`
- `review_id` (VARCHAR(32), Primary Key): Review identifier.
- `order_id` (VARCHAR(32), FK -> orders.order_id): Associated order.
- `review_score` (INT): Customer satisfaction rating from 1 to 5.
- `review_creation_date` (DATETIME): Review sent timestamp.
- `review_answer_timestamp` (DATETIME): Review submission timestamp.

---

## 2. Synthetic B2B Commercial Layer

### `account_managers`
- `manager_id` (VARCHAR(32), Primary Key): Account manager identifier.
- `manager_name` (VARCHAR(100)): Full name.
- `region` (VARCHAR(50)): Assigned territory (Southeast, South, Northeast, North, Center-West).
- `quarterly_quota` (DECIMAL(12,2)): Sales revenue target.
- `is_synthetic` (BOOLEAN): Always `TRUE`.

### `seller_territory_assignments`
- `seller_id` (VARCHAR(32), Primary Key, FK -> sellers.seller_id): Seller identifier.
- `manager_id` (VARCHAR(32), FK -> account_managers.manager_id): Assigned account manager.
- `assignment_strategy` (VARCHAR(50)): 'geographic_naive' or 'balanced_workload'.
- `is_synthetic` (BOOLEAN): Always `TRUE`.

---

## 3. Analytical Views

### `v_order_facts`
Denormalized order-item grain table joining orders, customers, products, sellers, payments, and reviews.

### `v_customer_summary`
Customer unique grain table aggregating lifetime orders, GMV, AOV, first/last purchase timestamps, and average review score.

### `v_seller_summary`
Seller grain table aggregating lifetime GMV, order volume, on-time delivery rate, and assigned account manager.

### `v_category_sales`
Monthly category sales aggregation for trend analysis and demand forecasting.

### `v_territory_summary`
Account manager workload metrics including seller count, GMV under management, order volume, and composite workload index.
