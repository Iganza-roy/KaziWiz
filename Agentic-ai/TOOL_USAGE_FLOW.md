# 🔧 Tool Usage Flow - Detailed Explanation

This document explains **exactly when and how tools are used** in the Multi-Expert AI Policy Deliberation System.

---

## 🎯 Quick Answer

**Tools are used primarily in Phase 4 (RESEARCH)** where all 26 experts gather real-time data from web search and knowledge base.

```
❌ Phase 1-3: No tools (initialization, problem framing)
✅ Phase 4: TOOLS ACTIVELY USED (research & data gathering)
✅ Phase 5: Tools available (optional fact-checking during debate)
❌ Phase 6-8: No tools (voting, tallying, reporting)
```

---

## 📊 Detailed Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     USER STARTS ANALYSIS                            │
│                  policy_topic = "Universal Healthcare"              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   PHASE 1-3: INITIALIZATION                         │
│                                                                     │
│  • Create 26+ expert agents (ai_agent.py)                          │
│  • Generate problem statement                                       │
│  • Setup turn management                                            │
│                                                                     │
│  🔧 TOOLS: None needed (setup phase)                               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│         PHASE 4: RESEARCH ⭐ PRIMARY TOOL USAGE PHASE ⭐            │
│                                                                     │
│  Step 1: Task System Initializes Tools                             │
│  ┌──────────────────────────────────────────────┐                  │
│  │  AgentTaskSystem.__init__()                  │                  │
│  │  ├─► Load 4 web search tools (Serper API)   │                  │
│  │  ├─► Load 3 knowledge base tools (Pinecone)  │                  │
│  │  └─► self.search_tools = [4 tools]          │                  │
│  └──────────────────────────────────────────────┘                  │
│                                                                     │
│  Step 2: Research Tasks Created WITH Tools                         │
│  ┌──────────────────────────────────────────────┐                  │
│  │  create_research_task(agent, topic, focus)   │                  │
│  │  └─► Task(                                    │                  │
│  │      description="Research and analyze...",   │                  │
│  │      agent=economic_expert,                   │                  │
│  │      tools=self.search_tools  ← TOOLS HERE!  │                  │
│  │  )                                            │                  │
│  └──────────────────────────────────────────────┘                  │
│                                                                     │
│  Step 3: Each of 26 Experts Executes Research                      │
│  ┌──────────────────────────────────────────────┐                  │
│  │  Economic Expert #1                          │                  │
│  │  ├─► Analyzes task: "research healthcare"    │                  │
│  │  ├─► LLM decides to use search_economic_data │                  │
│  │  ├─► Calls: search_economic_data(            │                  │
│  │  │      "healthcare spending GDP"            │                  │
│  │  │   )                                        │                  │
│  │  ├─► Receives: "OECD: US healthcare 18%..."  │                  │
│  │  ├─► LLM incorporates data into analysis     │                  │
│  │  └─► Output: Position with citations         │                  │
│  └──────────────────────────────────────────────┘                  │
│                                                                     │
│  ┌──────────────────────────────────────────────┐                  │
│  │  Social Welfare Expert #2                    │                  │
│  │  ├─► Calls: search_policy_cases(             │                  │
│  │  │      "universal healthcare"               │                  │
│  │  │   )                                        │                  │
│  │  ├─► Receives: "UK NHS case study..."        │                  │
│  │  ├─► Calls: search_policy_knowledge_base(    │                  │
│  │  │      "healthcare reform"                  │                  │
│  │  │   )                                        │                  │
│  │  ├─► Receives: Internal policy docs          │                  │
│  │  └─► Output: Position with evidence          │                  │
│  └──────────────────────────────────────────────┘                  │
│                                                                     │
│  ... [24 more experts, all with tool access]                       │
│                                                                     │
│  🔧 TOOLS ACTIVELY USED:                                           │
│  • search_economic_data        → ~26 calls across all experts      │
│  • search_policy_cases         → ~20 calls                         │
│  • search_financial_stats      → ~15 calls                         │
│  • search_market_data          → ~10 calls                         │
│  • search_policy_knowledge_base → ~12 calls (if Pinecone)          │
│                                                                     │
│  📊 OUTPUT: 26 research analyses with cited sources                │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│            PHASE 5: DEBATE (Full mode only)                         │
│                                                                     │
│  Step 1: Debate Tasks Created WITH Tools (Optional)                │
│  ┌──────────────────────────────────────────────┐                  │
│  │  create_debate_task(agent, topic, context)   │                  │
│  │  └─► Task(                                    │                  │
│  │      description="Present arguments...",      │                  │
│  │      agent=economic_expert,                   │                  │
│  │      tools=self.search_tools  ← Available!   │                  │
│  │  )                                            │                  │
│  └──────────────────────────────────────────────┘                  │
│                                                                     │
│  Step 2: Experts Debate Using Research Results                     │
│  ┌──────────────────────────────────────────────┐                  │
│  │  Economic Expert                             │                  │
│  │  ├─► Uses Phase 4 research results           │                  │
│  │  ├─► May call tools for fact-checking        │                  │
│  │  │   (optional, less common)                 │                  │
│  │  └─► Output: Structured debate argument      │                  │
│  └──────────────────────────────────────────────┘                  │
│                                                                     │
│  🔧 TOOLS: Available but primarily uses cached research            │
│  📊 OUTPUT: 26 debate contributions                                │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  PHASE 6: VOTING                                    │
│                                                                     │
│  Step 1: Voting Tasks Created WITHOUT Tools                        │
│  ┌──────────────────────────────────────────────┐                  │
│  │  create_voting_task(agent, topic, arguments) │                  │
│  │  └─► Task(                                    │                  │
│  │      description="Cast your vote...",         │                  │
│  │      agent=economic_expert,                   │                  │
│  │      tools=[]  ← NO TOOLS                    │                  │
│  │  )                                            │                  │
│  └──────────────────────────────────────────────┘                  │
│                                                                     │
│  Step 2: Each Expert Votes Based on All Evidence                   │
│  ┌──────────────────────────────────────────────┐                  │
│  │  Economic Expert                             │                  │
│  │  ├─► Reviews research from Phase 4           │                  │
│  │  ├─► Reviews debate from Phase 5             │                  │
│  │  ├─► Makes final decision                    │                  │
│  │  └─► Output: Vote + Rationale                │                  │
│  └──────────────────────────────────────────────┘                  │
│                                                                     │
│  🔧 TOOLS: None (decision based on prior evidence)                 │
│  📊 OUTPUT: 26 votes with rationale                                │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│               PHASE 7-8: ANNOUNCEMENT & REPORTING                   │
│                                                                     │
│  • Tally votes                                                      │
│  • Calculate consensus level                                        │
│  • Generate final decision                                          │
│  • Create comprehensive report                                      │
│                                                                     │
│  🔧 TOOLS: None (aggregation and formatting)                       │
│  📊 OUTPUT: Final report with decision                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Code Deep-Dive: How Tools Flow

