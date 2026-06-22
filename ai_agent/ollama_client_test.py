import requests

OLLAMA_URL = "http://ollama-remotehost:11434/api/generate"

payload = {
    "model": "hermes3",
    "prompt": "Explain RSI indicator",
    "stream": False
}

response = requests.post(
    OLLAMA_URL,
    json=payload,
    timeout=(10,180)
)

print(response.status_code)
print(response.json())