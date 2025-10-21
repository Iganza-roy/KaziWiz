"""
Search Tools for Economic Analysis Agent
Provides concise, factual data for economic decision-making
"""
import json
import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))


class EconomicSearchTools:
    """Search tools optimized for economic data gathering"""
    
    @tool("Search economic data")
    def search_economic_data(query: str) -> str:
        """Search for economic data, statistics, and financial information.
        
        Args:
            query: Search query for economic data
            
        Returns:
            Search results with economic data and statistics
        """
        # Handle both string and dict inputs from CrewAI wrapper
        if isinstance(query, dict):
            query = query.get('query', '') or query.get('q', '') or str(query)
        
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": str(query), "num": 3})
        headers = {
            "X-API-KEY": os.environ.get("SERPER_API_KEY", ""),
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
            response_data = response.json()
            
            # Debug: Check response status
            if response.status_code != 200:
                return f"API Error: Status {response.status_code} - {response.text[:200]}"
            
            if "organic" not in response_data:
                return f"No organic results. Response keys: {list(response_data.keys())}"
            
            results = response_data["organic"]
            output = []
            
            for result in results[:3]:  # Only top 3 results
                try:
                    # Extract only key information
                    output.append(f"• {result['title']}\n  {result['snippet']}\n  Source: {result['link']}")
                except KeyError:
                    continue
            
            return "\n\n".join(output) if output else "No relevant economic data found."
        
        except requests.exceptions.RequestException as e:
            return f"Network error: {str(e)}"
        except Exception as e:
            return f"Search error: {str(e)}"
    
    @tool("Search policy case studies")
    def search_policy_cases(policy_type: str) -> str:
        """Search for real-world case studies of similar policies.
        
        Args:
            policy_type: Type of policy to search for case studies
            
        Returns:
            Case studies with implementation results and outcomes
        """
        # Handle both string and dict inputs
        if isinstance(policy_type, dict):
            policy_type = policy_type.get('policy_type', '') or policy_type.get('query', '') or str(policy_type)
        
        query = f"{policy_type} policy implementation case study results statistics international"
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query, "num": 3})
        headers = {
            "X-API-KEY": os.environ.get("SERPER_API_KEY", ""),
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
            
            if "organic" not in response.json():
                return "No case studies found."
            
            results = response.json()["organic"]
            output = []
            
            for result in results[:3]:
                try:
                    output.append(f"📊 {result['title']}\n   {result['snippet']}")
                except KeyError:
                    continue
            
            return "\n\n".join(output) if output else "No relevant case studies found."
        
        except Exception as e:
            return f"Search error: {str(e)}"
    
    @tool("Search financial statistics")
    def search_financial_stats(topic: str) -> str:
        """Search for specific financial statistics, revenue data, or economic indicators.
        
        Args:
            topic: Financial topic to search statistics for
            
        Returns:
            Financial statistics and numerical data
        """
        # Handle both string and dict inputs
        if isinstance(topic, dict):
            topic = topic.get('topic', '') or topic.get('query', '') or str(topic)
        
        query = f"{topic} statistics revenue data numbers financial report India"
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query, "num": 3})
        headers = {
            "X-API-KEY": os.environ.get("SERPER_API_KEY", ""),
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
            
            if "organic" not in response.json():
                return "No financial statistics found."
            
            results = response.json()["organic"]
            output = []
            
            for result in results[:3]:
                try:
                    # Focus on snippets that contain numbers
                    snippet = result['snippet']
                    if any(char.isdigit() for char in snippet):  # Only include if contains numbers
                        output.append(f"💰 {result['title']}\n   {snippet}")
                except KeyError:
                    continue
            
            return "\n\n".join(output) if output else "No numerical data found."
        
        except Exception as e:
            return f"Search error: {str(e)}"
    
    @tool("Search market data")
    def search_market_data(market_topic: str) -> str:
        """Search for market trends, business impact data, and industry statistics.
        
        Args:
            market_topic: Market or business topic to search data for
            
        Returns:
            Market trends and business impact data
        """
        # Handle both string and dict inputs
        if isinstance(market_topic, dict):
            market_topic = market_topic.get('market_topic', '') or market_topic.get('query', '') or str(market_topic)
        
        query = f"{market_topic} India market data trends business impact statistics"
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query, "num": 3})
        headers = {
            "X-API-KEY": os.environ.get("SERPER_API_KEY", ""),
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
            
            if "organic" not in response.json():
                return "No market data found."
            
            results = response.json()["organic"]
            output = []
            
            for result in results[:2]:  # Only top 2 for market data
                try:
                    output.append(f"📈 {result['title']}\n   {result['snippet']}")
                except KeyError:
                    continue
            
            return "\n\n".join(output) if output else "No market data found."
        
        except Exception as e:
            return f"Search error: {str(e)}"