### 1. Tool Initialization (ai_agent_task.py)

```python
class AgentTaskSystem:
    def __init__(self):
        # Load web search tools
        self.search_tools = [
            EconomicSearchTools.search_economic_data,      # Tool 1
            EconomicSearchTools.search_policy_cases,       # Tool 2
            EconomicSearchTools.search_financial_stats,    # Tool 3
            EconomicSearchTools.search_market_data,        # Tool 4
        ]
        print(f"✅ Loaded {len(self.search_tools)} web search tools")
        
        # Load knowledge base tools (optional)
        self.kb_tools = get_knowledge_base_tools()  # 3 more tools
        
        # Combine
        self.all_tools = self.search_tools + self.kb_tools
```

**Output when system starts:**
```
✅ Loaded 4 web search tools
✅ Loaded 3 knowledge base tools
🔧 Total tools available: 7
```

---

### 2. Research Task Creation WITH Tools

```python
def create_research_task(self, agent, policy_topic, focus_area):
    """Creates research task with tool access"""
    return Task(
        description=f"""Research and analyze: {policy_topic}
        
        STEP 1 - MANDATORY RESEARCH (USE ALL AVAILABLE TOOLS):
        - Search the internal knowledge base for relevant policies
        - Search for economic data and current statistics
        - Search for policy case studies and international examples
        - Search for financial statistics and impact data
        
        STEP 2 - ANALYZE FROM YOUR EXPERTISE PERSPECTIVE:
        Based on your research, analyze...
        
        STEP 3 - FORMULATE YOUR POSITION:
        State your stance with evidence and citations.
        """,
        agent=agent,
        expected_output="Analysis with cited sources",
        tools=self.search_tools  # ← TOOLS PASSED HERE!
    )
```

