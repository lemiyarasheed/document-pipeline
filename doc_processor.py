# document-processor.py - Extract text from documents and pdfs
import os
import sqlite3
import PyPDF2
import glob
from docx import Document

class DocumentProcessor:
    def __init__(self, db_path="documents.db"):
        """Initialize database connection"""
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        """Create documents table if it does not exist"""
        self.conn.execute("""CREATE TABLE IF NOT EXISTS documents(
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          filename TEXT,
                          filepath TEXT,
                          content TEXT,
                          word_count INTEGER,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        self.conn.commit()
        print("✅ Database table ready")

    def extract_from_pdf(self, filepath):
        """Extract text from PDF File"""
        text = ""
        try:
            with open(filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
            print(f"✅ Extracted {len(text)} characters from PDF")
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
        return text

    def extract_from_docx(self, filepath):
        """Extract text from Word document"""
        text = ""
        try:
            doc = Document(filepath)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            print(f"✅ Extracted {len(text)} characters from DOCX")
        except Exception as e:
            print(f"❌ Error reading DOCX: {e}")
        return text

    def process_file(self, filepath):
        """Process a single file and store in database"""
        filename = os.path.basename(filepath)

        # Case-insensitive extension check
        file_lower = filepath.lower()
        
        if file_lower.endswith('.pdf'):
            content = self.extract_from_pdf(filepath)
        elif file_lower.endswith('.docx'):
            content = self.extract_from_docx(filepath)
        else:
            print(f"⚠️ Skipping unsupported file {filename}")
            return

        # Calculate word count
        word_count = len(content.split())

        # Store in database
        self.conn.execute("""
            INSERT INTO documents (filename, filepath, content, word_count)
            VALUES (?, ?, ?, ?)
        """, (filename, filepath, content, word_count))
        self.conn.commit()
        print(f"✅ Stored {filename} ({word_count} words)")

    def search(self, keyword):
        """Search for keyword in all documents"""
        cursor = self.conn.execute("""
            SELECT filename, content, word_count
            FROM documents
            WHERE content LIKE ?
        """, (f'%{keyword}%',))
        
        results = cursor.fetchall()
        
        if not results:
            print(f"🔍 No documents found containing '{keyword}'")
            return []
        
        print(f"\n🔍 Found {len(results)} document(s) containing '{keyword}':")
        for filename, content, word_count in results:
            preview = content[:100].replace('\n', ' ')
            print(f"   📄 {filename} - {preview}... ({word_count} words)")
        
        return results

    def close(self):
        """Close database connection"""
        self.conn.close()
        print("👋 Database connection closed")


def main():
    print("=" * 50)
    print("📄 DOCUMENT PROCESSING PIPELINE")
    print("=" * 50)

    processor = DocumentProcessor()

    # Process all documents in a folder
    folder_path = input("📁 Enter folder path with documents: ").strip()

    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        processor.close()
        return

    # Find all PDF and DOCX files (case-insensitive)
    files = []
    extensions = ['*.pdf', '*.docx']
    
    for ext in extensions:
        # Try multiple case variations
        files.extend(glob.glob(os.path.join(folder_path, ext)))           # lowercase
        files.extend(glob.glob(os.path.join(folder_path, ext.upper())))   # UPPERCASE
        files.extend(glob.glob(os.path.join(folder_path, ext.capitalize()))) # Capitalized

    # Remove duplicates
    files = list(set(files))

    if not files:
        print("❌ No PDF or DOCX files found")
        print("   (Checked for: .pdf, .PDF, .Pdf, .docx, .DOCX, .Docx)")
        processor.close()
        return

    print(f"\n📋 Found {len(files)} document(s) to process\n")

    for filepath in files:
        processor.process_file(filepath)

    print(f"\n✅ Processing complete! {len(files)} document(s) stored.")

    # Search example
    search_term = input("\n🔍 Enter a word to search (or press Enter to skip): ").strip()
    if search_term:
        processor.search(search_term)

    processor.close()


if __name__ == "__main__":
    main()