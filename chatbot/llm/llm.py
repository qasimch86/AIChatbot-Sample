from chatbot.llm.llm_huggingface import llm_huggingface

# ------------------------------------------------------------------------
# model_name = "EleutherAI/gpt-neo-1.3B"
# token = "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"
# ------------------------------------------------------------------------
# model_name="Qwen/Qwen2.5-1.5B"
# token="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"
# ------------------------------------------------------------------------
# model_name = "PipableAI/pip-sql-1.3b"
# token = "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"

##############################################################################################

def generate_query_llm(user_input, schema):
    # Model and Tokenizer Initialization
    model_name = "PipableAI/pip-sql-1.3b"
    token = "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"
    # prompt = user_input
    prompt = f"""
Database Schema:{schema}.

User task: "{user_input}"

Output: Write only the SQL query, without explanation or additional text.
"""
    sql_query = llm_huggingface(model_name, token, prompt)
    return sql_query

######################################################################################


# Inference
def generate_response_llm(user_input, sql_results, schema):
    """Generate a response based on user input and context."""

    if sql_results == None:
        return "Sorry, I couldn't find any relevant information."
    else:
        model_name="Qwen/Qwen2.5-1.5B"
        token="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"
        
        # prompt = user_input
        prompt = f"""
        User task: "{user_input}",
        Database Schema: {schema},
        SQL query: {sql_results}
        Please generate a response based on the input provided, excluding the input and schema them selves."""
        
        
        # Decode the output
        response_llm = llm_huggingface(model_name, token, prompt)
        
        # Assuming a simple concatenation of user input and context for now
    return response_llm #f"Based on the input: {user_input} and the {schema}, here's what I found: \n\n\n{tabular_form}"