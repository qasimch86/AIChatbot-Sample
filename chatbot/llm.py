from transformers import AutoModelForCausalLM, AutoTokenizer
model_name = "EleutherAI/gpt-neo-1.3B"
token="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"
tokenizer = AutoTokenizer.from_pretrained(model_name,token=token)
model = AutoModelForCausalLM.from_pretrained(model_name,token=token)

# Inference
def generate_response(user_input, context):
    """Generate a response based on user input and context."""
    if context == "No results found.":
        return "Sorry, I couldn't find any relevant information."
    else:
        # Assuming a simple concatenation of user input and context for now
        return f"Based on the information, here's what I found: {context}"
