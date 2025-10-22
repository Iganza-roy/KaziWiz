"""
Research Tools Module
Provides web search and browsing capabilities for agents
"""

import os
from crewai_tools import SerperDevTool, ScrapeWebsiteTool


class ResearchTools:
    """Centralized tool management for agent research"""
    
    def __init__(self):
        # Initialize tools with API keys from environment
        self.serper_api_key = os.environ.get("SERPER_API_KEY")
        
        # Web Search Tool (Google Search via Serper)
        self.search_tool = None
        if self.serper_api_key:
            try:
                self.search_tool = SerperDevTool()
                print(f"✅ SerperDevTool initialized with API key")
            except Exception as e:
                print(f"⚠️  SerperDevTool initialization failed: {e}")
        else:
            print("⚠️  SERPER_API_KEY not found - web search disabled")
        
        # Website scraping tool
        try:
            self.scrape_tool = ScrapeWebsiteTool()
            print(f"✅ ScrapeWebsiteTool initialized")
        except Exception as e:
            print(f"⚠️  ScrapeWebsiteTool initialization failed: {e}")
            self.scrape_tool = None
    
    def get_research_tools(self):
        """Get all available research tools"""
        tools = []
        
        if self.search_tool:
            tools.append(self.search_tool)
        
        if self.scrape_tool:
            tools.append(self.scrape_tool)
        
        return tools
    
    def get_search_tool(self):
        """Get just the search tool"""
        return self.search_tool if self.search_tool else None
    
    def is_search_available(self):
        """Check if web search is available"""
        return self.search_tool is not None
