# Document Summarizer

A simple Streamlit app that summarizes pasted text using the Gemini API.

## Features

- Paste text into the app
- Generate a concise summary
- Uses Gemini 2.5 Flash

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your API key:
   ```bash
   setx GEMINI_API_KEY "your_api_key_here"
   ```
   Or create a local `.env` file if you prefer.

## Run

```bash
streamlit run app.py
```
