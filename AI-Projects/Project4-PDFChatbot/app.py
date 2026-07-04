import tempfile
from pathlib import Path

import streamlit as st

from pdf_chatbot import ask_pdf, build_index


st.set_page_config(page_title="PDF Chatbot", page_icon="PDF", layout="centered")
st.title("PDF Chatbot")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    if st.button("Index PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = Path(temp_file.name)

        with st.spinner("Extracting, chunking, embedding, and indexing..."):
            build_index(temp_path)

        st.success("PDF indexed. Ask a question below.")

question = st.text_input("Ask a question about the indexed PDF")

if question:
    with st.spinner("Searching the PDF and generating an answer..."):
        st.write(ask_pdf(question))
