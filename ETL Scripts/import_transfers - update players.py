from dotenv import load_dotenv
import os
import pandas as pd
import psycopg2
import numpy as np
import requests

load_dotenv()


def postgres_conn():
    conn = psycopg2.connect(dbname=os.getenv('PG_DBNAME'),
                            user=os.getenv('PG_USER'),
                            password=os.getenv('PG_PASSWORD'),
                            host=os.getenv('PG_HOSTNAME'),
                            port=os.getenv('PG_PORT'))
    return conn


conn = postgres_conn()
# update cities
transfers_df = pd.read_csv("./CSVs/transfers_cleaned.csv", index_col=0)
player_df = transfers_df[["first_name", "surname",
                          "other_names", "dob", "height","city","country","position"]].drop_duplicates()
city_df = pd.read_sql(
    """select city_id, city_name, country_name from city
        left join country on city.country_id = country.country_id""", conn)
player_df["date_of_birth"] = player_df["dob"]
df = player_df.merge(city_df, how="left", left_on=["city","country"],right_on=["city_name","country_name"])
df["role"] = 'player'
df["position"] = df["position"].str.lower().str.strip()
df["city_id"]
df = df.where(pd.notnull(df), None)
cursor = conn.cursor()
for row in df[["first_name","surname","other_names","city_id","date_of_birth","role","height","country","position"]].drop_duplicates().dropna(subset=["first_name"]).itertuples(): #lng/lat to cater to (x,y)
    cursor.execute("insert into person(first_name,surname,other_names,city_id,date_of_birth,role,height,nationality,football_position) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (row[1], row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))

conn.commit()
cursor.close()
conn.close()
