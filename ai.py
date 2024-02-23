import openai

def ai(system_message, user_message, api_key = "API_KEY"):
    """
        Generate a dictionary of categories based on a prompt and a user message.

        This function uses an AI model to generate a dictionary of categories based on the provided prompt and message.

        Parameters:
        custom_prompt (str): The prompt for the AI model.
        user_message (str): The user message for the AI model.
        api_key (str): The API key for the AI model.

        Returns:
        dict: The generated dictionary of categories.

    """
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": f"{system_message}"},
            {"role": "user", "content": f"{user_message}"},
        ]
    )
    return response['choices'][0]['message']['content'] # "The Los Angeles Dodgers won the World Series in 2020."