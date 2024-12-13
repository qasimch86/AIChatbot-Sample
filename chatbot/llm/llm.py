from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

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
    input("Press Enter to continue......")
    # Model and Tokenizer Initialization
    model_name = "PipableAI/pip-sql-1.3b"
    token = "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"
    # Load model directly
    tokenizer = AutoTokenizer.from_pretrained(model_name, token = token)
    model = AutoModelForCausalLM.from_pretrained(model_name, token=token)
    print(f"Token: {token}")
    # Set pad_token to eos_token if not defined
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # prompt = user_input
    prompt = f"""
Database Schema:{schema}.

User task: "{user_input}"

Output: Write only the SQL query, without explanation or additional text.
"""
    print(f'generate_query_LLM: Prompt: {prompt}')

    # Tokenize the input prompt with attention_mask
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding="max_length"  # Ensures consistent input length
    )

    # Generate response
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            # attention_mask=inputs["attention_mask"],  # Explicitly provide the attention mask
            num_return_sequences=1,
            no_repeat_ngram_size=3,  # Avoid repeated n-grams
            top_k=10,  # Top-k sampling
            temperature=0.5,  # Sampling temperature
            # pad_token_id=tokenizer.eos_token_id,
            max_new_tokens=150,  # Limit response length
            do_sample=True
        )
    # Decode the output
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"sql_query: {sql_query}")
    input("Press Enter to continue...")
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
        # Load model directly
        tokenizer = AutoTokenizer.from_pretrained(model_name, token = token)
        model = AutoModelForCausalLM.from_pretrained(model_name, token=token)

        # Set pad_token to eos_token if not defined
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # prompt = user_input
        prompt = f"""
        User task: "{user_input}",
        Database Schema: {schema},
        SQL query: {sql_results}
        Please generate a response based on the input provided, excluding the input itself."""
        # Tokenize the input prompt with attention_mask
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=False,
            max_length=512,
            padding="max_length"  # Ensures consistent input length
        )

        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                # attention_mask=inputs["attention_mask"],  # Explicitly provide the attention mask
                num_return_sequences=1,
                no_repeat_ngram_size=3,  # Avoid repeated n-grams
                top_k=10,  # Top-k sampling
                temperature=0.5,  # Sampling temperature
                # pad_token_id=tokenizer.eos_token_id,
                max_new_tokens=512,  # Limit response length
                do_sample=True
            )
        # Decode the output
        response_llm = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Assuming a simple concatenation of user input and context for now
    return response_llm #f"Based on the input: {user_input} and the {schema}, here's what I found: \n\n\n{tabular_form}"