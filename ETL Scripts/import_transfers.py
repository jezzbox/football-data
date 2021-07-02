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

# Add teams
transfers_df = pd.read_csv("./CSVs/player_transfers_cleaned.csv",index_col=0)
joined_df = pd.DataFrame([],columns=["team"])
left_df = pd.DataFrame([],columns=["team"])
joined_df["team"] = transfers_df["joined"].str.lower().str.strip()
left_df["team"] = transfers_df["left"].str.lower().str.strip()

teams_df = pd.concat([joined_df,left_df]).drop_duplicates()

current_teams_df = pd.read_sql("select official_team_name from team", conn)
teams_df = teams_df.merge(current_teams_df, how="left", left_on="team", right_on="official_team_name")
teams_df = teams_df[teams_df["official_team_name"].notna() == False].dropna(subset=["team"])

cursor = conn.cursor()
for row in teams_df.itertuples():
    cursor.execute("INSERT INTO team(official_team_name) VALUES(%s)", [row[1]])

conn.commit()
cursor.close()
conn.close()

# link players
