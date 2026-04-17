# 📄 Document Processing Pipeline

A Python tool that extracts text from PDF and Word documents and stores them in a searchable SQLite database.

## 🚀 Features

- ✅ Extract text from **PDF** files
- ✅ Extract text from **Word (.docx)** files
- ✅ Case-insensitive file extension handling (.pdf, .PDF, .docx, .DOCX)
- ✅ Store documents in SQLite database with metadata
- ✅ Search across all documents for any keyword
- ✅ Word count tracking per document
- ✅ Graceful error handling (skips corrupted files)

## 🛠️ Technologies

- Python 3.9+
- PyPDF2 (PDF text extraction)
- python-docx (Word document extraction)
- SQLite3 (database storage)

## 📋 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/lemiyarasheed/document-pipeline.git
cd document-pipeline

2. Create virtual environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
bash
pip install -r requirements.txt
4. Run the program
bash
python document-processor.py
5. Enter folder path
When prompted, enter the path to a folder containing .pdf or .docx files:

text
📁 Enter folder path with documents: sample_docs
💬 Sample Usage
text
==================================================
📄 DOCUMENT PROCESSING PIPELINE
==================================================
✅ Database table ready
📁 Enter folder path with documents: sample_docs

📋 Found 2 document(s) to process

✅ Extracted 1250 characters from PDF
✅ Stored invoice.pdf (180 words)
✅ Extracted 800 characters from DOCX
✅ Stored report.docx (120 words)

✅ Processing complete! 2 document(s) stored.

🔍 Enter a word to search (or press Enter to skip): invoice

🔍 Found 1 document(s) containing 'invoice':
   📄 invoice.pdf - This invoice is for services rendered... (180 words)
📁 Project Structure
text
document-pipeline/
├── document-processor.py   # Main application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── documents.db           # SQLite database (created after first run)
🔍 How It Works
Function	What It Does
extract_from_pdf()	Reads text from PDF files
extract_from_docx()	Reads text from Word documents
process_file()	Extracts text and stores in database
search()	Searches for keywords across all documents
📊 Database Schema
Column	Type	Description
id	INTEGER	Unique document ID
filename	TEXT	Name of the file
filepath	TEXT	Full path to the file
content	TEXT	Extracted text content
word_count	INTEGER	Number of words in document
created_at	TIMESTAMP	When the document was added
🎯 Use Cases
Invoice processing - Extract and search invoice data

Contract management - Store and search legal documents

Report archiving - Build searchable document archive

Content analysis - Analyze text across multiple documents

🔧 Error Handling
Skips unsupported file types (.txt, .jpg, etc.)

Handles corrupted PDFs gracefully

Continues processing remaining files if one fails

🚀 Next Features (Planned)
Web interface with Streamlit

Extract emails, phone numbers, dates using regex

Export search results to CSV

Support for .txt files

Duplicate detection

👩‍💻 Author
Lemiya Rasheed
AI & Automation Specialist
GitHub

📅 Status
Version: 1.0
Last updated: April 17, 2026
Status: ✅ Working, production-ready

📄 License
This project is open source for portfolio purposes.