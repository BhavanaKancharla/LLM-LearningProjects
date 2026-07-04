import os
import json
import urllib.request
import urllib.error

from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Add it to your .env file.")

model = "gemini-2.5-flash"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

payload = {
    "contents": [
        {
            "parts": [
                {"text": "Explain Python in one sentence"}
            ]
        }
    ],
    "generationConfig": {
        "temperature": 0.3,
        "maxOutputTokens": 200,
    },
}

request = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))
except urllib.error.HTTPError as error:
    details = error.read().decode("utf-8", errors="ignore")
    raise RuntimeError(f"Gemini API error ({error.code}): {details}") from error

print(result["candidates"][0]["content"]["parts"][0]["text"])
