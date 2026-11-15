
import json
import urllib.request
import urllib.error

MODEL_NAME = "oamazonasgabriel/lfm2.5-230m:bf16-8gbRAM"
OLLAMA_URL = "http://localhost:11434/api/chat"


def explain_with_llm(question, database_answer):
    """
    Uses Ollama to explain an answer already obtained
    from the floor-plan database.
    """

    prompt = f"""
User question:
{question}

Verified database answer:
{database_answer}

Explain the database answer clearly and simply.

Rules:
- Use only facts in the verified database answer.
- Do not invent counts, labels, rooms, or measurements.
- Do not change any numbers.
- If the database says information is unavailable,
  clearly say that it cannot be confirmed.
- Keep the answer concise.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an assistant for building floor plans. "
                    "You must stay strictly grounded in the "
                    "provided database answer."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result["message"]["content"].strip()

    except urllib.error.URLError as error:
        return (
            "Could not connect to Ollama. "
            "Please make sure Ollama is running. "
            f"Details: {error}"
        )

    except (KeyError, json.JSONDecodeError) as error:
        return f"Unexpected response from Ollama: {error}"

    except TimeoutError:
        return "Ollama took too long to respond. Please try again."
