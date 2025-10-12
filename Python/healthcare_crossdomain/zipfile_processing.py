import streamlit as st
import zipfile
import os
import tempfile
from pypdf import PdfReader
from langchain.schema import Document

def zip_to_doc(uploaded_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "uploaded.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.read())

        # Extract ZIP contents
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # Find all PDF files
        pdf_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.lower().endswith(".pdf")]

        if not pdf_files:
            st.warning("No PDF files found in the ZIP.")
        else:
            st.success(f"Found {len(pdf_files)} PDF file(s). Processing...")

            documents = []

            for pdf_path in pdf_files:
                try:
                    reader = PdfReader(pdf_path)
                    text = ""
                    for page in reader.pages:
                        print("inside for page")
                        page_text = page.extract_text()
                        print("page_text ", page_text)
                        if page_text:
                            text += page_text + "\n"
                    print("text outside for page", text)

                    doc = Document(
                        page_content=text,
                        metadata={"source": os.path.basename(pdf_path)}
                    )
                    documents.append(doc)
                except Exception as e:
                    st.error(f"Error processing {os.path.basename(pdf_path)}: {e}")
    return documents

# Page setup
st.set_page_config(page_title="PDF Extractor with LangChain", layout="wide")
st.title("📁 Upload ZIP of PDFs and Process with LangChain")

if "documents" not in st.session_state:
    st.session_state.documents = ""
zip_documents = ""
# Upload ZIP file
uploaded_file = st.file_uploader("Upload a ZIP file containing PDFs", type=["zip"])

if uploaded_file:
    zip_documents = zip_to_doc(uploaded_file)

    #st.subheader(f"📄 {os.path.basename(uploaded_file)}")
    st.text_area("Extracted Text", zip_documents, height=300)

st.success(f"✅ Loaded {len(zip_documents)} LangChain Document(s). Ready for embedding or retrieval.")




