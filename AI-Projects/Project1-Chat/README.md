# Project1-Chat

A simple Python project that sends a prompt to the Gemini API and prints the generated response.

## What it does

- Loads the Gemini API key from a `.env` file
- Sends a sample prompt to the Gemini model
- Prints the model's response to the terminal

## Requirements

- Python 3.9+
- A Gemini API key

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in this folder with your API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Run

```bash
python chat.py
```

The script currently sends a fixed prompt asking the model to explain Python in one sentence.
