"""
Knowledge Base Retriever Tools for CrewAI Agents
Simplified version without decorators for debugging
"""
from typing import List, Dict
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from knowledge_base import EconomicKnowledgeBase
except ImportError as e:
    print(f"Warning: Could not import EconomicKnowledgeBase: {e}")
    EconomicKnowledgeBase = None

# Initialize knowledge base (lazy loading)
_kb_instance = None

def get_kb():
    """Get or create knowledge base instance"""
    global _kb_instance
    if _kb_instance is None and EconomicKnowledgeBase is not None:
        try:
            _kb_instance = EconomicKnowledgeBase()
        except Exception as e:
            print(f"Warning: Could not initialize knowledge base: {e}")
            return None
    return _kb_instance


def search_policy_knowledge_base_func(query: str) -> str:
    """
    Search the internal policy knowledge base for relevant information.
    
    Args:
        query: The search query
        
    Returns:
        Formatted search results with sources
    """
    try:
        kb = get_kb()
        if kb is None:
            return "Knowledge base not available"
            
        results = kb.search(query, top_k=3)
        
        if not results:
            return f"No results found in knowledge base for query: '{query}'"
        
        # Format results
        output = [f"Knowledge Base Search Results for: '{query}'\n"]
        output.append("="*80 + "\n")
        
        for i, doc in enumerate(results, 1):
            output.append(f"\n{i}. {doc.get('title', 'Untitled')}")
            output.append(f"   Source: {doc.get('source', 'Unknown')}")
            output.append(f"   Category: {doc.get('category', 'general')}")
            output.append(f"   Relevance: {doc['score']:.3f}")
            
            # Show first 500 chars
            text = doc.get('text', '')
            preview = text[:500]
            if len(text) > 500:
                preview += "..."
            output.append(f"\n   Content Preview:")
            output.append(f"   {preview}\n")
            output.append("-"*80)
        
        output.append(f"\nFound {len(results)} relevant documents")
        output.append("\nCite these sources in your response!")
        
        return "\n".join(output)
    
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"


def search_policy_by_category_func(category: str, query: str = "") -> str:
    """
    Search for policies within a specific category.
    
    Args:
        category: The policy category
        query: Optional search query
        
    Returns:
        Formatted search results
    """
    try:
        kb = get_kb()
        if kb is None:
            return "Knowledge base not available"
            
        search_query = query if query else category
        results = kb.search(search_query, top_k=5, filter={'category': category})
        
        if not results:
            return f"No documents found in category '{category}'"
        
        # Format results
        output = [f"Category Search: {category.upper()}\n"]
        if query:
            output.append(f"Query: {query}\n")
        output.append("="*80 + "\n")
        
        for i, doc in enumerate(results, 1):
            output.append(f"\n{i}. {doc.get('title', 'Untitled')}")
            output.append(f"   Source: {doc.get('source', 'Unknown')}")
            output.append(f"   Relevance: {doc['score']:.3f}")
            
            # Show snippet
            text = doc.get('text', '')
            preview = text[:300]
            if len(text) > 300:
                preview += "..."
            output.append(f"\n   {preview}\n")
            output.append("-"*80)
        
        output.append(f"\nFound {len(results)} documents in '{category}' category")
        
        return "\n".join(output)
    
    except Exception as e:
        return f"Error searching category '{category}': {str(e)}"


def get_knowledge_base_stats_func() -> str:
    """Get statistics about the knowledge base"""
    try:
        kb = get_kb()
        if kb is None:
            return "Knowledge base not available"
            
        stats = kb.get_stats()
        
        output = [
            "KNOWLEDGE BASE STATISTICS",
            "="*80,
            f"Total Documents: {stats['total_vectors']}",
            f"Index Name: {stats['index_name']}",
            f"Embedding Dimension: {stats['dimension']}",
            "",
            "Available Categories:",
            "  * taxation: Tax policies, GST, income tax",
            "  * budget: Budget policies, fiscal spending",
            "  * subsidy: Subsidy programs, welfare",
            "  * trade: Trade policies, import/export",
            "  * infrastructure: Infrastructure development",
            "  * monetary: Monetary policies, interest rates",
            "  * employment: Employment policies, labor",
            "  * gdp: GDP growth policies",
            "="*80
        ]
        
        return "\n".join(output)
    
    except Exception as e:
        return f"Error getting knowledge base stats: {str(e)}"


def get_knowledge_base_tools():
    """
    Get list of knowledge base tools as LangChain @tool decorated functions.
    
    Returns:
        List of tool functions
    """
    try:
        from langchain.tools import tool
        
        @tool("search_policy_knowledge_base")
        def search_policy_knowledge_base(query: str) -> str:
            """Search the internal policy knowledge base for relevant information. Use this to find GST, taxation, TDS, and other policy information from Document 40.docx and other uploaded documents."""
            return search_policy_knowledge_base_func(query)
        
        @tool("search_policy_by_category")
        def search_policy_by_category(category_query: str) -> str:
            """Search for policies within a specific category. Input format: 'category' or 'category: query'. Categories: taxation, budget, subsidy, trade, infrastructure, monetary, employment, gdp."""
            if ':' in category_query:
                parts = category_query.split(':', 1)
                category = parts[0].strip()
                query = parts[1].strip()
            else:
                category = category_query.strip()
                query = ""
            return search_policy_by_category_func(category, query)
        
        @tool("get_knowledge_base_statistics")
        def get_knowledge_base_statistics(query: str = "") -> str:
            """Get statistics about the knowledge base including total documents and available categories. Shows what information is available."""
            return get_knowledge_base_stats_func()
        
        return [
            search_policy_knowledge_base,
            search_policy_by_category,
            get_knowledge_base_statistics
        ]
    
    except Exception as e:
        print(f"Error creating knowledge base tools: {e}")
        import traceback
        traceback.print_exc()
        return []


# For testing
if __name__ == "__main__":
    print("\n" + "="*80)
    print("TESTING KNOWLEDGE BASE RETRIEVER")
    print("="*80)
    
    # Test getting tools
    tools = get_knowledge_base_tools()
    print(f"\nGot {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool['name']}")
    
    # Test search
    print("\nTesting search...")
    result = search_policy_knowledge_base_func("GST administration")
    print(result)
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
