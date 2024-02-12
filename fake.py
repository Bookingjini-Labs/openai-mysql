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

# Create a Faker instance for Belgium
fake = faker.Faker('nl_BE')
fake.add_provider(VehicleProvider)

def generate_customer_data(n):
    """Generate n rows of fake customer data."""
    data = []
    for _ in range(n):
        data.append([fake.unique.random_number(digits=5), 
                     fake.first_name(), 
                     fake.last_name(), 
                     fake.email(), 
                     fake.phone_number(), 
                     fake.street_address(), 
                     fake.city(), 
                     fake.postcode(), 
                     'Belgium'])
    return data

# Generate 10K rows of data
data = generate_customer_data(10000)

# Create a pandas DataFrame
df = pd.DataFrame(data, columns=['CustomerID', 'FirstName', 'LastName', 'Email', 'PhoneNumber', 'Address', 'City', 'PostalCode', 'Country'])

# Save the data from dataframe to SQL Server, create a connection to the database
with engine.connect() as conn:
    df.to_sql('customers', conn, if_exists='replace', index=False)