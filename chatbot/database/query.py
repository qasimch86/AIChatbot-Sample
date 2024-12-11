from chatbot.database.connection import get_mssqlserver_connection
from sqlalchemy import text

def query_sql_database(query):
    """Query the SQL Server database using SQLAlchemy."""
    # Parse the user input to extract conditions
    try:
        connection = get_mssqlserver_connection()
        if connection:
            print("Verifying query...", query)
            result = connection.execute(query)
            # print(f"result: {result}")
            rows = result.fetchall()
            return rows if rows else []
        else:
            print("Failed to get connection.")
            return [] 
    except Exception as e:
        print("SQL Query failed:", e)
        return []
    finally:
        if connection:
            connection.close()  # Ensure the connection is closed after the query