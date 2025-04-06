import pandas as pd
import streamlit as st
import plotly.express as px
from src.backend.mongo_utils import fetch_data_from_mongo


def load_data():
    orders = fetch_data_from_mongo("orders")
    reviews = fetch_data_from_mongo("reviews")
    customers = fetch_data_from_mongo("customers")
    support_df = fetch_data_from_mongo("support_tickets")
    return pd.DataFrame(orders), pd.DataFrame(reviews), pd.DataFrame(customers), pd.DataFrame(support_df)


def show_kpis(orders_df):
    total_sales = (orders_df["price"] * orders_df["quantity"]).sum()
    top_product = orders_df["product"].value_counts().idxmax()
    top_category = orders_df["category"].value_counts().idxmax()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💰 Total Sales", f"${total_sales:,.2f}")
    with col2:
        st.metric("📦 Most Popular Product", top_product)
    with col3:
        st.metric("🧩 Top Category", top_category)


def sales_over_time(orders_df):
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
    orders_df["month"] = orders_df["order_date"].dt.to_period("M").astype(str)
    monthly_sales = orders_df.groupby("month").apply(
        lambda x: (x["price"] * x["quantity"]).sum()).reset_index(name="Total Sales")
    fig = px.line(monthly_sales, x="month", y="Total Sales",
                  title="📈 Monthly Sales Trend")
    st.plotly_chart(fig, use_container_width=True)


def product_sales_bar(orders_df):
    product_sales = orders_df.groupby("product").apply(
        lambda x: (x["price"] * x["quantity"]).sum()).reset_index(name="Sales")
    top_products = product_sales.sort_values("Sales", ascending=False).head(10)
    fig = px.bar(top_products, x="product", y="Sales",
                 title="🏆 Top 10 Product Sales")
    st.plotly_chart(fig, use_container_width=True)


def review_distribution(reviews_df):
    fig = px.histogram(reviews_df, x="rating", nbins=5,
                       title="⭐ Rating Distribution")
    st.plotly_chart(fig, use_container_width=True)


def customer_lifetime_value(orders_df):
    clv = orders_df.groupby('customer_id').apply(
        lambda x: (x['price'] * x['quantity']).sum()).reset_index(name='CLV')
    st.write("Customer Lifetime Value (CLV):", clv.head())


def active_customers(orders_df, customers_df):
    recent_orders = orders_df[orders_df['order_date'] >=
                              pd.to_datetime('today') - pd.DateOffset(days=30)]
    active_customers = recent_orders['customer_id'].nunique()
    st.write(f"Active customers in the last 30 days: {active_customers}")


def order_distribution_by_category(orders_df):
    category_sales = orders_df.groupby('category').apply(
        lambda x: (x['price'] * x['quantity']).sum()).reset_index(name='Total Sales')
    st.write("Sales by Category:", category_sales)


def top_products_by_revenue(orders_df):
    product_sales = orders_df.groupby('product').apply(
        lambda x: (x['price'] * x['quantity']).sum()).reset_index(name='Revenue')
    top_products = product_sales.sort_values(
        'Revenue', ascending=False).head(10)
    st.write("Top Products by Revenue:", top_products)


def ticket_resolution_time(support_df):
    # Only calculate for resolved tickets
    resolved_tickets = support_df.dropna(subset=['resolved_at'])
    resolved_tickets['resolved_at'] = pd.to_datetime(
        resolved_tickets['resolved_at'])
    resolved_tickets['created_at'] = pd.to_datetime(
        resolved_tickets['created_at'])
    resolved_tickets['resolution_time'] = (
        resolved_tickets['resolved_at'] - resolved_tickets['created_at']).dt.days
    avg_resolution_time = resolved_tickets['resolution_time'].mean()
    st.write(f"Average Ticket Resolution Time: {avg_resolution_time:.2f} days")


def review_analysis(review_df):
    avg_rating = review_df.groupby(
        'product')['rating'].mean().reset_index(name='Avg Rating')
    most_reviewed = review_df['product'].value_counts().head(
        10).reset_index(name='Review Count')
    st.write("Average Rating per Product:", avg_rating)
    st.write("Top 10 Most Reviewed Products:", most_reviewed)

# Use the functions inside the dashboard


# def generate_additional_insights():
#     orders_df, reviews_df, customers_df, support_df = load_data()

    # with st.spinner("Generating additional insights..."):
    #     customer_lifetime_value(orders_df)
    #     active_customers(orders_df, customers_df)
    #     order_distribution_by_category(orders_df)
    #     top_products_by_revenue(orders_df)
    #     ticket_resolution_time(support_data)
    #     review_analysis(review_data)


def generate_visualization():
    st.subheader("📊 Business Insights Dashboard")

    orders_df, reviews_df, customers_df, support_df = load_data()

    with st.spinner("Generating insights..."):
        show_kpis(orders_df)

        st.markdown("---")
        sales_over_time(orders_df)

        st.markdown("---")
        product_sales_bar(orders_df)

        st.markdown("---")
        review_distribution(reviews_df)

        customer_lifetime_value(orders_df)
        active_customers(orders_df, customers_df)
        order_distribution_by_category(orders_df)
        top_products_by_revenue(orders_df)
        ticket_resolution_time(support_df)
        review_analysis(reviews_df)
