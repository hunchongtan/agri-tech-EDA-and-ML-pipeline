import sqlite3
import pandas as pd
import os
import requests

DATA_DIR = "data"
DB_ORIGINAL = os.path.join(DATA_DIR, "agri.db")
DB_PATH = os.path.join(DATA_DIR, "calls.db")
DB_URL = "https://techassessment.blob.core.windows.net/aiip5-assessment-data/agri.db"
TABLE_NAME = "farm_data"

# Make data folder
os.makedirs(DATA_DIR, exist_ok=True)

# Download and rename the database
def download_and_rename_database():
    if not os.path.exists(DB_PATH):
        response = requests.get(DB_URL)
        if response.status_code == 200:
            with open(DB_ORIGINAL, "wb") as db_file:
                db_file.write(response.content)
            os.rename(DB_ORIGINAL, DB_PATH)
        else:
            raise Exception(f"Failed to download database: {response.status_code}")

# Load data
def data_load():
    download_and_rename_database()
    try:
        conn = sqlite3.connect(DB_PATH)
        
        query = f"SELECT * FROM {TABLE_NAME}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        print("Data loaded successfully.")
        return df
    
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
        raise

if __name__ == "__main__":
    df = data_load()
    print("Preview Dataset:")
    print(df.head())
