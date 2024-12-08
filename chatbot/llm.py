from transformers import AutoModelForCausalLM, AutoTokenizer
model_name = "EleutherAI/gpt-neo-1.3B"
token="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"
tokenizer = AutoTokenizer.from_pretrained(model_name,token=token)
model = AutoModelForCausalLM.from_pretrained(model_name,token=token)

# Inference
def generate_response(user_input,context):
    input_text = user_input
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=150,num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
