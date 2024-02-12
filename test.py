import faker
from faker_vehicle import VehicleProvider
import pandas as pd
from sqlalchemy import create_engine
import os

server = ''
database = ''
username = ''
password = ''

# Create a connection string
connection_string = f"mysql+pymysql://{username}:{password}@{server}/{database}"

# use sqlalchemy to create a connection to the database
engine = create_engine(connection_string)

conn = engine.connect()
# Display the first 5 rows of the customers table
print(pd.read_sql('SELECT * FROM customers LIMIT 5', conn).to_markdown())

print(pd.read_sql('SELECT * FROM cars', conn).to_markdown())