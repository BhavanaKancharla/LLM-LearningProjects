import io
import os
import re
from pathlib import Path

import docx
import requests
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

st.set_page_config(page_title="RAG Document Assistant", page_icon="📚", layout="wide")

st.title("RAG Document Assistant")
st.write("Upload text files, ask questions, and get grounded answers from the uploaded content.")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Please set GEMINI_API_KEY in the local .env file.")
    st.stop()

st.subheader("Upload documents")
uploaded_files = st.file_uploader("Choose documents", type=["txt", "md", "pdf", "docx"], accept_multiple_files=True)


def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 80):
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks = []
    current = []
    current_len = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if current_len + len(sentence) + 1 <= chunk_size:
            current.append(sentence)
            current_len += len(sentence) + 1
        else:
            if current:
                chunks.append(" ".join(current))
            current = [sentence]
            current_len = len(sentence) + 1

    if current:
        chunks.append(" ".join(current))

    if overlap > 0 and len(chunks) > 1:
        merged = []
        for i, chunk in enumerate(chunks):
            if i == 0:
                merged.append(chunk)
            else:
                if len(merged[-1]) + len(chunk) < chunk_size:
                    merged[-1] = merged[-1] + " " + chunk
                else:
                    merged.append(chunk)
        return merged

    return chunks


def read_pdf_text(uploaded_file):
    try:
        reader = PdfReader(io.BytesIO(uploaded_file.getvalue()))
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return "\n".join(text)
    except Exception:
        return ""


def read_docx_text(uploaded_file):
    try:
        document = docx.Document(io.BytesIO(uploaded_file.getvalue()))
        return "\n".join([paragraph.text for paragraph in document.paragraphs if paragraph.text])
    except Exception:
        return ""


def read_uploaded_text(uploaded_file):
    if uploaded_file is None:
        return ""
    name = uploaded_file.name.lower()
    if name.endswith((".txt", ".md")):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    if name.endswith(".pdf"):
        return read_pdf_text(uploaded_file)
    if name.endswith(".docx"):
        return read_docx_text(uploaded_file)
    return ""


def retrieve_relevant_chunks(question: str, chunks: list[dict], top_k: int = 3):
    if not chunks:
        return []

    vectorizer = TfidfVectorizer(stop_words="english")
    documents = [chunk["text"] for chunk in chunks if chunk["text"].strip()]
    if not documents:
        return []

    vectors = vectorizer.fit_transform([question] + documents)
    question_vector = vectors[0]
    doc_vectors = vectors[1:]
    similarities = cosine_similarity(question_vector, doc_vectors).flatten()
    ranked_indices = similarities.argsort()[::-1][:top_k]

    results = []
    for index in ranked_indices:
        results.append({
            "chunk": chunks[index],
            "score": float(similarities[index]),
        })

    return results



def call_gemini(prompt: str, api_key: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 700,
        },
    }

    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    result = response.json()
    return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()


if uploaded_files:
    all_chunks = []
    source_files = []
    for uploaded_file in uploaded_files:
        text = read_uploaded_text(uploaded_file)
        if text.strip():
            file_chunks = split_text_into_chunks(text)
            source_files.append(uploaded_file.name)
            for idx, chunk in enumerate(file_chunks, start=1):
                all_chunks.append({
                    "text": chunk,
                    "source": uploaded_file.name,
                    "chunk_id": idx,
                })

    st.success(f"Loaded {len(all_chunks)} text chunks from {len(source_files)} file(s).")
    st.write("**Sources:** " + ", ".join(sorted(set(source_files))))
else:
    all_chunks = []
    st.info("Upload one or more .txt, .md, .pdf, or .docx files to start.")

question = st.text_input("Ask a question about the uploaded content")

if st.button("Answer") and question.strip():
    if not all_chunks:
        st.error("Please upload at least one document first.")
        st.stop()

    with st.spinner("Searching and generating an answer..."):
        relevant_chunks = retrieve_relevant_chunks(question, all_chunks)
        if not relevant_chunks:
            st.warning("No relevant content was found in the uploaded documents.")
            st.stop()

        top_score = max(chunk["score"] for chunk in relevant_chunks)
        if top_score < 0.03:
            st.warning("The uploaded documents do not contain strong context for this question.")
            st.info("Try uploading more relevant documents or asking a question that matches the content.")
            st.stop()

        context = "\n\n".join([chunk["chunk"]["text"] for chunk in relevant_chunks])

        prompt = f"""
You are a helpful assistant.
Answer the user's question using ONLY the provided context.
If the answer is not in the context, say you do not have enough information.

Context:
{context}

Question:
{question}
"""

        answer = call_gemini(prompt, api_key)
        st.subheader("Answer")
        st.markdown(answer)

        with st.expander("Retrieved context and sources"):
            for idx, item in enumerate(relevant_chunks, start=1):
                chunk = item["chunk"]
                score = item["score"]
                st.markdown(f"**Source {idx}:** {chunk['source']} (chunk {chunk['chunk_id']}), similarity {score:.2f}")
                st.write(chunk["text"])

