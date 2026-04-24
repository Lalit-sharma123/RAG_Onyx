##################### correct

import requests
import time
import json
from app.config import OLLAMA_URL, MODEL


# ---------------------------
# 🔹 NORMAL (NON-STREAM)
# ---------------------------
def generate_answer(prompt, retries=2):

    print("🧠 Calling LLM...")

    for attempt in range(retries):
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120   # ⚡ balanced timeout
            )

            response.raise_for_status()

            data = response.json()
            answer = data.get("response", "").strip()

            if not answer:
                return "⚠️ Empty response from model."

            print("✅ LLM responded")
            return answer

        except requests.exceptions.Timeout:
            print(f"⏳ Timeout... retry {attempt + 1}")
            time.sleep(2)

        except requests.exceptions.ConnectionError:
            return "⚠️ Cannot connect to LLM server."

        except Exception as e:
            return f"⚠️ LLM error: {str(e)}"

    return "⚠️ Model is slow/unavailable. Try again."


# ---------------------------
# 🔹 STREAMING (FOR UI)
# ---------------------------
def stream_answer(prompt, retries=2):

    print("🧠 Streaming LLM...")

    for attempt in range(retries):
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": True
                },
                stream=True,
                timeout=180
            )

            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))
                        if "response" in data:
                            yield data["response"]
                    except:
                        continue

            return  # success → exit

        except requests.exceptions.Timeout:
            yield f"\n⏳ Timeout... retry {attempt + 1}"
            time.sleep(2)

        except requests.exceptions.ConnectionError:
            yield "\n⚠️ Cannot connect to LLM server."
            return

        except Exception as e:
            yield f"\n⚠️ Streaming error: {str(e)}"
            return

    yield "\n⚠️ Model is slow/unavailable. Try again."