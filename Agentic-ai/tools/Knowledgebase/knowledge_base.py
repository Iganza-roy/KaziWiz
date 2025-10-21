"""
Economic Knowledge Base
Pinecone integration for storing and retrieving economic policy documents
"""
import os
from typing import List, Dict, Optional
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class EconomicKnowledgeBase:
    """Manages Pinecone vector database for economic policy documents"""
    
    def __init__(self):
        """Initialize Pinecone connection and embeddings"""
        # Get API key
        self.api_key = os.getenv('PINECONE_API_KEY')
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY not found in environment variables")
        
        self.index_name = os.getenv('PINECONE_INDEX_NAME', 'economic-policies')
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.api_key)
        
        # Create or connect to index
        self._setup_index()
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        print(f"✅ Connected to Pinecone index: {self.index_name}")
    
    def _setup_index(self):
        """Create index if it doesn't exist"""
        existing_indexes = [idx.name for idx in self.pc.list_indexes()]
        
        if self.index_name not in existing_indexes:
            print(f"📊 Creating new index: {self.index_name}")
            self.pc.create_index(
                name=self.index_name,
                dimension=384,  # all-MiniLM-L6-v2 dimension
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
        
        self.index = self.pc.Index(self.index_name)
    
    def add_documents(self, documents: List[Dict]):
        """
        Add documents to knowledge base
        
        Args:
            documents: List of dicts with 'id', 'text', and 'metadata'
        """
        if not documents:
            print("⚠️  No documents to add")
            return
        
        print(f"\n📤 Adding {len(documents)} documents to Pinecone...")
        
        # Process in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            
            # Generate embeddings
            texts = [doc['text'] for doc in batch]
            embeddings = self.embeddings.embed_documents(texts)
            
            # Prepare vectors
            vectors = []
            for doc, embedding in zip(batch, embeddings):
                vector = {
                    'id': doc['id'],
                    'values': embedding,
                    'metadata': {
                        **doc['metadata'],
                        'text': doc['text'][:1000]  # Store first 1000 chars
                    }
                }
                vectors.append(vector)
            
            # Upsert to Pinecone
            self.index.upsert(vectors=vectors)
            print(f"  ✅ Uploaded batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
        
        print(f"✅ Successfully added {len(documents)} documents")
    
    def search(self, query: str, top_k: int = 5, filter: Optional[Dict] = None) -> List[Dict]:
        """
        Search for relevant documents
        
        Args:
            query: Search query text
            top_k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of matching documents with scores
        """
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # Search Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            filter=filter,
            include_metadata=True
        )
        
        # Format results
        documents = []
        for match in results['matches']:
            doc = {
                'id': match['id'],
                'score': match['score'],
                'text': match['metadata'].get('text', ''),
                **match['metadata']
            }
            documents.append(doc)
        
        return documents
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        stats = self.index.describe_index_stats()
        return {
            'total_vectors': stats['total_vector_count'],
            'dimension': stats['dimension'],
            'index_name': self.index_name
        }
    
    def delete_all(self):
        """Delete all vectors from index (use with caution!)"""
        self.index.delete(delete_all=True)
        print("🗑️  All vectors deleted from index")


# For testing
if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧪 TESTING ECONOMIC KNOWLEDGE BASE")
    print("="*80)
    
    # Initialize
    kb = EconomicKnowledgeBase()
    
    # Get stats
    stats = kb.get_stats()
    print(f"\n📊 Knowledge Base Stats:")
    print(f"   Total Vectors: {stats['total_vectors']}")
    print(f"   Dimension: {stats['dimension']}")
    print(f"   Index: {stats['index_name']}")
    
    # Test search if vectors exist
    if stats['total_vectors'] > 0:
        print("\n🔍 Testing search...")
        results = kb.search("tax policy reforms", top_k=3)
        
        print(f"\nFound {len(results)} results:\n")
        for i, doc in enumerate(results, 1):
            print(f"{i}. Score: {doc['score']:.3f}")
            print(f"   Title: {doc.get('title', 'N/A')}")
            print(f"   Category: {doc.get('category', 'N/A')}")
            print(f"   Source: {doc.get('source', 'N/A')}")
            print()
    else:
        print("\n⚠️  No vectors in knowledge base")
        print("   Run: python ingest_documents.py")
    
    print("="*80)
    print("✅ TEST COMPLETE")
    print("="*80)
