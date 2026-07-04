# Project 3 - Mini RAG With 5 Documents

This project teaches retrieval augmented generation:

1. Embed the documents.
2. Store vectors locally.
3. Embed the user question.
4. Retrieve the most similar documents.
5. Ask Gemini to answer using only that context.

## Setup

```powershell
py -m pip install -r requirements.txt
```

Create `.env`:

```env
GEMINI_API_KEY=your_gemini_key_here
```

## Build The Index

```powershell
py rag.py
```

Then type:

```text
index
```

## Ask Questions

Run again:

```powershell
py rag.py
```

Then ask:

```text
What is Docker used for?
```

## Files

- `docs/` contains the five starter documents.
- `vector_store.json` is created after indexing.
- `rag.py` contains embedding, retrieval, and answer generation.
