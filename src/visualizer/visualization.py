# import pandas as pd
# import streamlit as st
# import plotly.express as px
# from src.backend.mongo_utils import fetch_data_from_mongo


# @st.cache_data
# def load_data():
#     return {
#         "orders": pd.DataFrame(fetch_data_from_mongo("orders")),
#         "reviews": pd.DataFrame(fetch_data_from_mongo("reviews")),
#         "customers": pd.DataFrame(fetch_data_from_mongo("customers")),
#         "support": pd.DataFrame(fetch_data_from_mongo("support_tickets"))
#     }


# def show_kpis(orders_df):
#     if not all(col in orders_df.columns for col in ["price", "quantity", "product", "category"]):
#         st.warning("Missing columns in orders dataset.")
#         return

#     total_sales = (orders_df["price"] * orders_df["quantity"]).sum()
#     top_product = orders_df["product"].value_counts().idxmax()
#     top_category = orders_df["category"].value_counts().idxmax()

#     col1, col2, col3 = st.columns(3)
#     col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
#     col2.metric("📦 Most Popular Product", top_product)
#     col3.metric("🧩 Top Category", top_category)


# def sales_over_time(orders_df):
#     orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
#     orders_df["month"] = orders_df["order_date"].dt.to_period("M").astype(str)
#     monthly_sales = orders_df.groupby("month").apply(
#         lambda x: (x["price"] * x["quantity"]).sum()).reset_index(name="Total Sales")
#     fig = px.line(monthly_sales, x="month", y="Total Sales",
#                   title="📈 Monthly Sales Trend")
#     st.plotly_chart(fig, use_container_width=True)


# def product_sales_bar(orders_df):
#     product_sales = orders_df.groupby("product").apply(
#         lambda x: (x["price"] * x["quantity"]).sum()).reset_index(name="Sales")
#     top_products = product_sales.sort_values("Sales", ascending=False).head(10)
#     fig = px.bar(top_products, x="product", y="Sales",
#                  title="🏆 Top 10 Product Sales")
#     st.plotly_chart(fig, use_container_width=True)


# def review_distribution(reviews_df):
#     fig = px.histogram(reviews_df, x="rating", nbins=5,
#                        title="⭐ Rating Distribution")
#     st.plotly_chart(fig, use_container_width=True)


# def customer_lifetime_value(orders_df):
#     clv = orders_df.groupby('customer_id').apply(
#         lambda x: (x['price'] * x['quantity']).sum()).reset_index(name='CLV')
#     st.write("Customer Lifetime Value (Top 5):",
#              clv.sort_values("CLV", ascending=False).head())


# def active_customers(orders_df, customers_df):
#     orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
#     recent_orders = orders_df[orders_df['order_date']
#                               >= pd.Timestamp.now() - pd.DateOffset(days=30)]
#     active_count = recent_orders['customer_id'].nunique()
#     st.metric("🧍 Active Customers (30 days)", active_count)


# def order_distribution_by_category(orders_df):
#     category_sales = orders_df.groupby('category').apply(
#         lambda x: (x['price'] * x['quantity']).sum()).reset_index(name='Total Sales')
#     st.bar_chart(category_sales.set_index("category"))


# def top_products_by_revenue(orders_df):
#     product_sales = orders_df.groupby('product').apply(
#         lambda x: (x['price'] * x['quantity']).sum()).reset_index(name='Revenue')
#     st.write("Top Products by Revenue:", product_sales.sort_values(
#         'Revenue', ascending=False).head(10))


# def ticket_resolution_time(support_df):
#     resolved = support_df.dropna(subset=['resolved_at']).copy()
#     resolved['resolved_at'] = pd.to_datetime(resolved['resolved_at'])
#     resolved['created_at'] = pd.to_datetime(resolved['created_at'])
#     resolved['resolution_time'] = (
#         resolved['resolved_at'] - resolved['created_at']).dt.days
#     avg_time = resolved['resolution_time'].mean()
#     st.metric("⏱️ Avg Resolution Time", f"{avg_time:.2f} days")


# def review_analysis(reviews_df):
#     avg_rating = reviews_df.groupby(
#         'product')['rating'].mean().reset_index(name='Avg Rating')
#     top_reviewed = reviews_df['product'].value_counts().head(
#         10).reset_index(name='Review Count')
#     st.write("Average Rating per Product:", avg_rating.sort_values(
#         "Avg Rating", ascending=False).head(5))
#     st.write("Top 10 Most Reviewed Products:", top_reviewed)


# def generate_visualization():
#     st.subheader("📊 Business Insights Dashboard")
#     data = load_data()

#     orders_df = data["orders"]
#     reviews_df = data["reviews"]
#     customers_df = data["customers"]
#     support_df = data["support"]

#     with st.spinner("Analyzing..."):
#         show_kpis(orders_df)

#         tab1, tab2, tab3, tab4 = st.tabs(
#             ["Sales", "Reviews", "Customers", "Support"])

