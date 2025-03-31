import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from src.logger import logging
from src.exception import MyException

load_dotenv()


# mongodb credentials
mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB")


if not all([mongo_uri, mongo_db]):
    raise MyException(
        "MongoDB credentials are not set in the environment variables.")

datasets = {
    "customers": "src/data/customers.csv",
    "orders": "src/data/orders.csv",
    "support_tickets": "src/data/support_tickets.csv",
    "reviews": "src/data/reviews.csv"
}

# Connect to MongoDB
try:
    client = MongoClient(mongo_uri)
    db = client[mongo_db]

    for collection_name, file_path in datasets.items():
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        df = pd.read_csv(file_path)
        df = df.where(pd.notnull(df), None)

        # Get Collection
        collection = db[collection_name]

        # Delete existing data
        collection.delete_many({})

        # Insert new data
        collection.insert_many(df.to_dict(orient='records'))
        logging.info(f"{collection_name} data stored in MongoDB successfully!")

except MyException as e:
    print(f"Error connecting to MongoDB: {e}")
