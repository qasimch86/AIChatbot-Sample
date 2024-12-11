from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# # Model and Tokenizer Initialization
# model_name = "EleutherAI/gpt-neo-1.3B"
# token = "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"
# tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
# model = AutoModelForCausalLM.from_pretrained(model_name, token=token)

###############################################################################################
# Load model directly
token2="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"
model_name="Qwen/Qwen2.5-1.5B"
tokenizer = AutoTokenizer.from_pretrained(model_name, token = token2)
model = AutoModelForCausalLM.from_pretrained(model_name, token=token2)


# Set pad_token to eos_token if not defined
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def generate_query_LLM(user_input, schema):
    prompt = f"""
Database Schema:
{schema}.

User task: "{user_input}"

Output:
Write only the SQL query, without explanation or additional text.
"""

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
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],  # Explicitly provide the attention mask
            num_return_sequences=1,
            no_repeat_ngram_size=3,  # Avoid repeated n-grams
            top_k=10,  # Top-k sampling
            temperature=0.3,  # Sampling temperature
            # pad_token_id=tokenizer.eos_token_id,
            max_new_tokens=150,  # Limit response length
            do_sample=True
        )
    print(f'here are the outputs: {outputs}')
    # Decode the output
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Clean the SQL query to remove any unwanted information (like schema details)
    # sql_query = sql_query.split('Generate an SQL query for the following task:')[1]  # Remove the prompt part
    sql_query = sql_query.strip()
    # print(f'This is query after LLM tokenizer + split + strip:{sql_query}')
    
    return sql_query

# Inference
def generate_response(user_input, context):
    """Generate a response based on user input and context."""
    if context == None:
        return "Sorry, I couldn't find any relevant information."
    else:
        # Assuming a simple concatenation of user input and context for now
        return f"Based on the information, here's what I found: {context}"