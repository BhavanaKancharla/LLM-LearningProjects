import os
import streamlit as st
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

st.set_page_config(page_title="Document Summarizer", page_icon="📝", layout="wide")

st.title("Document Summarizer")
st.write("Paste text or upload a document to get a concise summary.")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Please set the GEMINI_API_KEY environment variable or add it to the local .env file.")
    st.stop()


def split_text(text, max_chars=3500):
    words = text.split()
    chunks = []
    current = []
    current_len = 0

    for word in words:
        if current_len + len(word) + 1 > max_chars and current:
            chunks.append(" ".join(current))
            current = [word]
            current_len = len(word)
        else:
            current.append(word)
            current_len += len(word) + 1

    if current:
        chunks.append(" ".join(current))

    return chunks


def call_gemini(prompt, api_key, max_output_tokens=800):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": max_output_tokens,
        },
    }

    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    result = response.json()
    return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()


def summarize_text(text, api_key):
    if len(text) <= 4000:
        prompt = f"""
You are an expert summarizer.
Summarize the following text in a detailed but concise way.
Return all of these sections in order:
1. Overview: 2-3 sentences explaining the main idea.
2. Key Points: 4-6 bullet points covering the most important ideas.
3. Conclusion: 1 sentence summarizing the takeaway.

Text to summarize:
{text}
"""
        return call_gemini(prompt, api_key, max_output_tokens=1000)

    chunks = split_text(text)
    section_summaries = []
    for index, chunk in enumerate(chunks, start=1):
        prompt = f"""
Summarize this section of a document in 2-4 clear sentences.
Focus on the most important facts and achievements.

Section {index}:
{chunk}
"""
        section_summary = call_gemini(prompt, api_key, max_output_tokens=400)
        section_summaries.append(f"Section {index}: {section_summary}")

    combined_prompt = f"""
Combine the following section summaries into one polished, complete summary.
Return:
1. Overview
2. Key Points as bullet points
3. Conclusion

Section summaries:
{'\n\n'.join(section_summaries)}
"""
    return call_gemini(combined_prompt, api_key, max_output_tokens=1200)


text_input = st.text_area("Paste text here", height=250, placeholder="Enter the text you want summarized...")

if st.button("Summarize") and text_input.strip():
    with st.spinner("Generating summary..."):
        try:
            summary = summarize_text(text_input, api_key)
            st.subheader("Summary")
            st.markdown(summary)
        except Exception as e:
            st.error(f"Failed to generate summary: {e}")
