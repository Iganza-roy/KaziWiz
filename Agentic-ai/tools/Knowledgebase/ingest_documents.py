"""
Document Ingestion Tool
Processes documents from documents/ folder and adds to Pinecone knowledge base
Supports: PDF, TXT, DOCX, MD files
"""
import os
from pathlib import Path
from typing import List, Dict
import hashlib
from datetime import datetime

# Document processors
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None

from knowledge_base import EconomicKnowledgeBase


class DocumentProcessor:
    """Process various document types for knowledge base ingestion"""
    
    def __init__(self, documents_dir: str = "../documents"):
        """
        Initialize document processor
        
        Args:
            documents_dir: Path to documents directory
        """
        self.documents_dir = Path(documents_dir)
        if not self.documents_dir.exists():
            self.documents_dir.mkdir(parents=True)
            print(f"📁 Created documents directory: {self.documents_dir}")
    
    def _generate_doc_id(self, filename: str, content: str) -> str:
        """Generate unique ID for document"""
        # Use hash of filename + first 100 chars
        unique_str = f"{filename}_{content[:100]}"
        return hashlib.md5(unique_str.encode()).hexdigest()
    
    def _extract_text_from_pdf(self, filepath: Path) -> str:
        """Extract text from PDF file"""
        if PdfReader is None:
            raise ImportError("pypdf not installed. Run: pip install pypdf")
        
        reader = PdfReader(str(filepath))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    
    def _extract_text_from_docx(self, filepath: Path) -> str:
        """Extract text from DOCX file"""
        if DocxDocument is None:
            raise ImportError("python-docx not installed. Run: pip install python-docx")
        
        doc = DocxDocument(str(filepath))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    
    def _extract_text_from_txt(self, filepath: Path) -> str:
        """Extract text from TXT/MD file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    def process_document(self, filepath: Path) -> Dict[str, str]:
        """
        Process a single document
        
        Args:
            filepath: Path to document file
            
        Returns:
            Dictionary with id, text, and metadata
        """
        print(f"📄 Processing: {filepath.name}")
        
        # Extract text based on file type
        ext = filepath.suffix.lower()
        
        if ext == '.pdf':
            text = self._extract_text_from_pdf(filepath)
        elif ext == '.docx':
            text = self._extract_text_from_docx(filepath)
        elif ext in ['.txt', '.md']:
            text = self._extract_text_from_txt(filepath)
        else:
            print(f"  ⚠️  Unsupported file type: {ext}")
            return None
        
        if not text:
            print(f"  ⚠️  No text extracted from {filepath.name}")
            return None
        
        # Generate ID
        doc_id = self._generate_doc_id(filepath.name, text)
        
        # Extract metadata
        metadata = {
            'title': filepath.stem.replace('_', ' ').title(),
            'source': filepath.name,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'uploaded_document',
            'category': self._infer_category(filepath.stem, text),
            'file_type': ext[1:],  # Remove dot
            'word_count': len(text.split())
        }
        
        print(f"  ✅ Extracted {len(text)} characters ({metadata['word_count']} words)")
        
        return {
            'id': doc_id,
            'text': text,
            'metadata': metadata
        }
    
    def _infer_category(self, filename: str, text: str) -> str:
        """Infer document category from filename and content"""
        filename_lower = filename.lower()
        text_lower = text.lower()
        
        # Category keywords
        categories = {
            'taxation': ['tax', 'gst', 'income tax', 'corporate tax', 'vat', 'duty'],
            'budget': ['budget', 'fiscal', 'spending', 'expenditure', 'appropriation'],
            'subsidy': ['subsidy', 'subsidies', 'welfare', 'benefit', 'assistance'],
            'trade': ['trade', 'import', 'export', 'tariff', 'commerce', 'wto'],
            'infrastructure': ['infrastructure', 'roads', 'railways', 'construction', 'development'],
            'monetary': ['monetary', 'interest rate', 'inflation', 'rbi', 'central bank'],
            'employment': ['employment', 'jobs', 'unemployment', 'labor', 'workforce'],
            'gdp': ['gdp', 'growth', 'economic growth', 'development']
        }
        
        # Check filename and text for keywords
        for category, keywords in categories.items():
            if any(keyword in filename_lower for keyword in keywords):
                return category
            if any(keyword in text_lower[:500] for keyword in keywords):  # Check first 500 chars
                return category
        
        return 'general_economic'
    
    def chunk_large_document(self, doc: Dict[str, str], chunk_size: int = 2000, overlap: int = 200) -> List[Dict]:
        """
        Split large documents into chunks
        
        Args:
            doc: Document dictionary
            chunk_size: Maximum characters per chunk
            overlap: Overlapping characters between chunks
            
        Returns:
            List of chunked documents
        """
        text = doc['text']
        
        if len(text) <= chunk_size:
            return [doc]  # No chunking needed
        
        chunks = []
        start = 0
        chunk_num = 1
        
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk_text.rfind('.')
                last_newline = chunk_text.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size * 0.7:  # At least 70% of chunk
                    end = start + break_point + 1
                    chunk_text = text[start:end]
            
            # Create chunk
            chunk = {
                'id': f"{doc['id']}_chunk_{chunk_num}",
                'text': chunk_text.strip(),
                'metadata': {
                    **doc['metadata'],
                    'chunk_number': chunk_num,
                    'is_chunked': True,
                    'total_chunks': 0  # Will update after all chunks created
                }
            }
            chunks.append(chunk)
            
            # Move to next chunk with overlap
            start = end - overlap
            chunk_num += 1
        
        # Update total chunks
        for chunk in chunks:
            chunk['metadata']['total_chunks'] = len(chunks)
        
        print(f"  📑 Split into {len(chunks)} chunks")
        return chunks
    
    def process_all_documents(self, chunk_large_docs: bool = True) -> List[Dict]:
        """
        Process all documents in documents directory
        
        Args:
            chunk_large_docs: Whether to chunk documents larger than 2000 chars
            
        Returns:
            List of processed documents
        """
        print("\n" + "="*80)
        print("📂 DOCUMENT INGESTION")
        print("="*80)
        print(f"📁 Scanning directory: {self.documents_dir}")
        
        # Find all supported files
        supported_exts = ['.pdf', '.txt', '.md', '.docx']
        files = []
        for ext in supported_exts:
            files.extend(self.documents_dir.glob(f'*{ext}'))
        
        if not files:
            print(f"\n⚠️  No documents found in {self.documents_dir}")
            print(f"   Supported formats: {', '.join(supported_exts)}")
            return []
        
        print(f"\n📄 Found {len(files)} documents")
        print("="*80)
        
        # Process each document
        all_docs = []
        for filepath in files:
            doc = self.process_document(filepath)
            if doc:
                # Chunk if needed
                if chunk_large_docs and len(doc['text']) > 2000:
                    chunks = self.chunk_large_document(doc)
                    all_docs.extend(chunks)
                else:
                    all_docs.append(doc)
        
        print("="*80)
        print(f"✅ Processed {len(files)} files → {len(all_docs)} document chunks")
        print("="*80)
        
        return all_docs


def main():
    """Main ingestion workflow"""
    print("\n" + "="*80)
    print("🗄️  ECONOMIC POLICY KNOWLEDGE BASE - DOCUMENT INGESTION")
    print("="*80)
    
    # Initialize processor
    processor = DocumentProcessor(documents_dir="../documents")
    
    # Process all documents
    documents = processor.process_all_documents(chunk_large_docs=True)
    
    if not documents:
        print("\n❌ No documents to ingest!")
        print("\n💡 Add documents to: economic-agent/documents/")
        print("   Supported formats: PDF, TXT, MD, DOCX")
        return
    
    # Initialize knowledge base
    print("\n📊 Initializing Pinecone knowledge base...")
    kb = EconomicKnowledgeBase()
    
    # Add documents to knowledge base
    kb.add_documents(documents)
    
    # Show stats
    stats = kb.get_stats()
    print("\n" + "="*80)
    print("📈 KNOWLEDGE BASE STATISTICS")
    print("="*80)
    print(f"Total documents: {stats['total_vectors']}")
    print(f"Index name: {stats['index_name']}")
    print(f"Embedding dimension: {stats['dimension']}")
    print("="*80)
    
    # Test search
    print("\n🔍 Testing search functionality...")
    test_query = "tax policy impact on revenue"
    results = kb.search(test_query, top_k=3)
    
    print(f"\nQuery: '{test_query}'")
    print(f"Found {len(results)} results:\n")
    
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc['title']} (Score: {doc['score']:.3f})")
        print(f"   Source: {doc['source']}")
        print(f"   Category: {doc['category']}")
        print()
    
    print("="*80)
    print("✅ INGESTION COMPLETE!")
    print("="*80)
    print("\n💡 Your Economic Policy MP can now use this knowledge base!")
    print("   Run: python ../parliament_member.py")


if __name__ == "__main__":
    main()