---

### 3. Domain-Specific Tasks Use Generic Research Template

```python
# All these ultimately call create_research_task()
def create_economic_analysis_task(self, agent, policy_topic):
    return self.create_research_task(
        agent, 
        policy_topic, 
        focus_area="economic impact"  # Specialization
    )

def create_social_welfare_task(self, agent, policy_topic):
    return self.create_research_task(
        agent, 
        policy_topic, 
        focus_area="social welfare implications"
    )

# ... 8 more domain-specific task creators
```

**Key Point:** All domain experts get tools through `create_research_task()`.

---

### 4. Orchestration Calls Task Creators (uagent_main.py)

```python
def run_research_phase(self, agents, policy_topic):
    """Execute research with all 26 experts"""
    
    # Map agents to task creators
    task_creators = {
        'economic': self.task_system.create_economic_analysis_task,
        'social': self.task_system.create_social_welfare_task,
        'geospatial': self.task_system.create_geospatial_demographic_task,
        # ... 23 more mappings
    }
    
    # Create tasks for each agent
    research_tasks = []
    for role, agent in agents.items():
        creator = task_creators.get(role)
        if creator:
            task = creator(agent, policy_topic)  # ← Tools included!
            research_tasks.append(task)
    
    # Execute all tasks in parallel
    crew = Crew(
        agents=list(agents.values()),
        tasks=research_tasks,
        verbose=True
    )
    
    results = crew.kickoff()
    return results
```

---

### 5. Agent Execution with Tools (CrewAI internals)

When CrewAI executes a task:

```python
# Simplified CrewAI flow
def execute_task(task, agent):
    # 1. Agent receives task description
    prompt = task.description
    
    # 2. Agent receives available tools
    available_tools = task.tools  # [search_economic_data, ...]
    
    # 3. LLM decides whether to use tools
    llm_response = agent.llm.generate(prompt, tools=available_tools)
    
    # 4. If LLM wants to use a tool:
    if llm_response.tool_calls:
        for tool_call in llm_response.tool_calls:
            # Execute the tool
            tool_result = tool_call.function.invoke(tool_call.arguments)
            
            # Give result back to LLM
            llm_response = agent.llm.generate(
                prompt + f"\nTool result: {tool_result}",
                tools=available_tools
            )
    
    # 5. Return final answer
    return llm_response.content
```

---

### 6. Example: Economic Expert Using Tools

**Task Description Received:**
```
Research and analyze: Universal Healthcare

YOUR FOCUS AREA: economic impact

STEP 1 - MANDATORY RESEARCH (USE ALL AVAILABLE TOOLS):
- Search for economic data and current statistics related to this topic
- Search for policy case studies and international examples
...
```

**LLM Decision Process:**
```
1. LLM thinks: "I need data on healthcare spending"
2. LLM calls: search_economic_data("healthcare spending GDP by country")
3. Tool returns: "OECD: US healthcare 18% of GDP, UK 10%, Canada 11%..."
4. LLM thinks: "I need case studies"
5. LLM calls: search_policy_cases("universal healthcare systems")
6. Tool returns: "UK NHS established 1948, covers 67M people..."
7. LLM synthesizes: "Based on data showing US spends 18% GDP vs UK 10%..."
```

**Final Output:**
```
ECONOMIC ANALYSIS: Universal Healthcare

POSITION: CONDITIONAL SUPPORT

KEY FINDINGS:
1. Current US healthcare spending: 18% of GDP ($4 trillion/year)
   Source: OECD Health Statistics 2024

2. International comparisons show universal systems achieve lower costs:
   - UK: 10% of GDP, universal coverage
   - Canada: 11% of GDP, universal coverage
   Source: World Bank Health Expenditure Database

3. Case study: Taiwan's single-payer system (1995) reduced admin costs by 40%
   Source: Journal of Health Economics, 2023

POSITION RATIONALE:
Support implementation with conditions:
- Phased rollout over 7-10 years
- Cost controls through negotiated drug pricing
- Investment in primary care infrastructure

CONFIDENCE: HIGH (based on 12 cited sources)
```

