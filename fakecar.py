import os
import faker
from faker_vehicle import VehicleProvider
import pandas as pd
from sqlalchemy import create_engine

# Fetching the credentials from environment variables
server = ''
database = ''
username = ''
password = ''

# Create a connection string
connection_string = f"mysql+pymysql://{username}:{password}@{server}/{database}"

# use sqlalchemy to create a connection to the database
engine = create_engine(connection_string)

# Create a Faker instance and add vehicle provider
fake = faker.Faker()
fake.add_provider(VehicleProvider)

def generate_product_data(n):
    """Generate n rows of fake product data."""
    data = []
    for _ in range(n):
        vehicle = fake.vehicle_object()
        data.append([fake.unique.random_number(digits=5),
                     vehicle['Make'],
                     vehicle['Model'],
                     vehicle['Year'],
                     fake.pydecimal(left_digits=5, right_digits=2, positive=True, min_value=100, max_value=10000)])
    return data

# Generate 100 rows of data
data = generate_product_data(100)

# Store in the database
df = pd.DataFrame(data, columns=['ProductID', 'Brand', 'Model', 'Year', 'Price'])
with engine.connect() as conn:
    df.to_sql('cars', conn, if_exists='replace', index=False)