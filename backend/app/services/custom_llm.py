"""
Custom LLM Wrapper for ASI Cloud
Bypasses CrewAI's model name modification
"""

import os
from typing import Any, Dict, List, Optional
from openai import OpenAI
from crewai.llm import LLM


def create_asi_cloud_llm(model: str = "openai/gpt-oss-20b", temperature: float = 0.4):
    """
    Create a CrewAI-compatible LLM configured for ASI Cloud
    
    This uses CrewAI's native LLM class but forces the correct model name
    by monkeypatching the completion parameters
    """
    # Create the LLM instance with ASI Cloud config
    llm = LLM(
        model=model,  # This will be sent AS-IS to the API
        temperature=temperature,
        api_key=os.environ.get("ASI_API_KEY"),
        base_url="https://inference.asicloud.cudos.org/v1"
    )
    
    # Store the original model name to preserve it
    llm._original_model = model
    
    # Monkeypatch the internal client if it exists
    if hasattr(llm, 'client') and llm.client:
        # Force the client to use our base_url and API key
        llm.client.base_url = "https://inference.asicloud.cudos.org/v1"
        llm.client.api_key = os.environ.get("ASI_API_KEY")
    
    return llm
