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


def require_api_key():
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found. Add it to a .env file.")


def call_gemini(messages, temperature, max_output_tokens):
    require_api_key()

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    payload = {
        "contents": messages,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
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

    return result["candidates"][0]["content"]["parts"][0]["text"]


def make_message(role, text):
    return {
        "role": role,
        "parts": [{"text": text}],
    }


def show_help():
    print("\nCommands:")
    print("  /exit                 Stop the chat")
    print("  /help                 Show commands")
    print("  /settings             Show current settings")
    print("  /temp 0.9             Change temperature")
    print("  /tokens 500           Change max output tokens")
    print("  /history              Show conversation history")
    print("  /clear                Clear conversation memory\n")


def show_settings(temperature, max_output_tokens):
    print(f"\nModel: {MODEL}")
    print(f"Temperature: {temperature}")
    print(f"Max output tokens: {max_output_tokens}")
    print("Memory: previous user and AI turns are sent back each time\n")


def show_history(messages):
    if not messages:
        print("\nNo conversation history yet.\n")
        return

    print("\nConversation history:")
    for message in messages:
        role = "You" if message["role"] == "user" else "AI"
        text = message["parts"][0]["text"]
        print(f"{role}: {text}")
    print()


def main():
    temperature = 0.4
    max_output_tokens = 300
    messages = []

    print("Project1-Chat-V2: Gemini chat loop with memory")
    print("Type /help for commands.\n")
    show_settings(temperature, max_output_tokens)

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            print("Type a message, or /help for commands.")
            continue

        if user_input == "/exit":
            break

        if user_input == "/help":
            show_help()
            continue

        if user_input == "/settings":
            show_settings(temperature, max_output_tokens)
            continue

        if user_input == "/history":
            show_history(messages)
            continue

        if user_input == "/clear":
            messages.clear()
            print("Conversation memory cleared.\n")
            continue

        if user_input.startswith("/temp "):
            try:
                temperature = float(user_input.split(maxsplit=1)[1])
            except ValueError:
                print("Use a number like: /temp 0.8")
                continue
            print(f"Temperature set to {temperature}.\n")
            continue

        if user_input.startswith("/tokens "):
            try:
                max_output_tokens = int(user_input.split(maxsplit=1)[1])
            except ValueError:
                print("Use a whole number like: /tokens 500")
                continue
            print(f"Max output tokens set to {max_output_tokens}.\n")
            continue

        messages.append(make_message("user", user_input))
        answer = call_gemini(messages, temperature, max_output_tokens)
        print(f"AI: {answer}\n")
        messages.append(make_message("model", answer))


if __name__ == "__main__":
    main()
