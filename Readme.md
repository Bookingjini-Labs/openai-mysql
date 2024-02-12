# AI SQL Query Generator

This project leverages the power of OpenAI's GPT-3 model to generate SQL queries from natural language prompts. Additionally, it includes scripts to create and populate a MySQL database with mock data for testing.

## Project Structure

The project is composed of several Python scripts:

- **ai.py**: This is the primary script that interfaces with the OpenAI API to generate SQL queries. It also has the capability to translate the results into natural language.

- **fakecust.py, fakesales.py, fakecar.py**: These scripts are responsible for generating mock data for customers, car sales, and cars respectively. They also populate a MySQL database with this data.

- **test.py**: This script is utilized to test the database connection and display some data from the database.

## How to Use

1. Establish a MySQL database and update the connection details in the scripts.

2. Execute fakecust.py, fakesales.py, fakecar.py to populate the database with mock data.

3. Run ai.py to interact with the OpenAI API. You can use the `run_query` function to generate SQL queries. For instance:
