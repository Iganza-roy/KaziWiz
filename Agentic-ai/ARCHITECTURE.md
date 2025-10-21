# 🏗️ System Architecture

## Overview

The Multi-Expert AI Policy Deliberation System is built on a **layered architecture** that separates concerns and enables scalability, flexibility, and maintainability.

---

## Architecture Layers

### 1. User Interface Layer

**Purpose**: Multiple entry points for system interaction

**Components:**
- **CLI (Command Line Interface)**
  - Interactive mode with prompts
  - Direct command execution
  - Argument parsing via `argparse`
  
- **Programmatic API**
  - Python class instantiation
  - Method calls (`run()`, `kickoff()`)
  - Result dictionary returns
  
- **Agentverse Integration**
  - Distributed agent registration
  - Mailbox communication
  - Query parameter handling

**Implementation**: `uagent_main.py` → `main()` function

---

### 2. Orchestration Layer

**Purpose**: Manages workflow execution and phase coordination

**Key Class**: `AutoPolicyDeliberationSystem`

**Responsibilities:**
- Agent initialization (26+ experts)
- Phase sequencing (8 phases)
- Mode selection (full/quick/research/debate)
- Result aggregation
- Report generation
- Error handling

**Key Methods:**
```python
__init__()                    # Initialize system
run()                         # Standard execution
kickoff(inputs)              # CrewAI-compatible execution
run_quick_analysis()         # Quick mode
run_research_only()          # Research mode
run_debate_only()            # Debate mode
interactive_mode()           # CLI prompts
register_with_agentverse()   # Deployment
```

**Implementation**: `uagent_main.py` → `AutoPolicyDeliberationSystem` class

---

### 3. Agent Layer

**Purpose**: Defines expert agents with specialized roles

**Key Class**: `DecisionAgent`

**Agent Categories:**

1. **Orchestration Experts (3)**
   - Problem Statement Clarification
   - Turn Management
   - Voting Coordinator

2. **Economic Experts (4)**
   - Macro-Economic Analysis
   - Micro-Economic Analysis
   - Policy Impact Analysis
   - Trade & Investment

3. **Social Welfare Experts (3)**
   - Healthcare Accessibility
   - Education & Skills
   - Housing & Safety Nets

4. **Geospatial & Demographic Experts (3)**
   - Geographic Poverty Analysis
   - Demographic Policy
   - Resource Access & Unemployment

5. **Income Inequality Experts (3)**
   - Inequality Causes
   - Income Redistribution
   - Impact Assessment

6. **Resource Allocation Experts (3)**
   - Resource Optimization
   - Real-Time Prioritization
   - System Efficiency

7. **Feedback & Adaptation Experts (2)**
   - Policy Monitoring
   - Adaptive Policy

8. **Core Experts (6)**
   - Economic Analyst
   - Social Dynamics
   - Geospatial Analyst
   - Income Distribution
   - Resource Management
   - Legal Adviser

**Agent Structure:**
```python
Agent(
    role="Expert Title",
    goal="What the expert aims to achieve",
    backstory="Experience and specialization",
    verbose=True,
    llm=LLM_instance
)
```

**Implementation**: `ai_agent.py` → `DecisionAgent` class

---

### 4. Task Layer

**Purpose**: Creates and manages tasks for agents

**Key Class**: `AgentTaskSystem`

**Task Types:**

1. **Generalized Templates**
   - `create_research_task()` - Data gathering with tools
   - `create_debate_task()` - Structured argumentation
   - `create_voting_task()` - Democratic decision-making

2. **Domain-Specific Tasks**
   - `create_economic_analysis_task()`
   - `create_social_welfare_task()`
   - `create_geospatial_demographic_task()`
   - `create_income_inequality_task()`
   - `create_resource_allocation_task()`
   - `create_adaptation_feedback_task()`
   - `create_legal_compliance_task()`

3. **Specialized Tasks**
   - `create_problem_statement_task()`
   - `create_turn_management_task()`
   - `create_voting_coordination_task()`

4. **Workflow Generators**
   - `create_full_deliberation_workflow()`
   - `create_quick_analysis_workflow()`

**Task Structure:**
```python
Task(
    description="Detailed task instructions",
    agent=agent_instance,
    expected_output="What should be produced",
    tools=[tool1, tool2, ...]  # Optional
)
```

**Implementation**: `ai_agent_task.py` → `AgentTaskSystem` class

---

### 5. Tool Layer

**Purpose**: Provides external data access **DURING RESEARCH PHASE**

**When Tools Are Used:**
- ✅ **Research Phase (Phase 4)**: All 26 experts use tools to gather real-time data
- ✅ **Debate Phase (Phase 5)**: Optional, for fact-checking (tools enabled)
- ❌ **Voting Phase (Phase 6)**: No tools needed (uses debate summary)
- ❌ **Other Phases**: No tools needed

**How Tools Are Accessed:**
```python
# In ai_agent_task.py
def create_research_task(agent, policy_topic, focus_area):
    return Task(
        description="Research and analyze...",
        agent=agent,
        tools=self.search_tools  # ← Tools passed here!
    )
```

**Categories:**

#### A. Web Search Tools (Serper API)

**File**: `tools/search_tool.py`

**Tools:**
1. `search_economic_data(query)` - Economic statistics
2. `search_policy_cases(policy_type)` - Case studies
3. `search_financial_stats(topic)` - Financial data
4. `search_market_data(market_topic)` - Market trends

**Usage Example:**
```python
# Agent internally calls during research:
result = search_economic_data("poverty reduction GDP impact")
# Returns: "• World Bank: Poverty fell 30%... Source: worldbank.org"
```

**Implementation:**
```python
@tool("Search economic data")
def search_economic_data(query: str) -> str:
    # Serper API call
    # Returns formatted search results with citations
```

#### B. Knowledge Base Tools (Pinecone)

**File**: `tools/Knowledgebase/retriever_simple.py`

**Tools:**
1. `search_policy_knowledge_base(query)` - Vector search
2. `search_policy_by_category(category)` - Category filter
3. `get_knowledge_base_statistics()` - KB metadata

**Usage Example:**
```python
# Agent internally calls during research:
result = search_policy_knowledge_base("healthcare reform precedents")
# Returns: Previous policy documents and analysis
```

**Implementation:**
```python
@tool("search_policy_knowledge_base")
def search_policy_knowledge_base(query: str) -> str:
    # Pinecone vector search
    # Returns relevant documents from internal KB
```

---

### 6. LLM Layer

**Purpose**: Provides language model capabilities

**Provider**: ASI Cloud (OpenAI-compatible API)

**Configuration:**
```python
LLM(
    model="openai/asi1-mini",
    temperature=0.7,
    api_key=os.environ.get("ASI_API_KEY"),
    base_url="https://inference.asicloud.cudos.org/v1"
)
```

**Features:**
- Chat completions
- Function calling (for tools)
- Streaming (optional)
- Error handling with retries

**Token Management:**
- Average per agent: 1,500-2,000 tokens
- Full workflow: 85,000-100,000 tokens
- Batching for efficiency

---

## Data Flow

### Typical Execution Flow (Full Mode)

```
1. USER INPUT
   └─► CLI/API/Agentverse
   
2. INITIALIZATION
   └─► AutoPolicyDeliberationSystem.__init__()
       └─► DecisionAgent() creates 26+ agents
           └─► Each agent gets LLM instance
   
3. TASK CREATION
   └─► AgentTaskSystem.create_full_deliberation_workflow()
       └─► Generates tasks for all phases
           └─► Tasks include tool access
   
4. PHASE 1: PROBLEM STATEMENT
   └─► Problem Statement Expert
       └─► Task execution (no tools)
           └─► LLM generates problem definition
               └─► Output: Structured problem statement
   
5. PHASE 2: TURN MANAGEMENT
   └─► Turn Management Expert
       └─► Task execution (no tools)
           └─► LLM creates discussion rules
               └─► Output: Orchestration plan
   
6. PHASE 3: RESEARCH (26 experts, parallel)
   └─► Each expert executes research task
       └─► Agent decides to use tools
           └─► Tool calls (web search)
               └─► Serper API returns data
                   └─► Agent analyzes results
                       └─► LLM generates position
                           └─► Output: Research analysis
   
7. PHASE 4: DEBATE
   └─► Each expert presents arguments
       └─► LLM generates structured debate
           └─► Output: Opening, Evidence, Synthesis
   
8. PHASE 5: VOTING
   └─► Each expert casts vote
       └─► LLM generates vote + rationale
           └─► Output: Vote with reasoning
   
9. PHASE 6: ANNOUNCEMENT
   └─► Voting Coordinator tallies votes
       └─► LLM generates decision announcement
           └─► Output: Final decision + consensus
   
10. PHASE 7: REPORT
    └─► System aggregates all outputs
        └─► Format as text document
            └─► Save to file
                └─► Output: policy_report_*.txt
   
11. RETURN RESULTS
    └─► Dictionary with all outputs
        └─► User receives results
```

