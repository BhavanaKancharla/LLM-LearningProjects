# Project 4 - PDF Chatbot

This project teaches a fuller RAG architecture:

1. Extract text from PDF pages.
2. Split text into overlapping chunks.
3. Embed each chunk.
4. Store chunks and vectors in `pdf_vector_store.json`.
5. Retrieve the most relevant chunks for a question.
6. Ask Gemini to answer using only the retrieved context.

## Setup

```powershell
py -m pip install -r requirements.txt
```

Create `.env`:

```env
GEMINI_API_KEY=your_gemini_key_here
```

## Terminal Version

```powershell
py pdf_chatbot.py
```

Then type:

```text
index C:\path\to\your.pdf
```

After indexing, ask:

```text
What is this document about?
```

## Streamlit Version

```powershell
streamlit run app.py
```

Upload a PDF, click **Index PDF**, then ask questions.

## What You Are Learning

- Chunking
- Embeddings
- Vector similarity search
- Context construction
- RAG answer generation