#         with tab1:
#             sales_over_time(orders_df)
#             product_sales_bar(orders_df)
#             order_distribution_by_category(orders_df)
#             top_products_by_revenue(orders_df)

#         with tab2:
#             review_distribution(reviews_df)
#             review_analysis(reviews_df)

#         with tab3:
#             customer_lifetime_value(orders_df)
#             active_customers(orders_df, customers_df)

#         with tab4:
#             ticket_resolution_time(support_df)


import pandas as pd
import streamlit as st
import plotly.express as px
from src.backend.mongo_utils import fetch_data_from_mongo


@st.cache_data
def load_data():
    return {
        "orders": pd.DataFrame(fetch_data_from_mongo("orders")),
        "reviews": pd.DataFrame(fetch_data_from_mongo("reviews")),
        "customers": pd.DataFrame(fetch_data_from_mongo("customers")),
        "support": pd.DataFrame(fetch_data_from_mongo("support_tickets"))
    }


def show_kpis(orders_df):
    if not all(col in orders_df.columns for col in ["selling_price", "quantity", "product", "category"]):
        st.warning("Missing columns in orders dataset.")
        return

    total_sales = (orders_df["selling_price"] * orders_df["quantity"]).sum()
    top_product = orders_df["product"].value_counts().idxmax()
    top_category = orders_df["category"].value_counts().idxmax()

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
    col2.metric("📦 Most Popular Product", top_product)
    col3.metric("🧩 Top Category", top_category)


def sales_over_time(orders_df):
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
    orders_df["month"] = orders_df["order_date"].dt.to_period("M").astype(str)
    monthly_sales = orders_df.groupby("month").apply(
        lambda x: (x["selling_price"] * x["quantity"]).sum()).reset_index(name="Total Sales")
    fig = px.line(monthly_sales, x="month", y="Total Sales",
                  title="📈 Monthly Sales Trend")
    st.plotly_chart(fig, use_container_width=True)


def product_sales_bar(orders_df):
    product_sales = orders_df.groupby("product").apply(
        lambda x: (x["selling_price"] * x["quantity"]).sum()).reset_index(name="Sales")
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
        lambda x: (x['selling_price'] * x['quantity']).sum()).reset_index(name='CLV')
    st.write("Customer Lifetime Value (Top 5):",
             clv.sort_values("CLV", ascending=False).head())


def active_customers(orders_df, customers_df):
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
    recent_orders = orders_df[orders_df['order_date']
                              >= pd.Timestamp.now() - pd.DateOffset(days=30)]
    active_count = recent_orders['customer_id'].nunique()
    st.metric("🧍 Active Customers (30 days)", active_count)


def order_distribution_by_category(orders_df):
    category_sales = orders_df.groupby('category').apply(
        lambda x: (x['selling_price'] * x['quantity']).sum()).reset_index(name='Total Sales')
    st.bar_chart(category_sales.set_index("category"))


def top_products_by_revenue(orders_df):
    product_sales = orders_df.groupby('product').apply(
        lambda x: (x['selling_price'] * x['quantity']).sum()).reset_index(name='Revenue')
    st.write("Top Products by Revenue:", product_sales.sort_values(
        'Revenue', ascending=False).head(10))


def ticket_resolution_time(support_df):
    resolved = support_df.dropna(subset=['resolved_at']).copy()
    resolved['resolved_at'] = pd.to_datetime(resolved['resolved_at'])
    resolved['created_at'] = pd.to_datetime(resolved['created_at'])
    resolved['resolution_time'] = (
        resolved['resolved_at'] - resolved['created_at']).dt.days
    avg_time = resolved['resolution_time'].mean()
    st.metric("⏱️ Avg Resolution Time", f"{avg_time:.2f} days")


def review_analysis(reviews_df):
    avg_rating = reviews_df.groupby(
        'product')['rating'].mean().reset_index(name='Avg Rating')
    top_reviewed = reviews_df['product'].value_counts().head(
        10).reset_index(name='Review Count')
    st.write("Average Rating per Product:", avg_rating.sort_values(
        "Avg Rating", ascending=False).head(5))
    st.write("Top 10 Most Reviewed Products:", top_reviewed)


# New Insights

def sales_by_country(orders_df, customers_df):
    merged = orders_df.merge(
        customers_df, left_on="customer_id", right_on="customer_id", how="left")
    country_sales = merged.groupby("location").apply(
        lambda x: (x["selling_price"] * x["quantity"]).sum()).reset_index(name="Total Sales")
    top_5_location = country_sales.sort_values(
        "Total Sales", ascending=False).head(5)
    fig = px.bar(top_5_location.sort_values("Total Sales", ascending=False),
                 x="location", y="Total Sales", title="🌍 Sales by Location")
    st.plotly_chart(fig, use_container_width=True)


def repeat_vs_onetime_customers(orders_df):
    customer_order_counts = orders_df["customer_id"].value_counts()
    repeat = (customer_order_counts > 1).sum()
    onetime = (customer_order_counts == 1).sum()
    fig = px.pie(names=["Repeat", "One-time"], values=[repeat, onetime],
                 title="🔁 Repeat vs. One-time Customers")
    st.plotly_chart(fig, use_container_width=True)