---

## 🎯 Why This Design?

### Research Phase Needs Tools Because:

1. ✅ **Fresh Data**: Real-time statistics, recent case studies
2. ✅ **Evidence-Based**: Citations make arguments credible
3. ✅ **Diverse Perspectives**: Each expert finds domain-specific data
4. ✅ **Quality**: Better than pure LLM knowledge (which can be outdated)

### Debate Phase Uses Research Because:

1. ✅ **Already Gathered**: Tools provided ~70 data points in research
2. ✅ **Efficiency**: No need to re-search same information
3. ✅ **Consistency**: Arguments based on same evidence pool
4. ⚠️ **Optional Tools**: Available for fact-checking if needed

### Voting Phase Doesn't Need Tools Because:

1. ✅ **Decision Time**: All evidence already presented
2. ✅ **Synthesis Phase**: Weighing existing arguments
3. ✅ **No New Information**: Voting based on debate summary
4. ✅ **Faster**: No API calls needed

---

## 📊 Tool Usage Statistics

### Typical Full Analysis:

| Phase | Duration | Tool Calls | API Costs |
|-------|----------|------------|-----------|
| Research | 15-20 min | ~70-100 calls | $0.50-0.70 |
| Debate | 8-12 min | ~5-10 calls (optional) | $0.05-0.10 |
| Voting | 3-5 min | 0 calls | $0.00 |
| **Total** | **30-40 min** | **~75-110 calls** | **$0.55-0.80** |

### Tool Call Breakdown:

```
search_economic_data:        26 calls (1 per expert)
search_policy_cases:         20 calls (economic + social)
search_financial_stats:      15 calls (economic specialists)
search_market_data:          10 calls (trade + investment)
search_policy_knowledge_base: 12 calls (all with KB access)
search_policy_by_category:    8 calls (targeted searches)
get_knowledge_base_statistics: 3 calls (context checks)
─────────────────────────────────────────────────────
TOTAL:                       ~94 calls per analysis
```

---

## 💡 Optimization Tips

### Reduce Tool Calls:

```python
# Quick mode: Skip debate phase
system.run_quick_analysis()  # ~70 tool calls instead of ~94

# Research only: Skip debate and voting
system.run_research_only()   # ~70 tool calls, faster
```

### Increase Tool Usage:

```python
# Enable tools in debate phase for fact-checking
def create_debate_task(self, agent, policy_topic, position_context=""):
    return Task(
        description="...",
        agent=agent,
        tools=self.search_tools  # ← Already enabled!
    )
```

---

## 🔧 Troubleshooting Tool Issues

### Check if Tools Loaded:

```python
from ai_agent_task import AgentTaskSystem

ts = AgentTaskSystem()
print(f"Search tools: {len(ts.search_tools)}")  # Should be 4
print(f"KB tools: {len(ts.kb_tools)}")          # Should be 3 (or 0)
print(f"Total: {len(ts.all_tools)}")            # Should be 7 (or 4)
```

**Expected Output:**
```
✅ Loaded 4 web search tools
✅ Loaded 3 knowledge base tools
🔧 Total tools available: 7
Search tools: 4
KB tools: 3
Total: 7
```

### Test Individual Tool:

```python
from tools.search_tool import EconomicSearchTools

result = EconomicSearchTools.search_economic_data.invoke(
    "poverty reduction statistics"
)

print(result[:200])  # Should show search results
```

### Verify Task Has Tools:

```python
from ai_agent import DecisionAgent
from ai_agent_task import AgentTaskSystem

agent_system = DecisionAgent()
task_system = AgentTaskSystem()

agent = agent_system.Econimic_agent()
task = task_system.create_research_task(
    agent, 
    "Test Policy", 
    "economic impact"
)

print(f"Task has {len(task.tools)} tools")  # Should be 4
```

---

## 📚 Related Documentation

- **Architecture**: See `ARCHITECTURE.md` for system design
- **API Reference**: See `API_REFERENCE.md` for all methods
- **Examples**: See `EXAMPLES.md` for usage patterns
- **Main README**: See `README.md` for overview

---

**Last Updated**: October 21, 2025  
**Version**: 2.0
