import pyodbc
from sqlalchemy import create_engine
import chromadb

# Define the connection string for SQL Server
connection_string = "mssql+pyodbc://sa:sa@DESKTOP-0AGEURK\\SQLEXPRESS/TestDB3?driver=ODBC+Driver+17+for+SQL+Server"

# Create an engine
engine = create_engine(connection_string)

# Test the connection
def get_mssqlserver_connection():
    try:
        connection = engine.connect()
        print("Connection successful!")
        return connection
    except Exception as e:
        print("Connection failed:", e)
        return None

# Initialize ChromaDB client and collection
client = chromadb.PersistentClient(path="F:\\PythonWork\\AI Chatbot\\data")

def get_chromadb_connection():
    """Establish a connection to ChromaDB."""
    # You could also initialize your collections here if needed
    return client

# Test the connections
if __name__ == "__main__":
    # Test connection
    get_mssqlserver_connection()
    # Test ChromaDB connection
    get_chromadb_connection()
