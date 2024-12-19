from chatbot.llm.llm import generate_query_llm
from chatbot.intent_parser.parser import extract_sql_query

def generate_sql_query(user_input, schema):
    """Generate SQL query using the LLM."""

    # LLM API request to generate SQL query
    response = generate_query_llm(user_input, schema)

    # Extract SQL query
    final_query = response#extract_sql_query(response)

    # print(f"This is the code start from here: \n\n\n\n\n {final_query} \n\n\n\n Code ends here.\n\n\n\n")
    if not final_query or final_query.strip() == "":
        return "Sorry, I couldn't generate a valid SQL query."
    
    # Get the query from the response
    return final_query

