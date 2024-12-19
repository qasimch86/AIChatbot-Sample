from langchain_openai import ChatOpenAI

def llm_langchain(model_name, api_key, prompt):
    """
    Generate a response using Langchain's OpenAI LLM with customizable hyperparameters.
    """
    temperature = 0.1
    max_tokens = 512
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0

    kwargs = {
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty
    }
    valid_params = {
        "top_p": kwargs.get("top_p", None),
        "frequency_penalty": kwargs.get("frequency_penalty", None),
        "presence_penalty": kwargs.get("presence_penalty", None)
    }

    # Remove parameters with None values
    model_kwargs = {k: v for k, v in valid_params.items() if v is not None}
    llm = ChatOpenAI(
            model_name=model_name,
            openai_api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            **model_kwargs
        )

        # Generate and return the response
    print(f'prompt: {prompt}')
    try:
        response = llm.invoke(prompt)
        print(f'\n\n\n\nresponse {response.content}\n\n\n\n')
        return response.content
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"
