from chatbot.database.query import query_sql_database
from chatbot.query.generate_sql_query import generate_sql_query  # New import
import os
os.chdir(os.getcwd())
def retrieve_context(user_input,schema):
    """Retrieve relevant context from the database based on user input."""
    
    # Generate SQL query using LLM
    query = generate_sql_query(user_input, schema)

    # Execute the query against the database
    sql_results = query_sql_database(query)


    return sql_results
