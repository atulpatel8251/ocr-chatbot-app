import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import os
from difflib import get_close_matches
import platform

# 🛠 Set Tesseract path and environment variable for Windows
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"

# Streamlit setup
st.set_page_config(page_title="OCR PDF Chatbot", layout="wide")
st.title("📄 OCR PDF Chatbot")
st.write("Upload a scanned PDF and ask questions based on its text.")

# Upload PDF
pdf_file = st.file_uploader("Upload scanned PDF file", type=["pdf"])

# Initialize session state
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Extract text from PDF using OCR
if pdf_file:
    with st.spinner("Extracting text from PDF using OCR..."):
        images = convert_from_bytes(pdf_file.read())
        extracted_text = ""
        for page_num, img in enumerate(images):
            text = pytesseract.image_to_string(img, lang='hin+eng')
            extracted_text += f"\n--- Page {page_num+1} ---\n{text}"
        st.session_state.extracted_text = extracted_text
    st.success("Text extracted successfully!")
    st.text_area("📄 Extracted Text", st.session_state.extracted_text, height=300)

# Chatbot Section
st.markdown("### 💬 Chat with Extracted Content")
user_input = st.text_input("Ask a question based on the extracted text:")

if user_input:
    # Simple retrieval logic using closest matching line
    lines = st.session_state.extracted_text.splitlines()
    match = get_close_matches(user_input, lines, n=1, cutoff=0.2)
    bot_response = match[0] if match else "Sorry, I couldn't find a relevant answer."

    # Save chat history
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", bot_response))

# Display Chat History
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")
