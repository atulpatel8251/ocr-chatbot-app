import streamlit as st
import fitz  # PyMuPDF
import tempfile

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

# Extract text from PDF using PyMuPDF (fitz)
if pdf_file:
    try:
        with st.spinner("Extracting text from PDF..."):
            # Create a temporary file to save the PDF content
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(pdf_file.getvalue())
                pdf_path = tmp_file.name

            # Open PDF using PyMuPDF (fitz)
            doc = fitz.open(pdf_path)
            extracted_text = ""
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text = page.get_text("text")  # Extract text
                extracted_text += f"\n--- Page {page_num+1} ---\n{text}"

            st.session_state.extracted_text = extracted_text
            st.success("Text extracted successfully!")

            # Display the extracted text
            st.text_area("📄 Extracted Text", st.session_state.extracted_text, height=300)

    except Exception as main_error:
        st.error(f"An error occurred: {str(main_error)}")
        st.info("Please check if all dependencies are installed correctly.")

# Chatbot Section
st.markdown("### 💬 Chat with Extracted Content")

if not st.session_state.extracted_text:
    st.info("Please upload a PDF first to extract text for chatting.")
else:
    user_input = st.text_input("Ask a question based on the extracted text:")

    if user_input:
        # Simple retrieval logic using closest matching line
        lines = [line for line in st.session_state.extracted_text.splitlines() if line.strip()]

        if lines:
            match = get_close_matches(user_input, lines, n=1, cutoff=0.2)
            bot_response = match[0] if match else "Sorry, I couldn't find a relevant answer."
        else:
            bot_response = "No text was extracted from the PDF or the extraction is empty."

        # Save chat history
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_response))

# Display Chat History
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")
