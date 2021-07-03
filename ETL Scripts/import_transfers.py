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
# joined_df = pd.DataFrame([],columns=["team"])
# left_df = pd.DataFrame([],columns=["team"])
# joined_df["team"] = transfers_df["joined"].str.lower().str.strip()
# left_df["team"] = transfers_df["left"].str.lower().str.strip()

# teams_df = pd.concat([joined_df,left_df]).drop_duplicates()

# current_teams_df = pd.read_sql("select official_team_name from team", conn)
# teams_df = teams_df.merge(current_teams_df, how="left", left_on="team", right_on="official_team_name")
# teams_df = teams_df[teams_df["official_team_name"].notna() == False].dropna(subset=["team"])

# cursor = conn.cursor()
# for row in teams_df.itertuples():
#     cursor.execute("INSERT INTO team(official_team_name) VALUES(%s)", [row[1]])

# conn.commit()
# cursor.close()
# conn.close()

# link players
# current_players_df = pd.read_sql("select person_id, first_name,surname,other_names from person where role='player'", conn)
# df = current_players_df.merge(transfers_df,how="left", on = ["first_name","surname"])
# print(df[(df["season"].notna()) & (((df["first_name"] == 'danny') & (df["surname"] == 'ward')) == False) & (((df["first_name"] == 'lucas') & (df["surname"].notna() == False)) == False)])
# current_teams_df = pd.read_sql("select official_team_name, team_id from team", conn)
# df["left"] = df["left"].str.lower().str.strip()
# df["joined"] = df["joined"].str.lower().str.strip()
# merged_df = df.merge(current_teams_df,how="left", left_on="joined", right_on="official_team_name")
# merged_df["joined_id"] = merged_df["team_id"]
# merged_df2 = merged_df.merge(current_teams_df,how="left", left_on="left", right_on="official_team_name")
# merged_df2["left_id"] = merged_df2["team_id_y"]
# del df
# df = merged_df2[["person_id","left_id","joined_id","mv","fee","fee_details","date_from","date_to"]]
# df = df.where(pd.notnull(df), None)
# cursor = conn.cursor()
# for row in df.dropna(subset=["date_from"]).itertuples():
#     cursor.execute("INSERT INTO contract(person_id, team_from_id,team_to_id,market_value,fee,fee_details,contract_start,contract_end) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", [row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]])

# conn.commit()
# cursor.close()
# conn.close()

current_players_df = pd.read_sql("select person_id, first_name,surname,other_names from person where role='player'", conn)
df = current_players_df.merge(transfers_df,how="left", on = ["first_name","surname"])
print(df[(df["first_name"] == 'danny') & (df["surname"] == 'ward')])
current_teams_df = pd.read_sql("select official_team_name, team_id from team", conn)
df["left"] = df["left"].str.lower().str.strip()
df["joined"] = df["joined"].str.lower().str.strip()
merged_df = df.merge(current_teams_df,how="left", left_on="joined", right_on="official_team_name")
merged_df["joined_id"] = merged_df["team_id"]
merged_df2 = merged_df.merge(current_teams_df,how="left", left_on="left", right_on="official_team_name")
merged_df2["left_id"] = merged_df2["team_id_y"]
del df
df = merged_df2[["person_id","left_id","joined_id","mv","fee","fee_details","date_from","date_to"]]
df = df.where(pd.notnull(df), None)
cursor = conn.cursor()
for row in df.dropna(subset=["date_from"]).itertuples():
    cursor.execute("INSERT INTO contract(person_id, team_from_id,team_to_id,market_value,fee,fee_details,contract_start,contract_end) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", [row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]])

conn.commit()
cursor.close()
conn.close()


