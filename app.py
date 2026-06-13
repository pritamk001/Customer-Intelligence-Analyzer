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

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["RFM Segments", "Retention", "Geography", "Trends", "Market Basket"])

with tab1:
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

with tab2:
    st.subheader("Customer Retention Heatmap")
    fig3 = px.imshow(retention, labels=dict(x="Months Since First Purchase", y="Cohort Month", color="Retention %"),
                      color_continuous_scale="Blues", text_auto=True, aspect="auto")
    fig3.update_layout(height=600)
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.subheader("Top Markets (Excluding UK)")
    fig4 = px.bar(country_revenue, x=country_revenue.columns[0], y=country_revenue.columns[1], title="Revenue by Country")
    st.plotly_chart(fig4, use_container_width=True)

with tab4:
    st.subheader("Business Trends")
    fig5 = px.line(monthly_revenue, x='InvoiceMonth', y='TotalPrice', title='Monthly Revenue', markers=True)
    st.plotly_chart(fig5, use_container_width=True)
    
    fig6 = px.line(monthly_aov, x='InvoiceMonth', y='AOV', title='Average Order Value Trend', markers=True)
    st.plotly_chart(fig6, use_container_width=True)
    
    fig7 = px.bar(revenue_split, x='InvoiceMonth', y='TotalPrice', color='CustomerType', title='New vs Returning Revenue', barmode='stack')
    st.plotly_chart(fig7, use_container_width=True)

with tab5:
    st.subheader("Frequently Bought Together")
    st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))
