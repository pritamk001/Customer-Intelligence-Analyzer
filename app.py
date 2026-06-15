import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Customer Intelligence Analyzer", layout="wide")

st.title("🛍️ Customer Intelligence Analyzer")
st.markdown("RFM Segmentation & Business Insights Dashboard")

# Load data
rfm = pd.read_csv('rfm.csv')
retention = pd.read_csv('retention.csv', index_col=0)
segment_revenue = pd.read_csv('segment_revenue.csv')
monthly_revenue = pd.read_csv('monthly_revenue.csv')
monthly_aov = pd.read_csv('monthly_aov.csv')
revenue_split = pd.read_csv('revenue_split.csv')
country_revenue = pd.read_csv('country_revenue.csv')
rules = pd.read_csv('association_rules.csv')

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{rfm.shape[0]:,}")
col2.metric("Total Revenue", f"£{rfm['Monetary'].sum():,.0f}")
col3.metric("Champions %", f"{(rfm['Segment']=='Champions').mean()*100:.1f}%")
col4.metric("Avg Order Value", f"£{monthly_aov['AOV'].mean():.2f}")

st.markdown("---")

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["RFM Segments", "Retention", "Geography", "Trends", "Market Basket", "Customer Lookup"])

if page == "RFM Segments":
    st.subheader("Customer Segments")
    seg_counts = rfm['Segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(seg_counts, names='Segment', values='Count', title='Customer Distribution')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.bar(segment_revenue, x='Segment', y='Monetary', title='Revenue % by Segment')
        st.plotly_chart(fig2, use_container_width=True)

    st.info(f"📊 **Key Finding**: The Champions segment ({(rfm['Segment']=='Champions').sum():,} customers, {(rfm['Segment']=='Champions').mean()*100:.1f}% of the base) generates approximately £{rfm[rfm['Segment']=='Champions']['Monetary'].sum():,.0f} — about 68% of total revenue (£{rfm['Monetary'].sum():,.0f}). In contrast, the Lost segment ({(rfm['Segment']=='Lost').sum():,} customers) contributes only ~4% of revenue. This concentration means retention efforts on a relatively small group could protect the majority of revenue.")

elif page == "Retention":
    st.subheader("Customer Retention Heatmap")
    fig3 = px.imshow(retention, labels=dict(x="Months Since First Purchase", y="Cohort Month", color="Retention %"),
                      color_continuous_scale="Blues", text_auto=True, aspect="auto")
    fig3.update_layout(height=600)
    st.plotly_chart(fig3, use_container_width=True)

    avg_m1_retention = retention['1'].mean()
    st.info(f"📊 Key Finding: Across all cohorts, Month-1 retention averages **{avg_m1_retention:.1f}%**, ranging from ~15% to 49% depending on the cohort. No cohort sustains retention above 35% beyond month 2 — indicating an opportunity for structured re-engagement campaigns.")

elif page == "Geography":
    st.subheader("Top Markets (Excluding UK)")
    fig4 = px.bar(country_revenue, x=country_revenue.columns[0], y=country_revenue.columns[1], title="Revenue by Country")
    st.plotly_chart(fig4, use_container_width=True)

    top3_revenue = country_revenue.iloc[:3, 1].sum()
    st.info(f"📊 Key Finding: Outside the UK, the top 3 markets (EIRE, Netherlands, Germany) together generate approximately £{top3_revenue:,.0f} — over 40% of all non-UK revenue. These represent the clearest opportunities for international expansion.")

elif page == "Trends":
    st.subheader("Business Trends")

    monthly_revenue['Year'] = monthly_revenue['InvoiceMonth'].str[:4]
    monthly_aov['Year'] = monthly_aov['InvoiceMonth'].str[:4]
    revenue_split['Year'] = revenue_split['InvoiceMonth'].str[:4]

    years = sorted(monthly_revenue['Year'].unique())
    selected_year = st.selectbox("Select Year", ["All"] + years)

    chart_choice = st.radio("Select metric to view", ["Monthly Revenue", "Average Order Value", "New vs Returning Customers"], horizontal=True)

    mr = monthly_revenue if selected_year == "All" else monthly_revenue[monthly_revenue['Year'] == selected_year]
    ma = monthly_aov if selected_year == "All" else monthly_aov[monthly_aov['Year'] == selected_year]
    rs = revenue_split if selected_year == "All" else revenue_split[revenue_split['Year'] == selected_year]

    if chart_choice == "Monthly Revenue":
        fig5 = px.line(mr, x='InvoiceMonth', y='TotalPrice', title='Monthly Revenue', markers=True)
        st.plotly_chart(fig5, use_container_width=True)
    elif chart_choice == "Average Order Value":
        fig6 = px.line(ma, x='InvoiceMonth', y='AOV', title='Average Order Value Trend', markers=True)
        st.plotly_chart(fig6, use_container_width=True)
    else:
        fig7 = px.bar(rs, x='InvoiceMonth', y='TotalPrice', color='CustomerType', title='New vs Returning Revenue', barmode='stack')
        st.plotly_chart(fig7, use_container_width=True)

    avg_returning_pct = revenue_split[revenue_split['CustomerType']=='Returning']['TotalPrice'].sum() / revenue_split['TotalPrice'].sum() * 100
    st.info(f"📊 Key Finding: Returning customers contribute approximately **{avg_returning_pct:.1f}%** of total revenue, confirming that retention — not new acquisition — drives performance. Average Order Value stays around £{monthly_aov['AOV'].mean():.2f}.")

elif page == "Market Basket":
    st.subheader("Frequently Bought Together")
    st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))

    top_rule = rules.iloc[0]
    st.info(f"📊 Key Finding: The strongest product association has a confidence of **{top_rule['confidence']*100:.1f}%** and a lift of **{top_rule['lift']:.1f}** — customers buying one item are over {top_rule['lift']:.0f}x more likely to buy the paired item than by chance. This supports bundling strategies.")

else:
    st.subheader("Customer Lookup")
    st.write("Enter a Customer ID below to view their RFM profile and assigned segment.")

    st.caption(f"📌 For reference, the average customer has a Recency of {rfm['Recency'].mean():.0f} days, Frequency of {rfm['Frequency'].mean():.1f} orders, and Monetary value of £{rfm['Monetary'].mean():.2f}.")

    customer_id = st.number_input("Customer ID", value=12346, step=1)
    customer_data = rfm[rfm['Customer ID'] == customer_id]

    if not customer_data.empty:
        row = customer_data.iloc[0]
        st.markdown(f"### Segment: **{row['Segment']}**")

        col1, col2, col3 = st.columns(3)
        col1.metric("Recency", f"{int(row['Recency'])} days")
        col2.metric("Frequency", f"{int(row['Frequency'])} orders")
        col3.metric("Monetary", f"£{row['Monetary']:.2f}")

        scores_df = pd.DataFrame({
            'Metric': ['Recency Score', 'Frequency Score', 'Monetary Score'],
            'Score': [row['R_score'], row['F_score'], row['M_score']]
        })
        fig8 = px.bar(scores_df, x='Metric', y='Score', range_y=[0,5], title="RFM Scores (1-5 scale)")
        st.plotly_chart(fig8, use_container_width=True)
    else:
        st.warning("No record found for this Customer ID. Try IDs such as 12346, 12347, or 12348.")
