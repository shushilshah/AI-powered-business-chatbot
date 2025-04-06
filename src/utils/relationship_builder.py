import pandas as pd


def build_dataset_relationship(datasets: dict) -> dict:
    """
    Automatically merge datasets based on known keys.
    : param datasets: Dictionary containing multiple datasets.
    :return: Dictionary with merged datasets and relationships.
    """
    merged_data = {}

    if "orders" in datasets and "customers" in datasets:
        merged_data["orders_customers"] = pd.merge(
            datasets["orders"], datasets["customers"], on='customer_id', how='left')

    if "orders" in datasets and "reviews" in datasets:
        merged_data["orders_reviews"] = pd.merge(
            datasets["orders"], datasets["reviews"], on="product_id", how='left')

    if "orders" in datasets and "support_tickets" in datasets:
        merged_data["orders_tickets"] = pd.merge(
            datasets["orders"], datasets["support_tickets"], on="order_id", how='left')

    return merged_data
