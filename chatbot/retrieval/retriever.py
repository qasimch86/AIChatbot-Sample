from chatbot.database.query import query_sql_database
from chatbot.query.generate_sql_query import generate_sql_query  # New import
import os
os.chdir(os.getcwd())
def retrieve_context(user_input,schema):
    """Retrieve relevant context from the database based on user input."""
    
    # Generate SQL query using LLM
    query = generate_sql_query(user_input, schema)
    # print('Retriever: generate_sql_query')
    print(f"Generated SQL query: {query}")

    # Execute the query against the database
    sql_results = query_sql_database(query)
    # print('Retriever: sql_results')
    print(f'Retriever: sql_results: {sql_results}')

    return sql_results
