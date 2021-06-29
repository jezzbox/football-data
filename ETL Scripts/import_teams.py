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

# Import cities
country_df =pd.read_sql("SELECT country_id, country_name FROM country",conn)
team_df = pd.read_csv("./CSVs/teams.csv",index_col=0)

team_df["country_name"] = team_df["team"].apply( lambda x: "wales" if x == "Cardiff City" else "england")
team_df = team_df.merge(country_df, how="left", on="country_name")
team_df["city"] = team_df["city"].str.lower().str.strip() # lower case and strip any leading/trailing spaces
team_df["lat"] = pd.to_numeric(team_df["lat"]) # make sure lat/lng are numeric
team_df["lng"] = pd.to_numeric(team_df["lng"])

cursor = conn.cursor()
for row in team_df[["city", "country_id","lng","lat"]].drop_duplicates().itertuples(): #lng/lat to cater to (x,y)
    cursor.execute("INSERT INTO city (city_name, country_id,city_location) VALUES(%s, %s, point(%s,%s))", (row[1], row[2], row[3], row[4]))

conn.commit()
cursor.close()
conn.close()

# import stadiums
city_df =pd.read_sql("SELECT city_id, city_name FROM city",conn)
city_df["city"] = city_df["city_name"]
team_df["stadium"] = team_df["stadium"].str.lower().str.strip()
team_df = pd.merge(team_df,city_df,how="left",on="city")
team_df["capacity"] = pd.to_numeric(team_df["capacity"])

cursor = conn.cursor()
for row in team_df[["stadium", "city_id","capacity"]].drop_duplicates().itertuples():
    cursor.execute("INSERT INTO stadium (stadium_name, city_id,capacity) VALUES(%s, %s,%s)", (row[1], row[2],row[3]))


conn.commit()
cursor.close()
conn.close()

# import teams
team_df["team"] = team_df["team"].str.lower().str.strip()

cursor = conn.cursor()
for row in team_df[["team", "city_id"]].drop_duplicates().itertuples():
    cursor.execute("INSERT INTO team (official_team_name, city_id) VALUES(%s, %s)", (row[1], row[2]))

conn.commit()
cursor.close()
conn.close()

#import home stadiums
stadium_df =pd.read_sql("SELECT stadium_name, stadium_id FROM stadium",conn)
db_team_df =pd.read_sql("SELECT official_team_name, team_id FROM team",conn)


team_df = pd.merge(team_df,db_team_df,how="left",left_on="team", right_on = "official_team_name")
team_df = pd.merge(team_df,stadium_df,how="left",left_on="stadium", right_on = "stadium_name")
print(team_df[["stadium_id","team_id"]])

cursor = conn.cursor()
for row in team_df[["stadium_id","team_id"]].drop_duplicates().itertuples():
    cursor.execute("INSERT INTO home_stadium (stadium_id, team_id) VALUES(%s, %s)", (row[1], row[2]))


conn.commit()
cursor.close()
conn.close()