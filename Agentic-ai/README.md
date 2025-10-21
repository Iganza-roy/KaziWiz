# 🎯 Multi-Expert AI Policy Deliberation System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Latest-green.svg)](https://github.com/joaomdmoura/crewAI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **An advanced multi-agent AI system that orchestrates 26+ expert agents to conduct comprehensive policy analysis through democratic deliberation, research, debate, and voting.**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [API Reference](#api-reference)
- [Tools & Integrations](#tools--integrations)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

### 📚 Additional Documentation

- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Complete documentation navigation guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture and system design (6 layers)
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation for all classes and methods
- **[EXAMPLES.md](EXAMPLES.md)** - 20 detailed usage examples and tutorials
- **[TOOL_USAGE_FLOW.md](TOOL_USAGE_FLOW.md)** - Detailed explanation of when and how tools are used

---

## 🌟 Overview

This system simulates a **multi-expert policy deliberation process** where AI agents with different specializations collaborate to analyze complex policy decisions. Think of it as a "digital think tank" where experts from economics, social welfare, law, geospatial analysis, and more work together to evaluate policy proposals.

### What Makes This Special?

- **26+ Specialized AI Experts**: Each with distinct expertise and perspectives
- **Democratic Decision-Making**: Agents debate, vote, and reach consensus
- **Evidence-Based Analysis**: Integrated web search and knowledge base tools
- **Multiple Execution Modes**: From quick analysis to comprehensive deliberation
- **Transparent Process**: Full audit trail of research, debates, and voting
- **Real-World Applications**: Used for policy analysis, urban planning, economic evaluation

---

## ✨ Key Features

### 🎭 Multi-Expert System
- **Economic Experts** (4): Macro, Micro, Policy Impact, Trade & Investment
- **Social Welfare Experts** (3): Healthcare, Education, Housing
- **Geospatial Experts** (3): Geographic Poverty, Demographics, Resource Access
- **Income Inequality Experts** (3): Causes, Redistribution, Impact Assessment
- **Resource Allocation Experts** (3): Optimization, Real-time Prioritization, Efficiency
- **Feedback & Adaptation Experts** (2): Policy Monitoring, Adaptive Policy
- **Core Experts** (6): Economic, Social, Geospatial, Income, Resource, Legal
- **Orchestration Experts** (3): Problem Statement, Turn Management, Voting Coordinator

### 🚀 Execution Modes
1. **Full Mode**: Complete workflow (Research → Debate → Vote → Report) - ~25-40 min
2. **Quick Mode**: Streamlined analysis (Research → Vote → Report) - ~15-25 min
3. **Research Only**: Data gathering phase - ~10-15 min
4. **Debate Only**: Argumentation and voting - ~8-12 min

### 🔧 Advanced Capabilities
- **Web Search Integration**: Real-time data gathering via Serper API
- **Knowledge Base**: Optional Pinecone vector database for policy documents
- **Interactive CLI**: User-friendly prompts for guided analysis
- **Agentverse Integration**: Deploy as distributed AI agent
- **Flexible APIs**: Programmatic access via Python
- **Comprehensive Reports**: Auto-generated policy analysis documents

### 🎯 Output Quality
- Detailed research from 26 expert perspectives
- Evidence-based arguments with citations
- Democratic voting with weighted scores
- Consensus analysis and minority opinions
- Actionable recommendations and conditions

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                     │
│  • CLI (Interactive Mode)                                   │
│  • Programmatic API (Python)                                │
│  • Agentverse Integration (Distributed)                     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              ORCHESTRATION LAYER (uagent_main.py)           │
│  • AutoPolicyDeliberationSystem                             │
│  • Mode Selection (Full/Quick/Research/Debate)              │
│  • Phase Management (8 Phases)                              │
│  • Result Aggregation                                       │
└─────────────────────────────────────────────────────────────┘
                           ↓
        ┌──────────────────┴──────────────────┐
        ↓                                      ↓
┌──────────────────┐                 ┌──────────────────┐
│   AGENT LAYER    │                 │   TASK LAYER     │
│  (ai_agent.py)   │                 │(ai_agent_task.py)│
│                  │                 │                  │
│  • 26+ Experts   │◄───────────────►│  • Research Tasks│
│  • Specialized   │                 │  • Debate Tasks  │
│  • Role/Goal     │                 │  • Voting Tasks  │
│  • Backstory     │                 │  • Tool Access   │
└──────────────────┘                 └──────────────────┘
        ↓                                      ↓
┌─────────────────────────────────────────────────────────────┐
│                     TOOL LAYER                              │
│  • Web Search (Serper API) - 4 tools                        │
│  • Knowledge Base (Pinecone) - 3 tools (optional)           │
│  • Economic Data Search                                     │
│  • Policy Case Studies                                      │
│  • Financial Statistics                                     │
│  • Market Data                                              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                      LLM LAYER                              │
│  • ASI Cloud API (OpenAI-compatible)                        │
│  • Model: asi1-mini                                         │
│  • Temperature: 0.7                                         │
└─────────────────────────────────────────────────────────────┘
```

### 8-Phase Deliberation Process

```
Phase 1: INITIALIZATION
└─► Initialize 26+ expert agents with specialized roles

Phase 2: PROBLEM STATEMENT
└─► Clarification expert defines the policy challenge
    ❌ No tools used (problem framing)

Phase 3: TURN MANAGEMENT
└─► Orchestration expert sets discussion rules
    ❌ No tools used (process setup)

Phase 4: RESEARCH ⭐ TOOLS USED HERE ⭐
└─► All 26 experts gather data using tools (parallel execution)
    ✅ Web Search Tools (4 tools via Serper API):
       • search_economic_data("query") → Real-time economic stats
       • search_policy_cases("type") → International case studies
       • search_financial_stats("topic") → Financial data
       • search_market_data("topic") → Market trends
    ✅ Knowledge Base Tools (3 tools via Pinecone):
       • search_policy_knowledge_base("query") → Internal policies
       • search_policy_by_category("category") → Categorized docs
       • get_knowledge_base_statistics() → KB metadata
    📊 Each expert:
       1. Uses tools to search for relevant data
       2. LLM analyzes tool results with expert knowledge
       3. Forms evidence-based position with citations
       4. Output: Research analysis with sources

Phase 5: DEBATE (Full mode only)
└─► Structured argumentation with evidence presentation
    ✅ Tools optionally available for fact-checking
    📊 Experts use research results from Phase 4

Phase 6: VOTING
└─► Democratic voting with rationale
    ❌ No tools needed (uses debate summary)
    • Strongly Support (+2)
    • Support (+1)
    • Conditional (0)
    • Oppose (-1)
    • Strongly Oppose (-2)
    • Abstain (0)

Phase 7: ANNOUNCEMENT
└─► Vote tallying, consensus analysis, final decision
    ❌ No tools needed (aggregation)

Phase 8: REPORT GENERATION
└─► Comprehensive documentation of entire process
    ❌ No tools needed (formatting)
```

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd Agentic-ai
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install crewai crewai-tools langchain python-dotenv requests
```

### Optional Dependencies

```bash
# For knowledge base (optional)
pip install pinecone-client

# For Agentverse integration (optional)
pip install uagents uagents-adapter
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Required: ASI Cloud API for LLM
ASI_API_KEY=your_asi_cloud_api_key_here

# Optional: Web search capabilities
SERPER_API_KEY=your_serper_api_key_here

# Optional: Knowledge base (Pinecone)
PINECONE_API_KEY=your_pinecone_api_key_here

# Optional: Agentverse deployment
AV_API_KEY=your_agentverse_api_key_here
```

**Get API Keys:**
- ASI Cloud: [https://inference.asicloud.cudos.org/](https://inference.asicloud.cudos.org/)
- Serper: [https://serper.dev/](https://serper.dev/)
- Pinecone: [https://www.pinecone.io/](https://www.pinecone.io/)
- Agentverse: [https://agentverse.ai/](https://agentverse.ai/)

---

## 🚀 Quick Start

### 1. Interactive Mode (Recommended for First-Time Users)

```bash
python uagent_main.py --interactive
```

You'll be prompted for:
- Policy topic to analyze
- City/region context
- Policy type
- Time range
- Evaluation criteria
- Execution mode

### 2. Quick Analysis (Default Policy)

```bash
python uagent_main.py --mode quick
```

This runs a streamlined analysis on the default policy: "Poverty Reduction and Economic Outcome in Urban Areas"

### 3. Full Analysis

```bash
python uagent_main.py
```

Runs the complete deliberation process including debate phase (~25-40 minutes).

### 4. Custom Policy

```bash
python uagent_main.py --policy "Universal Healthcare" --mode quick
```

---

## 📚 Usage Examples

### Example 1: Basic Command Line

```bash
# Quick analysis of a custom policy
python uagent_main.py -p "Carbon Tax Policy" -m quick

# Full analysis with debate
python uagent_main.py -p "Affordable Housing Initiative"

# Research phase only
python uagent_main.py -p "Education Reform" -m research
```

### Example 2: Programmatic API

```python
from uagent_main import AutoPolicyDeliberationSystem

# Initialize system
system = AutoPolicyDeliberationSystem(
    policy_topic="Universal Basic Income",
    city_data="San Francisco",
    policy_type="Economic Welfare",
    time_range="5 years"
)

# Run full deliberation
results = system.run()

# Access results
print(f"Decision: {results['decision']}")
print(f"Consensus: {results['consensus_level']}")
print(f"Report: {results['final_report']}")
```

### Example 3: Using kickoff() Method (CrewAI Compatible)

```python
from uagent_main import AutoPolicyDeliberationSystem

system = AutoPolicyDeliberationSystem(
    policy_topic="Climate Action Plan"
)

# Quick mode via kickoff
results = system.kickoff(inputs={"mode": "quick"})
```

### Example 4: Interactive CLI Session

```bash
$ python uagent_main.py -i

What policy topic would you like to analyze?
> Universal Healthcare System

What city or region is being considered?
> California

What type of policy is this?
> Healthcare

What timeframe for implementation?
> 3-5 years

What are the key interests to evaluate?
> Cost, Accessibility, Quality

Select execution mode:
1. Full Analysis (25-40 min)
2. Quick Analysis (15-25 min)
3. Research Only (10-15 min)
4. Debate Only (8-12 min)
> 2

Starting analysis...
```

### Example 5: Batch Processing

```python
policies = [
    "Carbon Tax",
    "Universal Healthcare",
    "Affordable Housing"
]

results = {}
for policy in policies:
    system = AutoPolicyDeliberationSystem(policy_topic=policy)
    results[policy] = system.kickoff(inputs={"mode": "quick"})
    
    # Save individual reports
    with open(f"{policy.replace(' ', '_')}_report.txt", "w") as f:
        f.write(results[policy]['final_report'])
```

---

## 📂 Project Structure

```
Agentic-ai/
│
├── 📄 uagent_main.py              # Main orchestration system (46.7 KB)
│   ├── AutoPolicyDeliberationSystem class
│   ├── 8-phase workflow implementation
│   ├── Multiple execution modes
│   ├── Interactive CLI
│   ├── Agentverse integration
│   └── Command-line argument parsing
│
├── 📄 ai_agent.py                 # Agent definitions (17.5 KB)
│   ├── DecisionAgent class
│   ├── 26+ expert agent definitions
│   ├── Role/Goal/Backstory for each
│   └── LLM configuration (ASI Cloud)
│
├── 📄 ai_agent_task.py            # Task system (26.5 KB)
│   ├── AgentTaskSystem class
│   ├── Generalized task templates
│   ├── Domain-specific task creators
│   ├── Tool integration
│   └── Workflow generators
│
├── 📁 tools/                      # Tool implementations
│   ├── search_tool.py             # Web search tools (Serper API)
│   │   ├── search_economic_data()
│   │   ├── search_policy_cases()
│   │   ├── search_financial_stats()
│   │   └── search_market_data()
│   │
│   └── Knowledgebase/
│       └── retriever_simple.py    # Knowledge base tools (Pinecone)
│           ├── search_policy_knowledge_base()
│           ├── search_policy_by_category()
│           └── get_knowledge_base_statistics()
│
├── 📄 .env                        # Environment variables (API keys)
├── 📄 .gitignore                  # Git ignore patterns
├── 📄 README.md                   # This file
├── 📄 ARCHITECTURE.md             # Detailed architecture documentation
├── 📄 API_REFERENCE.md            # API reference guide
└── 📄 EXAMPLES.md                 # Comprehensive examples
```

### Core Files Explained

| File | Purpose | Size | Key Components |
|------|---------|------|----------------|
| `uagent_main.py` | Orchestration engine | 46.7 KB | System class, phases, modes, CLI |
| `ai_agent.py` | Agent definitions | 17.5 KB | 26+ expert agents with roles |
| `ai_agent_task.py` | Task management | 26.5 KB | Task templates, tool integration |
| `tools/search_tool.py` | Web search | ~8 KB | 4 Serper API tools |
| `tools/Knowledgebase/retriever_simple.py` | KB search | ~5 KB | 3 Pinecone tools |

---

## ⚙️ Configuration

### Environment Variables

```env
# ========== REQUIRED ==========
ASI_API_KEY=sk-xxx                # ASI Cloud API key for LLM

# ========== OPTIONAL ==========
SERPER_API_KEY=xxx                # Serper API for web search
PINECONE_API_KEY=xxx              # Pinecone for knowledge base
AV_API_KEY=xxx                    # Agentverse for deployment
BROWSERLESS_API_KEY=xxx           # Browserless (if using web scraping)

# ========== ADVANCED ==========
CREWAI_TRACING_ENABLED=true       # Enable CrewAI execution tracing
MAIN_UAGENT_ADDRESS=127.0.0.1:8033  # uAgent network address
```

### Command-Line Arguments

```bash
python uagent_main.py [OPTIONS]

Options:
  -i, --interactive          Launch interactive mode with prompts
  -m, --mode MODE           Execution mode: full, quick, research, debate
  -p, --policy TOPIC        Custom policy topic to analyze
  -r, --register            Register with Agentverse
  --port PORT               Port for Agentverse (default: 8034)
  -h, --help                Show help message
```

### System Parameters

Modify in `AutoPolicyDeliberationSystem.__init__()`:

```python
system = AutoPolicyDeliberationSystem(
    policy_topic="Your Policy",          # Policy to analyze
    background_context="Context here",   # Optional context
    city_data="City name",               # City/region
    policy_type="Type",                  # Policy category
    time_range="Timeframe",              # Implementation period
    interests="Key criteria"             # Evaluation criteria
)
```

---

## 🔍 How It Works

### Workflow Example: Poverty Reduction Policy

#### **Phase 1: Initialization**
```
✓ Economic Analyst
✓ Macro-Economic Expert
✓ Micro-Economic Expert
✓ Policy Impact Expert
✓ Social Welfare Experts (3)
✓ Geospatial Experts (3)
✓ Income Inequality Experts (3)
✓ Resource Allocation Experts (3)
✓ Feedback Experts (2)
✓ Legal Expert
✓ Orchestration Experts (3)

Total: 26 expert agents initialized
```

#### **Phase 2: Problem Statement**
The Problem Statement Expert articulates:
- Core issues (unemployment, housing crisis, income inequality)
- Policy objectives (improve mobility, access, employment)
- Success metrics (poverty rate reduction, income increase)
- Key questions for each expert domain
- Context and constraints

#### **Phase 3: Research** (All 26 experts, parallel)
Each expert uses search tools to gather data:

**Economic Expert:**
```
• Searched: "poverty reduction economic impact GDP"
• Found: World Bank report showing 10% poverty reduction = 1.2-1.8% GDP growth
• Analyzed: ROI of 150-300% for urban job programs
• Position: CONDITIONAL SUPPORT
```

**Social Welfare Expert:**
```
• Searched: "urban poverty healthcare education access"
• Found: Medellín case study (22% productivity increase)
• Analyzed: Impact on vulnerable populations
• Position: SUPPORT
```

*[24 more experts conduct similar research...]*

#### **Phase 4: Debate** (Full mode only)
Experts present structured arguments:

1. **Opening Statement**: Position + Top 3 arguments
2. **Evidence Presentation**: Quantitative data + case studies
3. **Synthesis**: Address counterarguments, propose conditions

#### **Phase 5: Voting**
Democratic voting with rationale:

```
Economic Analyst: CONDITIONAL SUPPORT (+0)
  "Support if programs have clear ROI metrics and sunset clauses"

Macro-Economic Expert: STRONGLY SUPPORT (+2)
  "High NPV and sustainable fiscal returns over 10 years"

Social Welfare Expert: SUPPORT (+1)
  "Improves quality of life but needs housing safeguards"

[23 more votes...]

Final Tally:
  Strongly Support: 8 (35%)
  Support: 12 (52%)
  Conditional: 4 (17%)
  Oppose: 2 (9%)
  
Weighted Score: +18 (out of ±52)
Consensus: STRONG CONSENSUS (87% support)
```

#### **Phase 6: Announcement**
Voting Coordinator announces:
- **Decision**: CONDITIONALLY APPROVED
- **Consensus Level**: Strong (87% support)
- **Key Arguments**: ROI 150-300%, GDP growth 1.2-1.8%, improved human capital
- **Conditions**: Phased implementation, outcome monitoring, anti-gentrification measures
- **Minority Concerns**: Short-term fiscal pressure, market distortions

#### **Phase 7: Report Generation**
Auto-generated comprehensive report:
```
policy_report_20251021_143045.txt (50-100 KB)

Contents:
• Executive Summary
• Problem Statement (from Phase 2)
• 26 Expert Research Analyses (with citations)
• Debate Transcript (if Full mode)
• 26 Voting Records (with rationales)
• Final Decision Announcement
• Vote Tally & Consensus Analysis
• Recommended Implementation Steps
• Risk Mitigation Strategies
```

---

## 📖 API Reference

### Main Class: `AutoPolicyDeliberationSystem`

#### Constructor

```python
AutoPolicyDeliberationSystem(
    policy_topic: str = "Poverty Reduction and Economic Outcome in Urban Areas",
    background_context: str = "[default context]",
    city_data: str = "Urban areas in developing countries",
    policy_type: str = "Social Welfare & Economic Development",
    time_range: str = "Short-term (0-3 years) to Long-term (7-15 years)",
    interests: str = "Economic mobility, social equity, infrastructure"
)
```

#### Methods

##### `run()` → dict
Standard execution method.

```python
system = AutoPolicyDeliberationSystem(policy_topic="Universal Healthcare")
results = system.run()
```

**Returns:**
```python
{
    'decision': 'APPROVED',
    'consensus_level': 'STRONG CONSENSUS',
    'vote_tally': {...},
    'final_report': 'path/to/report.txt',
    'execution_time': 1847.32,
    'expert_votes': [...]
}
```

##### `kickoff(inputs: dict)` → dict
CrewAI-compatible execution method.

```python
results = system.kickoff(inputs={"mode": "quick"})
```

**Inputs:**
- `mode`: "full", "quick", "research", "debate"

##### `run_quick_analysis()` → dict
Streamlined workflow (Research → Vote → Announce).

```python
results = system.run_quick_analysis()
```

##### `run_research_only()` → dict
Data gathering phase only.

```python
results = system.run_research_only()
```

##### `run_debate_only()` → dict
Argumentation and voting phases (requires prior research).

```python
results = system.run_debate_only()
```

##### `update_parameters(new_params: dict)`
Update system parameters dynamically.

```python
system.update_parameters({
    'policy_topic': 'New Topic',
    'city_data': 'New York City'
})
```

##### `interactive_mode()` → dict
Launch interactive CLI.

```python
results = system.interactive_mode()
```

##### `register_with_agentverse(port: int = 8034)`
Register as Agentverse agent.

```python
system.register_with_agentverse(port=8034)
```

---

## 🔧 Tools & Integrations

> **📘 For detailed tool usage flow, see [TOOL_USAGE_FLOW.md](TOOL_USAGE_FLOW.md)**

**When Are Tools Used?**
- ✅ **Phase 4 (Research)**: All 26 experts use tools to gather data
- ✅ **Phase 5 (Debate)**: Tools available for fact-checking
- ❌ **Other Phases**: No tools needed (setup/voting/reporting)

### Web Search Tools (Serper API)

**4 specialized search tools:**

1. **`search_economic_data(query: str)`**
   - Searches for economic statistics, GDP data, fiscal information
   - Returns top 3 results with titles, snippets, sources

2. **`search_policy_cases(policy_type: str)`**
   - Finds real-world case studies of similar policies
   - Returns implementation results and outcomes

3. **`search_financial_stats(topic: str)`**
   - Searches for specific financial statistics and revenue data
   - Filters for numerical data

4. **`search_market_data(market_topic: str)`**
   - Searches for market trends and business impact data
   - Returns industry statistics

**Usage in Tasks:**
```python
# Agents automatically use tools during research phase
task = task_system.create_research_task(
    agent=economic_expert,
    policy_topic="Carbon Tax",
    focus_area="Economic Impact"
)
# Agent will call search tools automatically
```

### Knowledge Base Tools (Pinecone - Optional)

**3 knowledge base tools:**

1. **`search_policy_knowledge_base(query: str)`**
   - Searches internal policy documents
   - Returns top 3 relevant documents with context

2. **`search_policy_by_category(category: str)`**
   - Filters by policy category (taxation, budget, subsidy, etc.)
   - Returns category-specific documents

3. **`get_knowledge_base_statistics()`**
   - Returns KB stats (document count, categories, index info)

**Setup Knowledge Base:**
```python
# Requires Pinecone setup
pip install pinecone-client

# Configure in tools/Knowledgebase/knowledge_base.py
# Add your policy documents to Pinecone index
```

### LLM Integration (ASI Cloud)

**Configuration:**
```python
llm = LLM(
    model="openai/asi1-mini",
    temperature=0.7,
    api_key=os.environ.get("ASI_API_KEY"),
    base_url="https://inference.asicloud.cudos.org/v1"
)
```

**Features:**
- OpenAI-compatible API
- Supports chat completions
- Function calling for tools
- Streaming responses (optional)

### Agentverse Integration

**Deploy as distributed agent:**
```bash
python uagent_main.py --register --port 8034
```

**Features:**
- Mailbox communication
- Query parameter schema
- Async message handling
- Network discovery

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Areas for Contribution

1. **New Expert Agents**: Add domain-specific experts
2. **Tool Integrations**: Connect new data sources
3. **Execution Modes**: Create specialized workflows
4. **Output Formats**: Add PDF, HTML, JSON exports
5. **Visualization**: Create vote visualizations, timelines
6. **Documentation**: Improve guides and examples

### Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/Agentic-ai.git
cd Agentic-ai

# Create feature branch
git checkout -b feature/your-feature-name

# Install dev dependencies
pip install -r requirements-dev.txt

# Make changes and test
python uagent_main.py --mode quick

# Commit and push
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Write clear commit messages

---

## 🐛 Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: No module named 'ai_agent'

**Cause:** File was named `ai-agent.py` (hyphen) instead of `ai_agent.py` (underscore).

**Solution:**
```bash
# Rename file
mv ai-agent.py ai_agent.py
```

#### 2. API Key Errors

**Symptoms:**
```
Error: API key not found
```

**Solution:**
```bash
# Check .env file exists and has correct format
cat .env

# Verify API key is loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('ASI Key:', os.getenv('ASI_API_KEY')[:10])"
```

#### 3. Tool Validation Error

**Symptoms:**
```
pydantic_core._pydantic_core.ValidationError: validation errors for Task
```

**Solution:** Tools are already disabled/fixed in latest version. If you see this, ensure you're using the latest `ai_agent_task.py`.

#### 4. Slow Execution

**Cause:** Full mode with web searches is comprehensive.

**Solution:**
```bash
# Use quick mode
python uagent_main.py --mode quick

# Or research only
python uagent_main.py --mode research
```

#### 5. Pinecone Warning

**Symptoms:**
```
Warning: Could not import EconomicKnowledgeBase: No module named 'pinecone'
```

**Solution:** This is non-critical. Install if you want knowledge base:
```bash
pip install pinecone-client
```

### Getting Help

1. **Check documentation**: See `ARCHITECTURE.md` and `API_REFERENCE.md`
2. **Run with verbose**: Enable detailed logging
3. **Check logs**: Review terminal output for errors
4. **Open issue**: [GitHub Issues](https://github.com/yourusername/Agentic-ai/issues)

---

## 📊 Performance & Benchmarks

### Execution Times

| Mode | Agents | Phases | Duration | Tools Used |
|------|--------|--------|----------|------------|
| Full | 26 | 8 | 25-40 min | Yes |
| Quick | 26 | 6 | 15-25 min | Yes |
| Research | 26 | 4 | 10-15 min | Yes |
| Debate | 26 | 4 | 8-12 min | No |

### Token Usage (Approximate)

- **Research Phase**: ~1,500 tokens/expert = 39,000 tokens
- **Debate Phase**: ~1,200 tokens/expert = 31,200 tokens
- **Voting Phase**: ~500 tokens/expert = 13,000 tokens
- **Total (Full)**: ~85,000-100,000 tokens per analysis

### Cost Estimates (ASI Cloud)

- Quick Mode: ~$0.10-$0.20 per analysis
- Full Mode: ~$0.30-$0.50 per analysis

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent orchestration framework
- **ASI Cloud**: LLM inference API
- **Serper**: Web search API
- **Pinecone**: Vector database for knowledge base
- **Agentverse**: Distributed agent network

---

## 📞 Contact & Support

- **GitHub**: [Your GitHub Profile](https://github.com/yourusername)
- **Email**: your.email@example.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/Agentic-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Agentic-ai/discussions)

---

## 🗺️ Roadmap

### Current Version: 2.0
- [x] 26+ expert agents
- [x] Multiple execution modes
- [x] Web search integration
- [x] Interactive CLI
- [x] Agentverse deployment

### Version 2.1 (Planned)
- [ ] PDF report generation
- [ ] Vote visualization dashboard
- [ ] Real-time streaming output
- [ ] Multi-language support

### Version 3.0 (Future)
- [ ] Custom agent builder UI
- [ ] Policy comparison mode
- [ ] Historical analysis tracking
- [ ] API server mode
- [ ] Docker containerization

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! It helps others discover the project.

---

**Built with ❤️ using CrewAI and ASI Cloud**

*Last Updated: October 21, 2025*
