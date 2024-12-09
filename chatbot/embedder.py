from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def encode_query(query):
    """Generate embeddings for a query."""
    return embedder.encode(query).tolist()