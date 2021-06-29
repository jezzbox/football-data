# football-data

This repository will document my football-data database as well as the webscraping and cleaning I have done in Python.


## Web scraping / data cleaning
All my python code will be presented as jupyter notebooks which you can find in the Notebooks folder. I will mostly be using Beautiful soup and pandas.

## ETL Scripts
ETL scripts will be saved in the ETL Scripts folder. I will be using psycopg2 to connect to the db with python.
## Database
Database: Postgres\
Diagram: https://lucid.app/lucidchart/1789da0d-5953-4e61-89a6-76f27eb64080/view

I have made this database intentionally complex to test my skills. Taking into account things such as a team possibly sharing a stadium, changing stadiums, having detail such as timestamps of goals, more than one country being eligible in a league, and contract information.

The database will be built to accomodate multiple leagues in different countries, however I will first only be adding the last 3 seasons of the premier league.

### Tables:

table | description | related table(s)
------------ | ------------- | -------------
country | unique countries |
city | unique cities | country
stadium | unique stadiums | city
home_stadium | the stadiums home team including history | team, stadium
league | unique leagues | 
season | unique seasons of leagues | league
country_eligibility | many to many relationship between leagues and countries | league, country
team | unique teams | city
person | unique players, managers | city
contract | player and manager contracts, also serves to relate players to a team | person, team
match | the matches played | team (home + away), stadium,season
match_attendance | players who played in the match, including time sent on/off | person, team, match
match_activity | goals, cards, set pieces including timestamp | match_attendance

### Naming conventions:
type | convention
------------ | -------------
case | snake_case
table names | singular
primary keys | *{table_name}_pkey*
foreign keys | *{related_table_name}_fkey*
unique constraint | *uq_{column_name}_key*
