import chromadb
import json
import os
from datetime import datetime
import pyodbc
from sqlalchemy import create_engine

# Define the connection string
connection_string = "mssql+pyodbc:/sa:sa@DESKTOP-0AGEURK\SQLEXPRESS\AdventureWorksDW2019?driver=ODBC+Driver+17+for+SQL+Server"

# Replace <username>, <password>, <server>, and <database> with your actual credentials
# For example:
# connection_string = "mssql+pyodbc://sa:yourpassword@localhost/AdventureWorks?driver=ODBC+Driver+17+for+SQL+Server"

# Create an engine
engine = create_engine(connection_string)

# Test the connection by running a simple query
with engine.connect() as connection:
    result = connection.execute("SELECT TOP 5 * FROM DimProduct")
    for row in result:
        print(row)

# Code for ChromaDB
client = chromadb.Client()
collection = client.get_or_create_collection("knowledge_base")
def query_database(query_embedding):
    """Query the vector database with an embedding."""
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

def add_documents(documents,embeddings):
    """Add documents to the vector database."""
    for i, doc in enumerate(documents):
        collection.add(
            documents=[doc],
            metadatas = [{"id":i}],
            embeddings=[embeddings[i]]
        )

# Directory to store logs
LOG_DIR = "chat_logs"
os.makedirs(LOG_DIR, exist_ok=True)

def save_interaction(user_input, response):
    """
    Save user-chatbot interaction to a JSON file.
    
    Args:
        user_input (str): The message from the user.
        response (str): The chatbot's response.
    """
    interaction = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "response": response,
    }
    log_file = os.path.join(LOG_DIR, "interactions.json")

    # Append to JSON file
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            data = json.load(file)
    else:
        data = []

    data.append(interaction)

    with open(log_file, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Saved interaction: {interaction}")

def get_adventureworks_connection():
    """Establishes a connection to the AdventureWorks database."""
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=your_server_name;"  # Replace with your SQL Server's name
        "Database=AdventureWorks;"  # Your AdventureWorks database name
        "Trusted_Connection=yes;"
    )
    return conn

def fetch_products():
    """Fetches product data from the AdventureWorks database."""
    conn = get_adventureworks_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ProductID, Name, ProductNumber, Color FROM Production.Product WHERE Color IS NOT NULL")
    
    rows = cursor.fetchall()
    product_data = []
    
    for row in rows:
        product_data.append({
            "ProductID": row.ProductID,
            "Name": row.Name,
            "ProductNumber": row.ProductNumber,
            "Color": row.Color
        })
    
    conn.close()
    return product_data