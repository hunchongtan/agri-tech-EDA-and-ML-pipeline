import sqlite3
import pandas as pd
import yaml

# Load configuration file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

DB_PATH = config["data"]["database"]
TABLE_NAME = config["data"]["table"]

def data_load():
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT * FROM {TABLE_NAME}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    print("Data loaded successfully.")
    return df

if __name__ == "__main__":
    df = data_load()
    print("Preview Dataset:")
    print(df.head())
