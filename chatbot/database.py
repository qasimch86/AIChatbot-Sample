import chromadb
import json
import os
from datetime import datetime


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