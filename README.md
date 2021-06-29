# football-data

This repository will document my football-data database as well as the webscraping and cleaning I have done in Python.



## Database
Database: Postgres\
Diagram: https://lucid.app/lucidchart/1789da0d-5953-4e61-89a6-76f27eb64080/view?page=0_0#

### Tables:	
table | description | type
------------ | ------------- | -------------
listings | contains all the listings and lots from the auction sites | fact
auction_sites | unique list of auction sites in the database | dimension
bottles | the bottles put up for auction | dimension
dates | date table including historic exchange rate | dimension
currencies | unique currencies | dimension
countries | unique countries | sub dimension
bottle_origins | origins of bottles. connects countries table to bottles table | junction table
stg_listings | staging table for importing data | staging table

### Naming conventions:
type | convention
------------ | -------------
case | snake_case
table names | sungular
primary keys | *{table_name}_pkey*
foreign keys | *{related_table_name}_fkey*
unique constraint | *uq_{column_name}_key*
