from click import pause
from chatbot.database import query_database
from chatbot.database import client
from chatbot.embedder import encode_query
import chromadb

def retrieve_context(collection_name,user_input):
    """Retrieve relevant context from the vector database."""
    try:
        collection = client.get_collection(collection_name)
    except chromadb.errors.InvalidCollectionException:
        collection = client.create_collection(collection_name)
        print(f"Collection {collection_name} created.")

    # Create query embedding based on user input
    query_embedding = encode_query(user_input)

    # Get results from the database based on user input
    results = query_database(collection,query_embedding)

    # Check if results are empty
    if is_documents_empty(results):
        context = "No results found."
        print(context)
    else:
        context = " ".join([res["document"] for res in results["documents"] if res])  # Ensure res is not empty
    return context

def is_documents_empty(results):
    # Check if 'documents' key exists and is a list
    if 'documents' in results and isinstance(results['documents'], list):
        # Check if the list is empty or contains empty sublists
        if not results['documents'] or all(not sublist for sublist in results['documents']):
            return True
    return False