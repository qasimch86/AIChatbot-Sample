from chatbot.database.connection import get_mssqlserver_connection, get_chromadb_connection
from sqlalchemy import text

def query_sql_database(query):
    """Query the SQL Server database using SQLAlchemy."""
    try:
        connection = get_mssqlserver_connection()
        if connection:
            print("Verifying query...")
            result = connection.execute(text(query))
            print(f"result: {result}")
            rows = result.fetchall()
            return result if result else []
        else:
            print("Failed to get connection.")
            return [] 
    except Exception as e:
        print("SQL Query failed:", e)
        return []
    finally:
        if connection:
            connection.close()  # Ensure the connection is closed after the query

def query_chromadb(collection, query_embedding):
    """Query ChromaDB with an embedding."""
    try:
        collection = get_chromadb_connection().get_collection(collection)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        return results
    except Exception as e:
        print("ChromaDB Query failed:", e)

def add_documents_to_chromadb(collection, documents, embeddings):
    """Add documents to ChromaDB."""
    try:
        collection = get_chromadb_connection().get_collection(collection)
        for i, doc in enumerate(documents):
            collection.add(
                documents=[doc],
                metadatas=[{"id": i}],
                embeddings=[embeddings[i]]
            )
    except Exception as e:
        print("Failed to add documents to ChromaDB:", e)