---

## Component Interaction

### CrewAI Integration

**Crew Creation:**
```python
crew = Crew(
    agents=[agent1, agent2, ...],
    tasks=[task1, task2, ...],
    process=Process.sequential,  # or parallel
    verbose=True
)

result = crew.kickoff()
```

**Our Implementation:**
- Each phase creates a Crew
- Tasks assigned to specific agents
- Sequential execution within Crew
- Results captured and aggregated

### Tool Execution Flow

```
Agent Task Execution
    │
    ├─► Agent analyzes task
    │   └─► Decides tool is needed
    │       └─► Calls tool via function calling
    │
    ├─► Tool executes
    │   └─► search_economic_data("poverty reduction")
    │       └─► HTTP request to Serper API
    │           └─► Parse JSON response
    │               └─► Format results
    │
    └─► Agent receives tool output
        └─► Incorporates into analysis
            └─► Generates final answer
```

---

## Scalability Considerations

### Horizontal Scaling

**Current**: Single-process execution
**Future**: Multi-process/distributed

**Approaches:**
1. **Process Pool**: Parallel phase execution
2. **Celery**: Distributed task queue
3. **Ray**: Distributed computing framework
4. **Agentverse**: Distributed agent network

### Vertical Scaling

**Current**: Sequential task execution
**Future**: Batch processing

**Optimizations:**
1. **LLM Batching**: Combine API calls
2. **Caching**: Store repeated searches
3. **Async I/O**: Non-blocking tool calls
4. **GPU Acceleration**: Local LLM inference

---

## Security Architecture

### API Key Management

- **Storage**: `.env` file (gitignored)
- **Loading**: `python-dotenv`
- **Access**: `os.environ.get()`
- **Rotation**: Environment variable updates

### Input Validation

- **User Input**: Sanitize policy topics
- **Tool Outputs**: Validate JSON structure
- **LLM Outputs**: Parse safely with error handling

### Rate Limiting

- **Serper API**: 2,500 queries/month (free tier)
- **ASI Cloud**: Per-token pricing
- **Pinecone**: Request limits per plan

---

## Error Handling Strategy

### Layered Error Handling

**Level 1: Tool Layer**
```python
try:
    response = requests.post(url, ...)
except requests.exceptions.RequestException as e:
    return f"Network error: {str(e)}"
```

**Level 2: Task Layer**
```python
try:
    task_result = agent.execute_task(...)
except Exception as e:
    print(f"Task execution error: {e}")
    # Graceful degradation
```

**Level 3: Orchestration Layer**
```python
try:
    results = self.run_research_phase(...)
except Exception as e:
    print(f"Phase execution error: {e}")
    # Continue to next phase or abort
```

### Graceful Degradation

1. **Tools Unavailable**: Use LLM knowledge only
2. **API Failure**: Retry with exponential backoff
3. **Agent Failure**: Skip and continue with other agents
4. **LLM Timeout**: Use cached/default response

---

## Configuration Management

### Environment-Based Configuration

**Development:**
```env
DEBUG=true
VERBOSE=true
LOG_LEVEL=DEBUG
```

**Production:**
```env
DEBUG=false
VERBOSE=false
LOG_LEVEL=INFO
```

### Runtime Configuration

**Programmatic:**
```python
system = AutoPolicyDeliberationSystem(
    policy_topic="Custom Topic",
    city_data="Custom City"
)
```

**CLI:**
```bash
python uagent_main.py -p "Custom Topic" -m quick
```

---

