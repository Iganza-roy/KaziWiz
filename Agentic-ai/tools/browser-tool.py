"""
Browser Tools for Economic Analysis Agent
Provides concise web scraping for economic data extraction
"""
import json
import os
import requests
from langchain.tools import tool


class EconomicBrowserTools:
    """Browser tools optimized for extracting economic facts and data"""
    
    @tool("Extract key facts from website")
    def extract_key_facts(website_url):
        """Scrape a website and extract only key facts, statistics, and data points.
        Returns a concise summary focused on actionable information."""
        
        browserless_key = os.environ.get('BROWSERLESS_API_KEY')
        if not browserless_key:
            return "Browserless API key not configured. Skipping web scraping."
        
        try:
            url = f"https://chrome.browserless.io/content?token={browserless_key}"
            payload = json.dumps({"url": website_url})
            headers = {"cache-control": "no-cache", "content-type": "application/json"}
            
            response = requests.request("POST", url, headers=headers, data=payload, timeout=30)
            
            if response.status_code != 200:
                return f"Could not access website: {website_url}"
            
            # Extract text content
            content = response.text
            
            # Simple extraction of key points (first 2000 chars with numbers/data)
            lines = content.split('\n')
            key_facts = []
            
            for line in lines:
                line = line.strip()
                # Look for lines with numbers, percentages, or currency
                if any(char.isdigit() for char in line) and len(line) > 20 and len(line) < 200:
                    key_facts.append(line)
                    if len(key_facts) >= 10:  # Limit to 10 key facts
                        break
            
            if key_facts:
                return "Key Facts Extracted:\n" + "\n• ".join(key_facts[:10])
            else:
                return f"No specific data points found on {website_url}"
        
        except Exception as e:
            return f"Error extracting data: {str(e)}"
    
    @tool("Get economic report summary")
    def get_report_summary(report_url):
        """Extract executive summary and key findings from economic reports or policy documents.
        Returns only the most important points and data."""
        
        browserless_key = os.environ.get('BROWSERLESS_API_KEY')
        if not browserless_key:
            return "Browserless API key not configured."
        
        try:
            url = f"https://chrome.browserless.io/content?token={browserless_key}"
            payload = json.dumps({"url": report_url})
            headers = {"cache-control": "no-cache", "content-type": "application/json"}
            
            response = requests.request("POST", url, headers=headers, data=payload, timeout=30)
            
            if response.status_code != 200:
                return f"Could not access report: {report_url}"
            
            content = response.text
            
            # Look for summary sections
            summary_keywords = ['summary', 'executive', 'key findings', 'conclusion', 'highlights']
            lines = content.lower().split('\n')
            
            summary_lines = []
            capture = False
            
            for i, line in enumerate(lines):
                # Start capturing if we find summary keywords
                if any(keyword in line for keyword in summary_keywords):
                    capture = True
                    continue
                
                # Capture next 15 lines after finding summary section
                if capture and len(summary_lines) < 15:
                    clean_line = line.strip()
                    if len(clean_line) > 30:  # Only meaningful lines
                        summary_lines.append(clean_line)
                
                if len(summary_lines) >= 15:
                    break
            
            if summary_lines:
                return "Report Summary:\n" + "\n".join(summary_lines[:10])
            else:
                # Fallback: return first substantial content
                substantial = [l.strip() for l in lines if len(l.strip()) > 50][:8]
                return "Report Excerpt:\n" + "\n".join(substantial)
        
        except Exception as e:
            return f"Error accessing report: {str(e)}"
    
    @tool("Quick web fact check")
    def quick_fact_check(url):
        """Quickly check a specific URL for factual data, numbers, and key information.
        Returns only data points, no fluff."""
        
        browserless_key = os.environ.get('BROWSERLESS_API_KEY')
        if not browserless_key:
            return "Browserless API key not configured."
        
        try:
            api_url = f"https://chrome.browserless.io/content?token={browserless_key}"
            payload = json.dumps({"url": url})
            headers = {"cache-control": "no-cache", "content-type": "application/json"}
            
            response = requests.request("POST", api_url, headers=headers, data=payload, timeout=20)
            
            if response.status_code != 200:
                return f"Could not access: {url}"
            
            content = response.text[:5000]  # First 5000 chars only
            
            # Extract sentences with numbers, currency, or percentages
            import re
            facts = []
            sentences = content.split('.')
            
            for sentence in sentences[:50]:  # Check first 50 sentences
                sentence = sentence.strip()
                # Look for numbers, currency symbols, or percentage signs
                if re.search(r'[\d$₹€£¥%]', sentence) and len(sentence) > 30 and len(sentence) < 250:
                    facts.append(sentence)
                    if len(facts) >= 8:  # Max 8 facts
                        break
            
            if facts:
                return "Facts Found:\n• " + "\n• ".join(facts)
            else:
                return f"No specific facts found at {url}"
        
        except Exception as e:
            return f"Error: {str(e)}"
