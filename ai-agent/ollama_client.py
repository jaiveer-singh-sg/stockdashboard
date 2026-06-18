import requests
import json


OLLAMA_URL="http://localhost:11434/api/generate"


def ask_ollama(prompt):

    payload={

        "model":"hermes3",

        "prompt":prompt,

        "stream":False,

        "format":"json"

    }


    response=requests.post(
        OLLAMA_URL,
        json=payload
    )


    data=response.json()


    return json.loads(
        data["response"]
    )