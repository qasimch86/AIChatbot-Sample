from chatbot.database.query import query_sql_database
from chatbot.query.generate_sql_query import generate_sql_query  # New import
from chatbot.embedding.embedder import encode_query
from data.load_csv import load_schema_from_csv
import os
os.chdir(os.getcwd())
def retrieve_context(user_input):
    """Retrieve relevant context from the database based on user input."""
    # Define schema here or pass it dynamically
    schema = load_schema_from_csv('./data/schema_adventureworks.csv')
    
    # Generate SQL query using LLM
    query = generate_sql_query(user_input, schema)
    # print(f"Generated SQL query: {query}")

    # Execute the query against the database
    sql_results = query_sql_database(query)
    # print(f'sql_results: {sql_results}')
    # Format the SQL results
    context = format_sql_result(sql_results)
    return context

def format_sql_result(results):
    """Format SQL query results into a user-friendly context."""
    formatted_results = []
    for row in results:
        formatted_results.append(f"Product ID: {row[0]}, Code: {row[1]}, Name: {row[2]}, Price: {row[3]}")
    return "\n".join(formatted_results)