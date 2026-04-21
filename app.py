# app.py - Document Processing Pipeline Web Interface

import streamlit as st
import os
import sqlite3
import glob
import PyPDF2
from docx import Document

# Page configuration
st.set_page_config(
    page_title="Document Processing Pipeline",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 Document Processing Pipeline")
st.markdown("Extract text from PDF and Word documents, then search across them.")

# Database path
DB_PATH = "documents.db"

# Initialize database
def init_database():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filepath TEXT,
            content TEXT,
            word_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_database()

# Function to extract from PDF
def extract_from_pdf(filepath):
    text = ""
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

# Function to extract from DOCX
def extract_from_docx(filepath):
    text = ""
    try:
        doc = Document(filepath)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
    return text

# Function to process and store file
def process_file(filepath):
    filename = os.path.basename(filepath)
    file_lower = filepath.lower()
    
    if file_lower.endswith('.pdf'):
        content = extract_from_pdf(filepath)
    elif file_lower.endswith('.docx'):
        content = extract_from_docx(filepath)
    else:
        return False, "Unsupported file type"
    
    if not content:
        return False, "No text extracted"
    
    word_count = len(content.split())
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO documents (filename, filepath, content, word_count)
        VALUES (?, ?, ?, ?)
    """, (filename, filepath, content, word_count))
    conn.commit()
    conn.close()
    
    return True, f"Stored {filename} ({word_count} words)"

# Function to search documents
def search_documents(keyword):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("""
        SELECT filename, content, word_count, created_at
        FROM documents
        WHERE content LIKE ?
        ORDER BY created_at DESC
    """, (f'%{keyword}%',))  # ← Only ONE placeholder, ONE value
    results = cursor.fetchall()
    conn.close()
    return results

# Function to get all documents
def get_all_documents():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("""
        SELECT filename, word_count, created_at
        FROM documents
        ORDER BY created_at DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return results

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Documents", "Search Documents", "View All Documents"])

# Page 1: Upload Documents
if page == "Upload Documents":
    st.header("📤 Upload Documents")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose PDF or DOCX files",
        type=['pdf', 'docx'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process
            success, message = process_file(temp_path)
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
            
            # Clean up
            os.remove(temp_path)
    
    # Folder path option
    st.markdown("---")
    st.subheader("Or process a folder of documents")
    folder_path = st.text_input("Enter folder path:")
    
    if st.button("Process Folder"):
        if os.path.exists(folder_path):
            files = []
            for ext in ['*.pdf', '*.docx']:
                files.extend(glob.glob(os.path.join(folder_path, ext)))
                files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
            
            if not files:
                st.warning("No PDF or DOCX files found")
            else:
                progress_bar = st.progress(0)
                for i, filepath in enumerate(files):
                    success, message = process_file(filepath)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.warning(f"⚠️ {message}")
                    progress_bar.progress((i + 1) / len(files))
                st.success(f"✅ Processed {len(files)} files")
        else:
            st.error("Folder not found")

# Page 2: Search Documents
elif page == "Search Documents":
    st.header("🔍 Search Documents")
    
    search_term = st.text_input("Enter keyword to search:")
    
    if search_term:
        with st.spinner("Searching..."):
            results = search_documents(search_term)
        
        if results:
            st.success(f"Found {len(results)} document(s)")
            
            for filename, content, word_count, created_at in results:
                with st.expander(f"📄 {filename} ({word_count} words)"):
                    # Show first 500 characters
                    st.text(content[:500])
                    if len(content) > 500:
                        st.text("... (truncated)")
                    st.caption(f"Added: {created_at}")
        else:
            st.info("No documents found containing that keyword")

# Page 3: View All Documents
elif page == "View All Documents":
    st.header("📚 All Documents")
    
    documents = get_all_documents()
    
    if documents:
        # Display as simple markdown table
        st.write("| Filename | Word Count | Added On |")
        st.write("|----------|------------|----------|")
        for filename, word_count, created_at in documents:
            st.write(f"| {filename} | {word_count} | {created_at} |")
        
        total_docs = len(documents)
        total_words = sum(row[1] for row in documents)
        st.markdown(f"**Total documents:** {total_docs}")
        st.markdown(f"**Total words indexed:** {total_words:,}")
    else:
        st.info("No documents in database yet. Upload some documents first.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption(f"Database: {DB_PATH}")