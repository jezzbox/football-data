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

def get_lat_long(city,country):

    response = requests.get(f"http://open.mapquestapi.com/geocoding/v1/address?key={os.getenv('MAPQUEST_KEY')}&location={city},{country}")
    data = response.json()
    lat_lng = data['results'][0]['locations'][0]['latLng']
    return [lat_lng['lng'],lat_lng['lat']]

conn = postgres_conn()
#update cities
transfers_df = pd.read_csv("./CSVs/transfers_cleaned.csv",index_col=0)
countries_df = pd.read_sql("select country_id, country_name from country",conn)

city_df = transfers_df[["city","country"]].drop_duplicates()
current_cities_df = pd.read_sql("select city_id, city_name from city",conn)
merged_df = city_df.merge(countries_df, how="left",left_on="country",right_on="country_name")
merged_df = merged_df.merge(current_cities_df, how="left",left_on="city",right_on="city_name")
merged_df[['lng','lat']] = merged_df.apply(lambda x: get_lat_long(x["city"],x["country"]),axis=1,result_type='expand')

cursor = conn.cursor()
for row in merged_df[["city", "country_id","lng","lat"]][merged_df["city_id"].notna() == False].drop_duplicates().itertuples(): #lng/lat to cater to (x,y)
    cursor.execute("INSERT INTO city (city_name, country_id,city_location) VALUES(%s, %s, point(%s,%s))", (row[1], row[2], row[3], row[4]))

conn.commit()
cursor.close()
conn.close()

#update countries
# cursor = conn.cursor()
# for country in city_df["country"].drop_duplicates().dropna():
#     cursor.execute("INSERT INTO country(country_name) VALUES(%s)", [country])
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

# current_players_df = pd.read_sql("select person_id, first_name,surname,other_names from person where role='player'", conn)
# df = current_players_df.merge(transfers_df,how="left", on = ["first_name","surname"])
# print(df[(df["first_name"] == 'danny') & (df["surname"] == 'ward')])
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


