import openai
from chatbot.llm.llm import generate_query_LLM

def generate_sql_query(user_input, schema):
    """Generate SQL query using the LLM."""
        
    # OpenAI API request to generate SQL query
    response = generate_query_LLM(user_input, schema)
    if not response or response.strip() == "":
        return "Sorry, I couldn't generate a valid SQL query."
    # Get the query from the response
    return response

