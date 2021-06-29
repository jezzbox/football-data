from dotenv import load_dotenv
import os
import pandas as pd
import psycopg2

load_dotenv()

def postgres_conn():
    conn = psycopg2.connect(dbname=os.getenv('PG_DBNAME'),
                            user=os.getenv('PG_USER'),
                            password=os.getenv('PG_PASSWORD'),
                            host=os.getenv('PG_HOSTNAME'),
                            port=os.getenv('PG_PORT'))
    return conn

conn = postgres_conn()

managers_df = pd.read_csv("./CSVs/managers.csv",index_col=0)
managers_df = managers_df.where(pd.notnull(managers_df), None)

cursor = conn.cursor()
for row in managers_df[['first_name', 'surname', 'date_of_birth', 'role','nationality']].drop_duplicates().itertuples():
    cursor.execute("INSERT INTO person (first_name, surname, date_of_birth, role, nationality) VALUES(%s, %s, %s, %s, %s)", (row[1], row[2], row[3], row[4], row[5]))


conn.commit()
cursor.close()
conn.close()