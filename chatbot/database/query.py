from chatbot.database.connection import get_mssqlserver_connection
from sqlalchemy import text
def query_sql_database(query):
    """Query the SQL Server database using SQLAlchemy and return both the column names and rows, including column names as the first row."""
    connection = None
    try:
        connection = get_mssqlserver_connection()
        if connection:
            print("Verifying query...", query)
            result = connection.execute(text(query))
            
            # Get column names (the keys of the result set)
            column_names = list(result.keys())# if hasattr(result, 'keys') else []
            print(f"Column Names: {column_names}")
            input('Press Enter to continue...')
            # Fetch all rows of the result set
            rows = result.fetchall()

            # Prepend column names as the first row
            result_set = [column_names] + rows if rows else [column_names]
            
            return result_set
        else:
            print("Failed to get connection.")
            return []  # Return empty list if connection fails
    except Exception as e:
        print("SQL Query failed:", e)
        return []  # Return empty list in case of error
    finally:
        if connection:
            connection.close()  # Ensure the connection is closed after the query