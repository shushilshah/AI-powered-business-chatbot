# src/analytics/business_queries.py

def total_sales(df):
    if 'sales' in df.columns:
        return f"💰 Total Sales: {df['sales'].sum():,.2f}"
    return "❌ 'sales' column not found in the dataset."


def most_engaging_customer(df):
    if 'customer_id' in df.columns:
        top_customer = df['customer_id'].value_counts().idxmax()
        return f"👤 Most engaging customer: {top_customer}"
    return "❌ 'customer_id' column not found."


def most_popular_product(df):
    if 'product' in df.columns:
        top_product = df['product'].value_counts().idxmax()
        return f"🔥 Most popular product: {top_product}"
    return "❌ 'product' column not found."


def highest_sales_by_country(df):
    if 'country' in df.columns and 'sales' in df.columns:
        top_country = df.groupby('country')['sales'].sum().idxmax()
        return f"🌍 Country with highest sales: {top_country}"
    return "❌ Required columns not found."
