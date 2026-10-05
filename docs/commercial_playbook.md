# Commercial Playbook & Decision Support Guidelines

This playbook defines operational policies, interpretation guidelines for data science models, and rules for query refusal when confidence or evidence is insufficient.

---

## 1. Customer Segmentation Rules (RFM)
- **Recency**: Days elapsed between a customer's latest order and the snapshot reference date.
- **Frequency**: Count of distinct completed orders placed by the customer.
- **Monetary**: Total spend across all completed orders.
- **Action Playbook**:
  - *Champions / High Value*: Target for early product launches, loyalty benefits, and exclusive offers.
  - *At Risk*: Re-engagement campaigns with personalized category discounts.
  - *One-Time Buyers*: Post-purchase cross-sell emails triggered within 30 days of initial fulfillment.

---

## 2. Propensity Model Interpretation
- **Target Variable**: Probability that a customer returns to place an order within the next 90 days.
- **Threshold Policy**:
  - Target top 2 deciles (top 20% highest propensity scores) for marketing budget efficiency.
  - Avoid blasting low-propensity cohorts where ROI on discounts is negative.

---

## 3. Demand Forecasting Guidelines
- **Granularity**: Category-level weekly or monthly aggregations.
- **Model Selection**: SARIMAX for trends with seasonal cycles; Moving Average for low-volume sparse categories.
- **Uncertainty & Caveats**:
  - The dataset spans 2016 to late 2018 (~2 years total).
  - Multi-year seasonality patterns cannot be established with high statistical certainty on a 2-year window. All forecasts include confidence intervals.

---

## 4. Refusal & Limitation Guidelines
The AI Copilot MUST refuse or provide strict caveats when:
1. Asked to make speculative financial guarantees or predictions outside historical data ranges.
2. Asked for individual personally identifiable information (PII).
3. The RAG retriever finds no documentation above the similarity score threshold (`SIMILARITY_THRESHOLD = 0.45`).
4. A query cannot be verified against the approved schema tables.
