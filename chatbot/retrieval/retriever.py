from chatbot.database.query import query_sql_database, query_chromadb
from chatbot.database.connection import get_chromadb_connection
from chatbot.embedding.embedder import encode_query
import chromadb

def retrieve_context(collection_name, user_input):
    """Retrieve relevant context from the vector database."""
    try:
        # Get ChromaDB client and collection
        collection = get_chromadb_connection().get_collection(collection_name)
    except chromadb.errors.InvalidCollectionException:
        collection = get_chromadb_connection().create_collection(collection_name)
        print(f"Collection {collection_name} created.")

    # Create query embedding based on user input
    query_embedding = encode_query(user_input)

    # Get results from ChromaDB
    chroma_results = query_chromadb(collection_name, query_embedding)

    # Check if ChromaDB results are empty
    if is_documents_empty(chroma_results):
        # If no relevant results from ChromaDB, fallback to SQL
        print("No results from ChromaDB, querying SQL database...")
        sql_results = query_sql_database(f"SELECT TOP 5 * FROM DimProduct WHERE EnglishProductName LIKE '%{user_input}%'")  # Modify this based on your SQL schema
        context = " ".join([str(row) for row in sql_results])  # Convert SQL rows to string
    else:
        # If ChromaDB has relevant results
        context = " ".join([res["document"] for res in chroma_results["documents"] if res])  # Ensure res is not empty

    return context

def is_documents_empty(results):
    """Helper function to check if documents are empty."""
    if 'documents' in results and isinstance(results['documents'], list):
        if not results['documents'] or all(not sublist for sublist in results['documents']):
            return True
    return False
