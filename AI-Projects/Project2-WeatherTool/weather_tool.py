import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent
load_dotenv()
load_dotenv(BASE_DIR.parent / "Project1-Chat" / ".env")

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"


def get_weather(city):
    """Fake weather tool so the project focuses on function-calling flow."""
    weather_by_city = {
        "bangalore": "Bangalore is 28 C and sunny.",
        "bengaluru": "Bengaluru is 28 C and sunny.",
        "mumbai": "Mumbai is 30 C and humid.",
        "delhi": "Delhi is 34 C and hazy.",
        "chennai": "Chennai is 31 C with light clouds.",
    }
    return weather_by_city.get(city.lower(), f"{city} is 27 C and clear.")


def call_gemini(contents, tools=None):
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found. Add it to a .env file.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    payload = {"contents": contents}
    if tools:
        payload["tools"] = tools

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Gemini API error ({error.code}): {details}") from error


def get_first_part(response):
    return response["candidates"][0]["content"]["parts"][0]


def ask_with_weather_tool(question):
    tools = [
        {
            "functionDeclarations": [
                {
                    "name": "get_weather",
                    "description": "Get the current weather for a city.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The city name, for example Bangalore.",
                            }
                        },
                        "required": ["city"],
                    },
                }
            ]
        }
    ]

    contents = [
        {
            "role": "user",
            "parts": [{"text": question}],
        }
    ]

    first_response = call_gemini(contents, tools=tools)
    first_part = get_first_part(first_response)

    if "functionCall" not in first_part:
        return first_part.get("text", "")

    function_call = first_part["functionCall"]
    function_name = function_call["name"]
    args = function_call.get("args", {})

    if function_name != "get_weather":
        raise ValueError(f"Unknown tool requested: {function_name}")

    city = args.get("city", "")
    tool_result = get_weather(city)

    contents.append(
        {
            "role": "model",
            "parts": [{"functionCall": function_call}],
        }
    )
    contents.append(
        {
            "role": "function",
            "parts": [
                {
                    "functionResponse": {
                        "name": "get_weather",
                        "response": {"result": tool_result},
                    }
                }
            ],
        }
    )

    final_response = call_gemini(contents, tools=tools)
    return get_first_part(final_response).get("text", "")


if __name__ == "__main__":
    print("Weather tool chat. Type 'exit' to stop.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break

        answer = ask_with_weather_tool(user_input)
        print(f"AI: {answer}")
