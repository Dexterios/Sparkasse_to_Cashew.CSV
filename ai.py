import openai

def ai(system_message, user_message, api_key = "API_KEY"):

    openai.api_key = api_key
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": f"{system_message}"},
            {"role": "user", "content": f"{user_message}"},
        ]
    )
    return response['choices'][0]['message']['content'] # "The Los Angeles Dodgers won the World Series in 2020."