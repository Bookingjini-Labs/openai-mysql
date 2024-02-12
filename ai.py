import openai
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


openai.api_key = ''

# Return the table names in the database
def get_table_names():
    with engine.connect() as conn:
        query = '''
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='ai'
        '''
        return pd.read_sql(query, conn)['TABLE_NAME'].tolist()
    

# Get 5 random rows from a table and store them in a dataframe
def get_random_rows(table, n=5):
    with engine.connect() as conn:
        query = f'SELECT * FROM {table} ORDER BY RAND() LIMIT {n}'
        return pd.read_sql(query, conn)
    

# Call get_random_rows() for each table, and store the results as markdown in a list
markdown = []
for table in get_table_names():
    markdown.append(f'### {table}')
    markdown.append(get_random_rows(table).to_markdown())
    markdown.append('\n')

# Join the markdown list into a single string
table_definitions = '\n'.join(markdown)
table_definitions = table_definitions + '\n---\nReturn the SQL Query for:'

GPT_MODEL = "gpt-3.5-turbo"

def generate_query(prompt: str, table_definitions: str):
    """Answers a query using GPT"""
    system = "You are an SQL generator that only returns SQL statements and no natural language. Given the table names, definitions and a prompt."
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": table_definitions+prompt}
    ]

    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0
    )

    response_message = response["choices"][0]["message"]["content"]
    print(response_message)
    return response_message

def parse_result_in_natural_language(prompt: str, result: str):
    '''
    Parses the result of a query into natural language
    '''
    completion = prompt + '\n' + result
    messages = [
        {"role" : "system", "content" : "You translate the result of a query and a prompt into natural language."},
        {"role": "user", "content": completion}
    ]
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages = messages,
        temperature=0
    )
    return response["choices"][0]["message"]["content"]

def run_query(prompt: str, return_natural_language: bool = False):
    query = generate_query(prompt, table_definitions)
    with engine.connect() as conn:
        result =  pd.read_sql(query, conn).to_markdown()

    if return_natural_language:
        result = parse_result_in_natural_language(prompt, result)

    return result

# print(run_query('What is the most expensive car?', return_natural_language=True))
# print(run_query('in which year Chevrolet Tahoe was made?', return_natural_language=True))
# print(run_query('who are the customers who have bought cars of price > 10000?', return_natural_language=True))
print(run_query('List 5 customer name and car details who have bought cars of price greater than 10000?', return_natural_language=True))