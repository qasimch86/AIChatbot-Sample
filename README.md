# AIChatBot
This AI Chatbot uses LLM and RAG to let organizations attach their private database with internal GPT trained model. 

1. retriever.py
Purpose: Handles retrieval of relevant documents or embeddings from your vector database based on user input.
Key Focus: Accesses pre-embedded data and retrieves information for further processing (e.g., context for LLM responses).
Example Usage:
retrieve_context(): Fetches relevant data from your ChromaDB or vector store.
2. llm.py
Purpose: Manages the interaction with the language model to generate human-like responses.
Key Focus: Processes the user query and contextual data to generate coherent responses.
Example Usage:
generate_response(): Uses LLM to create a conversational reply.
3. embedder.py
Purpose: Handles creation and storage of embeddings for data.
Key Focus: Converts text or other data into vector representations for similarity searches.
Example Usage:
embed_texts(): Embeds documents and stores them in the vector database.

4. query_builder.py
Purpose: Dynamically generates SQL queries based on user intent and extracted entities.
Key Focus: Converts structured user intents into executable database queries.
Example Functionality:
generate_query(intent, entities): Creates SQL queries like:
sql
Copy code
SELECT * FROM Products WHERE Name = 'Headset Ball Bearings';
5. intent_parser.py
Purpose: Analyzes user input to determine the user's intent and extract relevant entities.
Key Focus: Processes natural language and maps it to structured data (intents, entities).
Example Functionality:
parse_user_input("Tell me about Headset Ball Bearings") → {"intent": "get_product_info", "entities": {"product_name": "Headset Ball Bearings"}}
6. executor.py
Purpose: Executes the dynamically generated queries and retrieves results from the database.
Key Focus: Interacts with the database, runs SQL queries, and returns results.
Example Functionality:
execute_query(query): Executes the SQL query using SQLAlchemy and fetches results.
