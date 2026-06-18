import requests
import json

# OLLAMA_URL="http://localhost:11434/api/generate"
OLLAMA_URL="http://ollama-remotehost:11434/api/generate"


def ask_ollama(prompt):

    payload = {
        "model": "hermes3",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=(10, 180)   # (connection timeout, response timeout seconds)
        )

        response.raise_for_status()

        data = response.json()

        return json.loads(
            data["response"]
        )

    except requests.exceptions.Timeout:
        return {
            "error": "Ollama model response timed out after 180 seconds"
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Ollama request failed: {str(e)}"
        }

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by Ollama model"
        }