# RAG Document Assistant

A simple Streamlit app that lets you upload text files, retrieve the most relevant chunks, and ask questions grounded in the uploaded content.

## What it does

- Uploads one or more `.txt`, `.md`, `.pdf`, or `.docx` documents
- Splits the documents into smaller text chunks
- Uses TF-IDF and cosine similarity to find relevant chunks
- Shows which file each retrieved chunk came from
- Sends the retrieved context to Gemini for a grounded answer

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

3. Create a local `.env` file with your Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Run

```bash
streamlit run app.py
```
