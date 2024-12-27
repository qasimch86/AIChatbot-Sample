from transformers import pipeline

def llm_huggingface_pipeline(model_name, prompt):
    try:
        # Initialize the pipeline with the specified model
        sql_pipeline = pipeline("text-generation",
                                model=model_name,
                                use_auth_token=True)

        # Generate the text
        result = sql_pipeline(prompt, max_length=200)

        # Print the generated SQL query
        print(f"result: {result}")
        return result
    except Exception as e:
        # Catch and print any errors
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"
