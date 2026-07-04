import json
import math
import os
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv


CHAT_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
STORE_PATH = BASE_DIR / "vector_store.json"

load_dotenv()
load_dotenv(BASE_DIR.parent / "Project1-Chat" / ".env")

API_KEY = os.environ.get("GEMINI_API_KEY")


def require_api_key():
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found. Add it to a .env file.")


def post_json(url, payload, timeout=60):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Gemini API error ({error.code}): {details}") from error


def embed_text(text):
    require_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{EMBEDDING_MODEL}:embedContent?key={API_KEY}"
    payload = {
        "model": f"models/{EMBEDDING_MODEL}",
        "content": {"parts": [{"text": text}]},
    }
    result = post_json(url, payload)
    return result["embedding"]["values"]


def generate_answer(question, context):
    require_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{CHAT_MODEL}:generateContent?key={API_KEY}"
    prompt = f"""Answer the question using only the context below.

If the answer is not in the context, say you do not know from the provided documents.

Context:
{context}

Question:
{question}
"""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 500},
    }
    result = post_json(url, payload)
    return result["candidates"][0]["content"]["parts"][0]["text"]


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    if not mag_a or not mag_b:
        return 0.0
    return dot / (mag_a * mag_b)


def load_documents():
    documents = []
    for path in sorted(DOCS_DIR.glob("*.txt")):
        documents.append({"id": path.stem, "text": path.read_text(encoding="utf-8")})
    return documents


def build_index():
    documents = load_documents()
    if not documents:
        raise ValueError(f"No .txt documents found in {DOCS_DIR}")

    records = []
    for doc in documents:
        print(f"Embedding {doc['id']}...")
        records.append(
            {
                "id": doc["id"],
                "text": doc["text"],
                "embedding": embed_text(doc["text"]),
            }
        )

    STORE_PATH.write_text(json.dumps(records, indent=2), encoding="utf-8")
    print(f"Saved {len(records)} documents to {STORE_PATH}")


def retrieve(question, top_k=3):
    if not STORE_PATH.exists():
        raise FileNotFoundError("vector_store.json not found. Run: py rag.py index")

    records = json.loads(STORE_PATH.read_text(encoding="utf-8"))
    query_embedding = embed_text(question)

    ranked = sorted(
        records,
        key=lambda item: cosine_similarity(query_embedding, item["embedding"]),
        reverse=True,
    )
    return ranked[:top_k]


def ask(question):
    matches = retrieve(question)
    context = "\n\n".join(f"[{item['id']}]\n{item['text']}" for item in matches)
    return generate_answer(question, context)


def main():
    command = input("Type 'index' to build embeddings or ask a question: ").strip()
    if command.lower() == "index":
        build_index()
        return

    answer = ask(command)
    print(f"\nAI: {answer}")


if __name__ == "__main__":
    main()
