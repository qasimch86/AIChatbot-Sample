import openai

def llm_openai(model_name, api_key, prompt):
    """
    Generate a response from OpenAI's API with customizable hyperparameters.
    
    :param model_name: Name of the model (e.g., 'text-davinci-003')
    :param prompt: The prompt for the model to complete
    :param api_key: OpenAI API key
    :param temperature: Controls randomness (0.0 - 1.0)
    :param max_tokens: Max number of tokens in the response
    :param top_p: Controls diversity (0.0 - 1.0)
    :param frequency_penalty: Penalizes repeating words (0.0 - 2.0)
    :param presence_penalty: Penalizes new topics (0.0 - 2.0)
    :return: Generated text from the model
    """
    openai.api_key = api_key  # Set OpenAI API key
    temperature=0.7
    max_tokens=512
    top_p=1
    frequency_penalty=0
    presence_penalty=0
    print(f'Creating an instance of OpenAI: {prompt}\n\n')

    try:
        response = openai.Completion.create(
            model=model_name,  # Model name like 'text-davinci-003'
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        print(f'response = {response}')
        # Extracting and returning the generated text
        return response.choices[0].text.strip()
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"