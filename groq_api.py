import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_groq(message, history=None, model="mixtral-8x7b-32768"):
    if history is None:
        history = []

    history.append({"role": "user", "content": message})

    chat_completion = client.chat.completions.create(
        messages=history,
        model=model
    )

    return chat_completion.choices[0].message.content