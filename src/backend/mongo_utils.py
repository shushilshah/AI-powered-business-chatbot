from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = "bizbuddy_AI"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]


def fetch_data_from_mongo(collection_name: str, query: dict = {}, limit: int = 1000) -> pd.DataFrame:
    """Fetch data from MongoDB collection and return as a Pandas DataFrame."""
    collection = db[collection_name]
    cursor = collection.find(query).limit(limit)
    data = list(cursor)

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    if '_id' in df.columns:
        df.drop(columns=['_id'], inplace=True)
    return df
