"""
Output Validation Module
Validates LLM outputs to ensure they are policy analysis, not code
"""

import re
import logging

logger = logging.getLogger(__name__)


class OutputValidator:
    """Validates and sanitizes LLM outputs"""
    
    # Code-like patterns that indicate hallucination
    CODE_PATTERNS = [
        r'```[\w]*\n',  # Code blocks
        r'#include\s+<',  # C/C++ includes
        r'import\s+\w+\s+from',  # Python imports
        r'def\s+\w+\s*\(',  # Python function definitions
        r'class\s+\w+\s*[:\(]',  # Class definitions
        r'function\s+\w+\s*\(',  # JavaScript functions
        r'<\?php',  # PHP tags
        r'<!DOCTYPE',  # HTML
        r'<script',  # Script tags
        r'glsl|shader|vertex|fragment',  # Graphics programming
        r'layout\s*\(location',  # GLSL
        r'gl_Position',  # OpenGL
        r'#version\s+\d+',  # Shader versions
        r'int\s+main\s*\(',  # C/C++ main
        r'public\s+static\s+void\s+main',  # Java main
        r'---\nlayout:',  # Markdown frontmatter
        r'\$\$\s*\\begin\{',  # LaTeX math blocks
    ]
    
    # Keywords that suggest code instead of policy analysis
    CODE_KEYWORDS = [
        'jupyter', 'notebook', 'algorithm', 'implementation',
        'compile', 'runtime', 'binary', 'pointer', 'malloc',
        'vertex', 'shader', 'rendering', 'opengl', 'webgl',
        'array', 'buffer', 'matrix multiplication', 'gpu',
        'tensorflow', 'pytorch', 'neural network architecture',
        'docker', 'kubernetes', 'api endpoint', 'sql query'
    ]
    
    @staticmethod
    def is_valid_policy_output(output: str) -> tuple[bool, str]:
        """
        Check if output is valid policy analysis
        
        Returns:
            (is_valid, reason)
        """
        if not output or len(output) < 50:
            return False, "Output too short"
        
        # Check for code block patterns
        for pattern in OutputValidator.CODE_PATTERNS:
            if re.search(pattern, output, re.IGNORECASE | re.MULTILINE):
                return False, f"Contains code pattern: {pattern}"
        
        # Count code-like keywords
        output_lower = output.lower()
        code_keyword_count = sum(1 for kw in OutputValidator.CODE_KEYWORDS if kw in output_lower)
        
        if code_keyword_count >= 3:
            return False, f"Contains too many code keywords ({code_keyword_count})"
        
        # Check if it mentions policy-related terms
        policy_keywords = [
            'policy', 'carbon tax', 'economic', 'fiscal', 'impact',
            'government', 'revenue', 'emission', 'climate', 'environment',
            'stakeholder', 'implementation', 'analysis', 'evidence'
        ]
        
        policy_keyword_count = sum(1 for kw in policy_keywords if kw in output_lower)
        
        if policy_keyword_count < 2:
            return False, "Lacks policy-related content"
        
        return True, "Valid policy analysis"
    
    @staticmethod
    def extract_policy_content(output: str) -> str:
        """
        Try to extract policy analysis from mixed content
        Removes code blocks and focuses on prose
        """
        # Remove code blocks
        output = re.sub(r'```[\w]*\n.*?```', '', output, flags=re.DOTALL)
        
        # Remove HTML/XML tags
        output = re.sub(r'<[^>]+>', '', output)
        
        # Remove LaTeX math blocks
        output = re.sub(r'\$\$.*?\$\$', '', output, flags=re.DOTALL)
        
        # Remove frontmatter
        output = re.sub(r'^---.*?---', '', output, flags=re.DOTALL | re.MULTILINE)
        
        # Clean up extra whitespace
        output = re.sub(r'\n{3,}', '\n\n', output)
        output = output.strip()
        
        return output
    
    @staticmethod
    def create_fallback_response(agent_role: str, policy_topic: str) -> str:
        """
        Create a basic fallback response when LLM hallucinates
        """
        return f"""
**{agent_role} Analysis: {policy_topic}**

**Position:** CONDITIONAL SUPPORT

**Key Considerations:**

1. **Evidence Required:** Due to technical limitations in generating detailed analysis, I recommend consulting recent policy research reports and case studies on {policy_topic}.

2. **Economic Impact:** The economic implications of {policy_topic} require careful evaluation of fiscal impacts, market effects, and distributional consequences across different stakeholder groups.

3. **Implementation Feasibility:** Successful implementation depends on regulatory framework design, enforcement mechanisms, and stakeholder engagement.

4. **Risk Assessment:** Potential unintended consequences must be evaluated through pilot programs and phased rollout approaches.

**Recommendation:** Conduct comprehensive cost-benefit analysis and stakeholder consultation before proceeding with policy implementation.

*Note: This is a placeholder response. For detailed analysis, please consult subject matter experts and peer-reviewed policy research.*
"""
