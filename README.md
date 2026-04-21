---
title: Document Processing Pipeline
emoji: 📄
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.35.0"
app_file: app.py
pinned: false
---

# 📄 Document Processing Pipeline

A web application that extracts text from PDF and Word documents, stores them in a searchable database, and allows you to search across all documents.

## 🚀 Live Demo

[![Open in Spaces](https://img.shields.io/badge/🤗-Open%20in%20Spaces-blue)](https://huggingface.co/spaces/lemiyarasheed/document-pipeline)

## ✨ Features

- 📤 Upload PDF and DOCX files
- 📁 Process entire folders of documents
- 🔍 Search across all documents for any keyword
- 📊 View all documents in a table
- 📈 Word count tracking per document

## 🛠️ Technologies

- Python 3.11
- Streamlit (Web interface)
- PyPDF2 (PDF text extraction)
- python-docx (Word document extraction)
- SQLite3 (Database storage)

## 📋 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/lemiyarasheed/document-pipeline.git
cd document-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
💬 Sample Usage
Upload a PDF or DOCX file → Text is extracted and stored

Search for a keyword → Find all documents containing that word

View all documents → See everything in your database

📁 Project Structure
text
document-pipeline/
├── app.py              # Streamlit web interface
├── document-processor.py # CLI version (original)
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── documents.db       # SQLite database (created on first run)
🎯 Use Cases
Invoice processing and search

Contract management

Report archiving

Legal document search

👩‍💻 Author
Lemiya Rasheed
AI & Automation Specialist
GitHub

📅 Status
Version: 1.0
Last updated: April 21, 2026
Status: ✅ Working, deployed on Hugging Face Spaces

