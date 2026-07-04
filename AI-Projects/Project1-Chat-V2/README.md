# Project1-Chat-V2

This is the second checkpoint after `Project1-Chat`.

The first version sends one prompt and prints one answer. This version turns it into a real terminal chatbot.

## Concepts

- Prompting
- Conversation history
- Context
- Temperature
- Max output tokens
- Basic chat loop

## Setup

This project automatically reuses `GEMINI_API_KEY` from:

```text
../Project1-Chat/.env
```

You can also create a local `.env` file here:

```env
GEMINI_API_KEY=your_gemini_key_here
```

Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

## Run

```powershell
py chat_loop.py
```

## Try These

```text
Explain tokens like I am 10
```

```text
Now explain it for a software engineer
```

The second answer uses the previous conversation as context.

## Commands

```text
/help
/settings
/temp 0.9
/tokens 500
/history
/clear
/exit
```

## What Changed From Project1-Chat

Project1-Chat:

```text
One prompt -> one response
```

Project1-Chat-V2:

```text
User turn -> Gemini -> answer
User turn -> previous turns + new question -> Gemini -> answer
```

The model does not remember by itself. The Python program creates memory by sending the old messages again.
