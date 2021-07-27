from dotenv import load_dotenv
import os
import pandas as pd
import psycopg2
import numpy as np

load_dotenv()

def postgres_conn():
    conn = psycopg2.connect(dbname=os.getenv('PG_DBNAME'),
                            user=os.getenv('PG_USER'),
                            password=os.getenv('PG_PASSWORD'),
                            host=os.getenv('PG_HOSTNAME'),
                            port=os.getenv('PG_PORT'))
    return conn

conn = postgres_conn()
transfers_df = pd.read_csv("./CSVs/transfers_cleaned.csv",index_col=0)

city_df = transfers_df[["city","country"]].drop_duplicates()

#update countries
cursor = conn.cursor()
for country in city_df["country"].drop_duplicates().dropna():
    cursor.execute("INSERT INTO country(country_name) VALUES(%s)", [country])
conn.commit()
cursor.close()
conn.close()



