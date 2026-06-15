 🛍️ Customer Intelligence Analyzer

An interactive business intelligence dashboard that segments customers, analyzes retention patterns, and uncovers cross-selling opportunities using real-world e-commerce transaction data.

**🔗 Live Dashboard**: [customer-intelligence-analyzer.streamlit.app](https://customer-intelligence-analyzer.streamlit.app)

---

 📌 Problem Statement

Businesses often struggle to identify which customers drive the most value, which are at risk of churning, and how to grow into new markets. This project analyzes over **800,000 transactions** from a UK-based online retailer to answer:

- Who are our most valuable customers, and how much revenue do they generate?
- How well do we retain customers over time?
- Which international markets show growth potential?
- Which products are commonly bought together?

---

  📊 Key Findings

- **Pareto Effect Confirmed**: The "Champions" segment (22.1% of customers) generates approximately **68% of total revenue** (£17.7M), while the "Lost" segment (25.9% of customers) contributes only ~4%.
- **Retention Gap**: Average Month-1 retention across cohorts is **21.2%**, ranging from 15% to 49% — with no cohort sustaining above 35% retention beyond month 2.
- **International Opportunity**: Outside the UK, EIRE, the Netherlands, and Germany are the top three markets, together generating over 40% of all non-UK revenue.
- **Cross-Sell Opportunity**: Product association analysis (Apriori) found pairs with confidence up to **81.6%** and lift of **29.7** — indicating strong bundling potential for home-decor items.
- **Retention Drives Revenue**: Returning customers consistently contribute 70-85% of monthly revenue, confirming retention is the primary growth lever.

---

   🚀 Features

| Feature | Description |
|---|---|
| **RFM Segmentation** | Classifies 5,878 customers into segments (Champions, Loyal, At Risk, Lost, New) based on Recency, Frequency, and Monetary value |
| **Retention Heatmap** | Visualizes month-over-month customer retention across cohorts |
| **Geographic Analysis** | Identifies top revenue-generating markets outside the UK |
| **Business Trends** | Monthly revenue, Average Order Value, and New vs. Returning customer revenue, with year-level filtering |
| **Market Basket Analysis** | Apriori algorithm reveals frequently co-purchased products |
| **Customer Lookup** | Search any Customer ID to view their individual RFM profile and segment |

---

  🛠️ Tech Stack

- **Python** — core language
- **Pandas** — data cleaning, RFM calculation, cohort analysis
- **Plotly** — interactive visualizations
- **mlxtend** — Apriori algorithm for market basket analysis
- **Streamlit** — interactive web dashboard
- **Streamlit Community Cloud** — deployment

---

 📂 Dataset

[Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) — UCI Machine Learning Repository

Contains 1,067,371 transactions (Dec 2009 – Dec 2011) from a UK-based online retailer specializing in gift-ware. After cleaning (removing missing Customer IDs, cancellations, and invalid prices), **805,549 valid transactions** were analyzed.

---

 📁 Project Structure
├── app.py                  # Streamlit dashboard application
├── requirements.txt        # Python dependencies
├── rfm.csv                 # Customer RFM scores and segments
├── retention.csv           # Cohort retention matrix
├── segment_revenue.csv     # Revenue % by segment
├── monthly_revenue.csv     # Monthly revenue data
├── monthly_aov.csv         # Monthly average order value
├── revenue_split.csv       # New vs returning customer revenue
├── country_revenue.csv     # Revenue by country (excl. UK)
└── association_rules.csv   # Market basket analysis results

🔮 Future Enhancements

1.Customer Lifetime Value (CLV) prediction
2.Year-wise filtering across all dashboard sections
3.Automated email recommendation system per segment

👤 Author
Pritam
Built as part of a data science portfolio project.