## Monitoring & Observability

### Execution Tracing (CrewAI)

**Enable:**
```env
CREWAI_TRACING_ENABLED=true
```

**Features:**
- Agent decision logs
- Task execution timeline
- Tool usage metrics
- LLM call tracking

### Custom Logging

**Implementation:**
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Phase {phase_num} complete")
logger.error(f"Error in {agent.role}: {error}")
```

---

## Extension Points

### Adding New Agents

**Steps:**
1. Add method in `DecisionAgent` class
2. Define role/goal/backstory
3. Create task in `AgentTaskSystem`
4. Add to workflow in `uagent_main.py`

**Example:**
```python
# In ai_agent.py
def climate_expert(self):
    return Agent(
        role="Climate Change Expert",
        goal="Analyze environmental impacts",
        backstory="Climate scientist with policy experience",
        verbose=True,
        llm=self.llm
    )

# In ai_agent_task.py
def create_climate_task(self, agent, policy_topic):
    return self.create_research_task(
        agent, policy_topic,
        focus_area="Climate impact and sustainability"
    )
```

### Adding New Tools

**Steps:**
1. Create tool function with `@tool` decorator
2. Add to `AgentTaskSystem.search_tools`
3. Include in relevant tasks

**Example:**
```python
# In tools/custom_tool.py
from langchain.tools import tool

@tool("Custom data source")
def search_custom_source(query: str) -> str:
    """Search custom data source"""
    # Implementation
    return results

# In ai_agent_task.py
self.custom_tools = [search_custom_source]
self.all_tools = self.search_tools + self.custom_tools
```

### Adding New Execution Modes

**Steps:**
1. Create mode method in `AutoPolicyDeliberationSystem`
2. Add mode to CLI arguments
3. Update kickoff() dispatcher

**Example:**
```python
def run_validation_mode(self):
    """Research + validation only, no voting"""
    self.run_problem_statement_phase(...)
    results = self.run_research_phase(...)
    validation = self.run_validation_phase(results)
    return {'validation': validation}
```

---

## Performance Optimization

### Current Optimizations

1. **Sequential Crew Execution**: Predictable resource usage
2. **Tool Filtering**: Only relevant tools per task
3. **Output Truncation**: Prevent context overflow
4. **Conditional Tool Use**: Agent decides when to use tools

### Future Optimizations

1. **Parallel Phase Execution**: Use multiprocessing
2. **LLM Response Caching**: Cache similar queries
3. **Tool Result Caching**: Store search results
4. **Batch API Calls**: Combine multiple LLM requests
5. **Streaming Responses**: Show results progressively

---

## Testing Strategy

### Unit Tests (Future)

```python
# Test agent creation
def test_agent_creation():
    agent_system = DecisionAgent()
    agent = agent_system.Econimic_agent()
    assert agent.role == "Economic Analyst"

# Test task creation
def test_task_creation():
    task_system = AgentTaskSystem()
    task = task_system.create_research_task(agent, "Policy", "Focus")
    assert task.tools == task_system.search_tools
```

### Integration Tests (Future)

```python
# Test full workflow
def test_quick_analysis():
    system = AutoPolicyDeliberationSystem(policy_topic="Test Policy")
    results = system.run_quick_analysis()
    assert 'decision' in results
    assert 'final_report' in results
```

---

## Deployment Architecture

### Local Deployment

**Current**: Single machine, Python script

**Requirements:**
- Python 3.8+
- API keys in `.env`
- Dependencies installed

**Command:**
```bash
python uagent_main.py
```

### Server Deployment (Future)

**Option 1: Flask/FastAPI Server**
```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/analyze")
async def analyze(policy: str, mode: str):
    system = AutoPolicyDeliberationSystem(policy_topic=policy)
    results = system.kickoff(inputs={"mode": mode})
    return results
```

**Option 2: Docker Container**
```dockerfile
FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "uagent_main.py"]
```

### Agentverse Deployment

**Current**: Supported via `--register` flag

**Features:**
- Network discovery
- Mailbox communication
- Distributed execution
- Query handling

**Command:**
```bash
python uagent_main.py --register --port 8034
```

---

**Architecture Version**: 2.0  
**Last Updated**: October 21, 2025
