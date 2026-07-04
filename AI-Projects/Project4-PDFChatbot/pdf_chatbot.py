import json
import math
import os
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader


CHAT_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"
BASE_DIR = Path(__file__).parent
STORE_PATH = BASE_DIR / "pdf_vector_store.json"

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
    prompt = f"""You are a PDF question-answering assistant.

Answer using only the PDF context below. If the answer is not present, say you do not know from the PDF.
Mention page numbers when they are useful.

Context:
{context}

Question:
{question}
"""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 700},
    }
    result = post_json(url, payload)
    return result["candidates"][0]["content"]["parts"][0]["text"]


def extract_pdf_pages(pdf_path):
    reader = PdfReader(str(pdf_path))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({"page": index, "text": text})
    return pages


def chunk_text(text, chunk_size=900, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def build_index(pdf_path, chunk_size=900, overlap=150):
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pages = extract_pdf_pages(pdf_path)
    if not pages:
        raise ValueError("No extractable text found in the PDF.")

    records = []
    for page in pages:
        for chunk_number, chunk in enumerate(chunk_text(page["text"], chunk_size, overlap), start=1):
            chunk_id = f"page-{page['page']}-chunk-{chunk_number}"
            print(f"Embedding {chunk_id}...")
            records.append(
                {
                    "id": chunk_id,
                    "source": pdf_path.name,
                    "page": page["page"],
                    "text": chunk,
                    "embedding": embed_text(chunk),
                }
            )

    STORE_PATH.write_text(json.dumps(records, indent=2), encoding="utf-8")
    print(f"Saved {len(records)} chunks to {STORE_PATH}")


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    if not mag_a or not mag_b:
        return 0.0
    return dot / (mag_a * mag_b)


def retrieve(question, top_k=4):
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if not STORE_PATH.exists():
        raise FileNotFoundError("pdf_vector_store.json not found. Index a PDF first.")

    records = json.loads(STORE_PATH.read_text(encoding="utf-8"))
    query_embedding = embed_text(question)
    ranked = sorted(
        records,
        key=lambda item: cosine_similarity(query_embedding, item["embedding"]),
        reverse=True,
    )
    return ranked[:top_k]


def ask_pdf(question):
    matches = retrieve(question)
    context = "\n\n".join(
        f"[Source: {item['source']}, page {item['page']}]\n{item['text']}"
        for item in matches
    )
    return generate_answer(question, context)


def main():
    print("PDF Chatbot")
    print("1. Type: index path\\to\\file.pdf")
    print("2. Then ask a question")
    print("3. Type: exit")

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            print("Type a question, or type 'exit' to stop.")
            continue

        if user_input.lower() == "exit":
            break

        if user_input.lower().startswith("index "):
            pdf_path = user_input[6:].strip().strip('"')
            build_index(pdf_path)
            continue

        answer = ask_pdf(user_input)
        print(f"\nAI: {answer}")


if __name__ == "__main__":
    main()
