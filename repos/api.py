import openai
from dotenv import dotenv_values

config = dotenv_values(".env")
openai.api_key = config["SECRET"]


messages = []


def ChatGPT(data):
    messages.append({"role": "user", "content": data})
    
    completion = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=messages)

    chat_response = completion.choices[0].message
    messages.append(chat_response)
    return messages # list of objects [{content, role}, ... ]