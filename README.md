# Multi-Expert AI Policy Deliberation — Monorepo Overview

This repository contains a multi-agent policy deliberation system with three main components:

- Orchestration & agents (Agentic-ai)
- Backend API & services (backend)
- Frontend UI (frontend)

Core pieces and where to find them:

- Orchestration / CLI / workflow: [`AutoPolicyDeliberationSystem`](Agentic-ai/uagent_main.py) in [Agentic-ai/uagent_main.py](Agentic-ai/uagent_main.py)
- Agent definitions (26+ experts): [`DecisionAgent`](Agentic-ai/ai_agent.py) in [Agentic-ai/ai_agent.py](Agentic-ai/ai_agent.py)
- Task creation & tool wiring: [`AgentTaskSystem`](Agentic-ai/ai_agent_task.py) in [Agentic-ai/ai_agent_task.py](Agentic-ai/ai_agent_task.py)
- Knowledge base tools:
  - Pinecone-based KB: [Agentic-ai/tools/Knowledgebase/knowledge_base.py](Agentic-ai/tools/Knowledgebase/knowledge_base.py)
  - Document ingestion: [Agentic-ai/tools/Knowledgebase/ingest_documents.py](Agentic-ai/tools/Knowledgebase/ingest_documents.py)
  - Simple retriever: [Agentic-ai/tools/Knowledgebase/retriever_simple.py](Agentic-ai/tools/Knowledgebase/retriever_simple.py)
- Web / browser tools and search helpers: [Agentic-ai/tools/browser-tool.py](Agentic-ai/tools/browser-tool.py) and related search tools referenced in [Agentic-ai/ARCHITECTURE.md](Agentic-ai/ARCHITECTURE.md)
- Backend services & orchestration endpoints:
  - API server and socket events: [backend/main.py](backend/main.py)
  - Agent manager / LLM wiring: [`DecisionAgentSystem`](backend/app/services/agent_system.py) in [backend/app/services/agent_system.py](backend/app/services/agent_system.py)
  - Task system used by backend: [`AgentTaskSystem`](backend/app/services/task_system.py) in [backend/app/services/task_system.py](backend/app/services/task_system.py)
- Frontend entry: Next.js root layout and pages: [frontend/src/app/layout.tsx](frontend/src/app/layout.tsx) and the policy/session pages under [frontend/src/app/policy](frontend/src/app/policy) and [frontend/src/app/session](frontend/src/app/session)

Quick start (local, minimal):

1. Set environment variables (see [Agentic-ai/.env](Agentic-ai/.env) pattern and [Agentic-ai/README.md](Agentic-ai/README.md) configuration).
2. Run backend:
   - cd backend && pip install -r requirements.txt && uvicorn main:app --reload
3. Run orchestrator / experiments:
   - cd Agentic-ai && pip install -r requirements.txt && python uagent_main.py --mode quick
4. Run frontend:
   - cd frontend && npm install && npm run dev

Where to read implementation details:

- Tool usage & when tools are enabled: [Agentic-ai/TOOL_USAGE_FLOW.md](Agentic-ai/TOOL_USAGE_FLOW.md)
- System architecture: [Agentic-ai/ARCHITECTURE.md](Agentic-ai/ARCHITECTURE.md)
- Project-level README with detailed instructions: [Agentic-ai/README.md](Agentic-ai/README.md)

If you want a shorter targeted change (e.g., update the root README further or copy content into a specific subfolder), say which file to modify.