def support_tickets_by_type(support_df):
    if "issue_type" in support_df.columns:
        issue_counts = support_df["issue_type"].value_counts().reset_index()
        issue_counts.columns = ["Issue Type", "Count"]
        fig = px.bar(issue_counts, x="Issue Type", y="Count",
                     title="🛠️ Support Tickets by Issue Type")
        st.plotly_chart(fig, use_container_width=True)


def top_spending_customers(orders_df, customers_df):
    clv = orders_df.groupby("customer_id").apply(
        lambda x: (x["selling_price"] * x["quantity"]).sum()).reset_index(name="Total Spent")
    top_customers = clv.sort_values("Total Spent", ascending=False).head(10)
    merged = top_customers.merge(customers_df, on="customer_id", how="left")
    fig = px.bar(merged, x="name", y="Total Spent",
                 title="💎 Top Spending Customers")
    st.plotly_chart(fig, use_container_width=True)


def avg_rating_by_category(orders_df, reviews_df):
    merged = orders_df.merge(
        reviews_df, on=["customer_id", "product"], how="inner")
    cat_rating = merged.groupby(
        "category")["rating"].mean().reset_index(name="Avg Rating")
    fig = px.bar(cat_rating.sort_values("Avg Rating", ascending=False),
                 x="category", y="Avg Rating", title="📚 Average Rating by Category")
    st.plotly_chart(fig, use_container_width=True)


# Full Dashboard Generation
def generate_visualization():
    st.subheader("📊 Business Insights Dashboard")
    data = load_data()

    orders_df = data["orders"]
    reviews_df = data["reviews"]
    customers_df = data["customers"]
    support_df = data["support"]

    with st.spinner("Analyzing..."):
        show_kpis(orders_df)

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Sales", "Reviews", "Customers", "Support"])

        with tab1:
            sales_over_time(orders_df)
            product_sales_bar(orders_df)
            order_distribution_by_category(orders_df)
            top_products_by_revenue(orders_df)
            sales_by_country(orders_df, customers_df)

        with tab2:
            review_distribution(reviews_df)
            review_analysis(reviews_df)
            avg_rating_by_category(orders_df, reviews_df)

        with tab3:
            customer_lifetime_value(orders_df)
            active_customers(orders_df, customers_df)
            repeat_vs_onetime_customers(orders_df)
            top_spending_customers(orders_df, customers_df)

        with tab4:
            ticket_resolution_time(support_df)
            support_tickets_by_type(support_df)


def analyze_data_and_respond(question: str, data: dict) -> str:
    """Analyze the loaded data to answer specific questions"""
    question_lower = question.lower()

    if "sales" in question_lower:
        return analyze_sales_data(question_lower, data["orders"])
    elif "review" in question_lower or "rating" in question_lower:
        return analyze_review_data(question_lower, data["reviews"])
    # elif "customer" in question_lower:
    #     return analyze_customer_data(question_lower, data["customers"], data["orders"])
    # elif "support" in question_lower or "ticket" in question_lower:
    #     return analyze_support_data(question_lower, data["support"])

    return "I can analyze sales, reviews, customer, or support data. Which would you like to know about?"


# Add to visualization.py or a new analysis.py file
def analyze_sales_data(question: str, orders_df: pd.DataFrame) -> str:
    if "trend" in question:
        orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
        monthly_sales = orders_df.groupby(orders_df["order_date"].dt.to_period("M"))[
            "selling_price"].sum()
        if len(monthly_sales) > 1:
            last_month = monthly_sales[-1]
            prev_month = monthly_sales[-2]
            change = ((last_month - prev_month) / prev_month) * 100
            return f"Sales trend: {'up' if change > 0 else 'down'} by {abs(change):.1f}% last month."
        return "Not enough data to determine sales trends."

    if "top product" in question or "best selling" in question:
        top_product = orders_df["product"].value_counts().idxmax()
        return f"The top selling product is {top_product}."

    if "category" in question:
        top_category = orders_df["category"].value_counts().idxmax()
        return f"The most popular category is {top_category}."

    return "I can tell you about sales trends, top products, or categories. What specifically interests you?"


def analyze_review_data(question: str, reviews_df: pd.DataFrame) -> str:
    if "average" in question or "rating" in question:
        avg_rating = reviews_df["rating"].mean()
        return f"Our average rating is {avg_rating:.1f} out of 5."

    if "negative" in question or "complaint" in question:
        negative_reviews = reviews_df[reviews_df["rating"] < 3]
        if not negative_reviews.empty:
            common_complaints = negative_reviews["comments"].value_counts().head(
                3).index.tolist()
            return "Main complaints:\n- " + "\n- ".join(common_complaints)
        return "Great news! No significant negative feedback recently."

    return "I can analyze average ratings or common complaints. What would you like to know?"
