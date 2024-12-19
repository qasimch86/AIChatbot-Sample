from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def llm_huggingface_downloaded(model_name, token, prompt):

    # Load model directly
    tokenizer = AutoTokenizer.from_pretrained(model_name, token = token, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, token=token, device_map="auto", trust_remote_code=True)
    
    # Tokenize the input prompt with attention_mask
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1536,
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
            max_new_tokens=1500,  # Limit response length
            do_sample=True
        )
    # Decode the output
    docode_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"docode_output: {docode_output}")
    return docode_output