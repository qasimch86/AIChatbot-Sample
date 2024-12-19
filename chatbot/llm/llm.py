from chatbot.llm.llm_huggingface_downloaded import llm_huggingface_downloaded
from chatbot.llm.llm_huggingface_pipeline import llm_huggingface_pipeline
from chatbot.llm.llm_langchain import llm_langchain
from chatbot.llm.llm_openai import llm_openai

from chatbot.config import Config

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

    prompt = f"""
Output: Write only the SQL query, without explanation or additional text. Here is the given 
user task: "{user_input}"
and
database schema:{schema}.
"""
    # print(f'prompt = {prompt}')
    # input('Press Enter to continue...')
    sql_query=''
#######################################huggingface direct##########################################
    if Config.llm_provider == 'huggingface_direct':
        model_name='PipableAI/pip-sql-1.3b'#'bigcode/starcoderbase'
        token='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'   
        sql_query = llm_huggingface_downloaded(model_name, token, prompt)
#######################################huggingface pipeline##########################################
    if Config.llm_provider == 'huggingface_pipeline':
        model_name='PipableAI/pip-sql-1.3b'#'bigcode/starcoderbase'
        token='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'
        sql_query = llm_huggingface_pipeline(model_name, prompt)

#######################################langchain############################################
    elif Config.llm_provider=='langchain':
        ######################
        #For Langchain hosted services, we need langchain api_key. Usually we do not need it:
        #api key = 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
        ######################
        model_name='gpt-3.5-turbo'
        token= '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'
        sql_query = llm_langchain(model_name, token, prompt)

###########################################openai###########################################
    elif Config.llm_provider=='OpenAI':
        model_name='gpt-3.5-turbo'
        token= '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'   
        # print(f'Model name = {model_name}\n\n{prompt}')
        sql_query = llm_openai(model_name, token, prompt)

    return sql_query

######################################################################################
######################################################################################
######################################################################################

# Inference
def generate_response_llm(user_input, sql_results, schema):
    """Generate a response based on user input and context."""
    if sql_results == None:
        return "Sorry, I couldn't find any relevant information."

    # prompt = user_input
    prompt = f"""
        Please generate a response based on the sql query, user input, and database schema. You must exclude the input and schema from the response.
        SQL query: {sql_results}
        User task: "{user_input}",
        Database Schema: {schema}
        """
#######################################huggingface direct##########################################
    if Config.llm_provider == 'huggingface_downloaded':
        model_name='bigcode/starcoderbase'
        # token='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'
        # Decode the output
        response_llm = llm_huggingface_downloaded(model_name, token, prompt)
#######################################huggingface pipeline##########################################
    if Config.llm_provider == 'huggingface_pipeline':
        model_name='bigcode/starcoderbase'
        token='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'
        response_llm = llm_huggingface_pipeline(model_name, prompt)

#######################################langchain############################################
    elif Config.llm_provider=='langchain':
        model_name='gpt-3.5-turbo'
        token= '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'
        # Decode the output
        response_llm = llm_langchain(model_name, token, prompt)

###########################################openai###########################################
    elif Config.llm_provider=='openai':
        model_name='gpt-3.5-turbo'
        token='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'   
        # Decode the output
        response_llm = llm_openai(model_name, token, prompt)
    return response_llm