import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

# DATE_COLUMNS = {
#     "customers": ["created_at"],
#     "orders": ["order_date"],
#     "reviews": ["review_date"],
#     "support_tickets": ["created_at","resolved_at"]
# }


class PreprocessingPipeline:
    def __init__(self, db_url, db_name, collections):
        """
        db_url: MongoDB URL
        db_name: Database Name
        collections: List of collection names to be processed
        """
        self.db_url = db_url
        self.db_name = db_name
        self.collections = collections
        self.client = MongoClient(self.db_url)
        self.db = self.client[self.db_name]
        self.data = self.load_datasets()

    def load_datasets(self):
        """"Fetch all datasets from the database collections."""
        datasets = {}
        for collection_name in self.collections:
            data_cursor = self.db[collection_name].find()
            data = pd.DataFrame(list(data_cursor))
            # data.drop(columns=['_id'], inplace=True)
            datasets[collection_name] = data

        return datasets

    def handle_missing_data(self, data):
        """Handle the missing values present in dataset"""
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        data[numerical_cols] = data[numerical_cols].fillna(
            data[numerical_cols].median())
        # for categorical data types
        categorical_cols = data.select_dtypes(include=[object]).columns
        data[categorical_cols] = data[categorical_cols].fillna(
            data[categorical_cols].mode())
        return data

    # def transform_data_types(self,data):
    #     """Transform data types for a specified dataset."""
    #     date_columns = DATE_COLUMNS.get(dataset_name, [])
    #     for col in date_columns:
    #         if col in date_columns:
    #             data[col] = pd.to_datetime(data[col],errors='coerce')
    #     return data

    def encode_categorical_columns(self, data):
        label_encoder = LabelEncoder()
        categorical_cols = data.select_dtypes(include=[object]).columns
        for col in categorical_cols:
            data[col] = label_encoder.fit_transform(data[col].astype(str))

        return data

    def text_normalization(self, data):
        text_columns = data.select_dtypes(include=[object]).columns
        for col in text_columns:
            data[col] = data[col].str.lower().str.strip()
        return data

    def run_pipeline(self):
        "Run the full pipeline on all datasets."
        cleaned_data = {}
        for collection_name, data in self.data.items():
            data = self.handle_missing_data(data)
            # data = self.transform_data_types(data)
            data = self.encode_categorical_columns(data)
            data = self.text_normalization(data)
            cleaned_data[collection_name] = data

        return cleaned_data

    def save_cleaned_data(self, cleaned_data):
        for collection_name, data in cleaned_data.items():
            data.to_csv(
                f"transformed_data/cleaned_{collection_name}.csv", index=False)


if __name__ == "__main__":
    db_url = "your mongo dn url"
    db_name = "bizbuddy_AI"
    collections = ["customers", "orders", "reviews", "support_tickets"]
    pipeline = PreprocessingPipeline(db_url, db_name, collections)
    cleaned_data = pipeline.run_pipeline()

    pipeline.save_cleaned_data(cleaned_data)
