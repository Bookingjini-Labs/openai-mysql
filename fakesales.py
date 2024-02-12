import os
import faker
from faker_vehicle import VehicleProvider
import pandas as pd
from sqlalchemy import create_engine

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

def generate_sales_data(n):
    """Generate n rows of fake sales data."""
    cars = pd.read_sql('SELECT ProductID, Price FROM cars', engine)
    customer_ids = pd.read_sql('SELECT CustomerID FROM customers', engine)
    data = []
    for _ in range(n):
        car = cars.sample().iloc[0]
        quantity = fake.random_int(min=1, max=10)
        discount = fake.random_int(min=0, max=10)
        total = float(car['Price']) * quantity * (1 - discount/100)
        data.append([fake.unique.random_number(digits=5),
                     customer_ids.sample().iloc[0]['CustomerID'],
                     car['ProductID'],
                     quantity,
                     car['Price'],
                     discount,
                     total,
                     fake.name(),
                     fake.date_between(start_date='-1y', end_date='today')])
    return data

# Generate 10K rows of data
data = generate_sales_data(10000)

# Store in the database
df = pd.DataFrame(data, columns=['SalesID', 'CustomerID', 'ProductID', 'Quantity', 'Price', 'DiscountPercent', 'Total', 'SalesAgent', 'Date'])
with engine.connect() as conn:
    df.to_sql('carsales', conn, if_exists='replace', index=False)