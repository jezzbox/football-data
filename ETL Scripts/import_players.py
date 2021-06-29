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

players_df = pd.read_csv("./CSVs/players.csv",index_col=0)
players_df["height"] = pd.to_numeric(players_df["height"].apply(lambda x: x * 100),errors="coerce")
players_df = players_df.where(pd.notnull(players_df), None)

cursor = conn.cursor()
for row in players_df[['first_name', 'surname', 'other_names', 'date_of_birth', 'role', 'height', 'nationality', 'football_position']].drop_duplicates(subset=['first_name','surname','other_names','date_of_birth','nationality'],keep='last').itertuples():
    cursor.execute("INSERT INTO person (first_name, surname, other_names, date_of_birth, role, height, nationality, football_position) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))


conn.commit()
cursor.close()
conn.close()