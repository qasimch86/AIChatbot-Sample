from click import pause
from chatbot.embedder import encode_query
from chatbot.database import query_database
import chromadb

# Initialize ChromaDB client and collection
client = chromadb.Client()
collection = client.get_collection("adventureworks_products")


def retrieve_context(user_input):
    """Retrieve relevant context from the vector database."""
    query_embedding = encode_query(user_input)
    results = query_database(query_embedding)
    
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


# def retrieve_context(user_input):
#     """Retrieve relevant context from the vector database."""
#     query_embedding = encode_query(user_input)
#     # print("Query Embedding:", query_embedding)
#     results = query_database(query_embedding)
#     # print("Results:", results)  # Add this line to inspect results
#     # Assuming results is a list of dictionaries, and each dictionary has a "document" key
#     if is_documents_empty(results):
#         context = "No results found."
#         print(context)
#     else:
#         context = " ".join([res["document"] for res in results["documents"]])
#     return context

# def is_documents_empty(results):
#     # Check if 'documents' key exists and is a list
#     if 'documents' in results and isinstance(results['documents'], list):
#         # Check if the list is empty or contains only empty sublists
#         if not results['documents'] or all(not sublist for sublist in results['documents']):
#             return True
#     return False