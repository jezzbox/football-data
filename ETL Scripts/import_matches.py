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

matches_df = pd.read_csv("./CSVs/matches_cleaned.csv",)
print(matches_df)
##rename afc bournemoth
matches_df['home_team'] = matches_df['home_team'].str.replace('afc bournemouth','bournemouth')
matches_df['away_team'] = matches_df['away_team'].str.replace('afc bournemouth','bournemouth')
team_df =pd.read_sql("select official_team_name,team_id from team",conn)

matches_df = pd.merge(matches_df,team_df,how='left',left_on='home_team',right_on='official_team_name')
matches_df = pd.merge(matches_df,team_df,how='left',left_on='away_team',right_on='official_team_name',suffixes=['_home','_away'])
print(matches_df[matches_df['team_id_away'].notna() ])

##rename stadiums
matches_df['stadium_name'] = matches_df['stadium_name'].str.replace('amex stadium','american express community stadium')
matches_df['stadium_name'] = matches_df['stadium_name'].str.replace('etihad stadium','city of manchester stadium')
matches_df['stadium_name'] = matches_df['stadium_name'].str.replace("john smith's stadium",'mcalpine stadium')
matches_df['stadium_name'] = matches_df['stadium_name'].str.replace('molineux stadium','molineux')
matches_df['stadium_name'] = matches_df['stadium_name'].str.replace('vitality stadium','dean court')
stadium_df =pd.read_sql("select stadium_name,stadium_id from stadium",conn)

matches_df = pd.merge(matches_df,stadium_df,how='left',on='stadium_name')

cursor = conn.cursor()
for row in matches_df[['season_id', 'matchweek', 'match_date', 'kickoff', 'stadium_id', 'team_id_home', 'team_id_away', 'referee', 'attendance', 'clock', 'home_result', 'away_result']].itertuples():
    cursor.execute("INSERT INTO match (season_id,match_number,match_date,kick_off,stadium_id,home_team_id,away_team_id,referee,attendance,clock,home_result,away_result) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],row[9],row[10],row[11],row[12]))


conn.commit()
cursor.close()
conn.close()