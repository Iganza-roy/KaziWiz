
from crewai import Task
from crewai.tools import BaseTool
from tools.search_tool import EconomicSearchTools
from tools.Knowledgebase.retriever_simple import get_knowledge_base_tools


class AgentTaskSystem:
    """
    Centralized task creation system for all agents and experts.
    Tasks are generalized and can be shared across different agents.
    """
    
    def __init__(self):
        # Initialize search tools (these are LangChain @tool decorated, compatible with CrewAI)
        try:
            self.search_tools = [
                EconomicSearchTools.search_economic_data,
                EconomicSearchTools.search_policy_cases,
                EconomicSearchTools.search_financial_stats,
                EconomicSearchTools.search_market_data,
            ]
            print(f"✅ Loaded {len(self.search_tools)} web search tools")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize search tools: {e}")
            self.search_tools = []
        
        # Knowledge base tools are temporarily disabled (Pinecone not required)
        # You can re-enable by installing: pip install pinecone-client
        try:
            kb_tools_raw = get_knowledge_base_tools()
            self.kb_tools = [t for t in kb_tools_raw if t is not None] if kb_tools_raw else []
            if self.kb_tools:
                print(f"✅ Loaded {len(self.kb_tools)} knowledge base tools")
        except Exception as e:
            print(f"ℹ️  Knowledge base tools unavailable (optional): {str(e)[:50]}")
            self.kb_tools = []
        
        # Combine all available tools
        self.all_tools = self.search_tools + self.kb_tools
        
        if self.all_tools:
            print(f"🔧 Total tools available: {len(self.all_tools)}")
        else:
            print("ℹ️  Running without external tools (using LLM knowledge only)")
    
    # ========== GENERALIZED TASK TEMPLATES ==========
    
    def create_research_task(self, agent, policy_topic, focus_area):
        """
        Generalized research task - can be used by any expert agent
        
        Args:
            agent: The agent performing the research
            policy_topic: The policy being analyzed
            focus_area: Specific focus (e.g., "economic impact", "social welfare", "legal compliance")
        """
        return Task(
            description=f"""Research and analyze: {policy_topic}
            
            YOUR FOCUS AREA: {focus_area}
            
            STEP 1 - MANDATORY RESEARCH (USE ALL AVAILABLE TOOLS):
            - Search the internal knowledge base for relevant policies and precedents
            - Search for economic data and current statistics related to this topic
            - Search for policy case studies and international examples
            - Search for financial statistics and impact data
            - Search for market data and business impacts
            
            STEP 2 - ANALYZE FROM YOUR EXPERTISE PERSPECTIVE:
            Based on your role and expertise, analyze:
            - Key findings from your research (cite all sources)
            - Specific impacts relevant to your domain
            - Data-driven insights and evidence
            - Risks and opportunities from your perspective
            - Precedents and lessons from other implementations
            
            STEP 3 - FORMULATE YOUR POSITION:
            - State your stance: SUPPORT / OPPOSE / CONDITIONAL / NEUTRAL
            - Provide 3-5 key evidence-based arguments
            - Cite all data sources and research findings
            - Highlight critical considerations for your domain
            
            IMPORTANT: Use the search tools to gather real data and cite all sources.
            If tools are unavailable, use your knowledge and provide evidence-based analysis.
            """,
            agent=agent,
            expected_output=f"Comprehensive research analysis of {policy_topic} from {focus_area} perspective, with cited sources and clear position statement.",
            tools=self.search_tools  # Web search tools enabled
        )
    
    def create_debate_task(self, agent, policy_topic, position_context=""):
        """
        Generalized debate task - structured argumentation
        
        Args:
            agent: The agent participating in debate
            policy_topic: The policy being debated
            position_context: Optional context about other agents' positions
        """
        context_section = f"\n\nCONTEXT FROM OTHER EXPERTS:\n{position_context}\n" if position_context else ""
        
        return Task(
            description=f"""Participate in policy debate: {policy_topic}
            {context_section}
            PHASE 1 - OPENING STATEMENT:
            - State your position clearly (SUPPORT/OPPOSE/CONDITIONAL)
            - Provide your top 3 arguments backed by research
            - Reference data from your earlier research (cite sources)
            
            PHASE 2 - EVIDENCE PRESENTATION:
            - Present quantitative data supporting your position
            - Reference case studies and precedents
            - Highlight risks and benefits from your domain expertise
            - Address potential counterarguments preemptively
            
            PHASE 3 - SYNTHESIS:
            - Acknowledge valid points from other perspectives
            - Explain why your position best serves the overall goal
            - Propose any conditions or modifications if applicable
            - Make your case for why decision-makers should consider your view
            
            IMPORTANT: Be objective, evidence-based, and collaborative.
            Focus on finding the best solution, not winning an argument.
            """,
            agent=agent,
            expected_output="Structured debate contribution with opening statement, evidence presentation, and synthesis, all backed by cited research.",
            tools=self.search_tools  # Web search tools enabled for evidence gathering
        )
    
    def create_voting_task(self, agent, policy_topic, all_arguments):
        """
        Generalized voting task - final decision making
        
        Args:
            agent: The agent casting a vote
            policy_topic: The policy being voted on
            all_arguments: Summary of all expert arguments
        """
        return Task(
            description=f"""Cast your final vote on: {policy_topic}
            
            ALL EXPERT ARGUMENTS SUMMARY:
            {all_arguments}
            
            YOUR VOTING DECISION PROCESS:
            
            1. REVIEW ALL EVIDENCE:
               - Consider all expert perspectives presented
               - Weigh the strength of evidence from each domain
               - Identify areas of consensus and disagreement
            
            2. EVALUATE FROM YOUR EXPERTISE:
               - How does this policy align with your domain priorities?
               - What are the critical risks or benefits for your area?
               - Can concerns be mitigated with modifications?
            
            3. CAST YOUR VOTE:
               Choose ONE of the following:
               - STRONGLY SUPPORT: Policy should be implemented as proposed
               - SUPPORT: Policy is beneficial but may need minor adjustments
               - CONDITIONAL: Support only if specific conditions are met (specify)
               - OPPOSE: Policy has significant concerns (specify)
               - STRONGLY OPPOSE: Policy should not be implemented
               - ABSTAIN: Insufficient expertise or conflict of interest
            
            4. VOTING RATIONALE:
               - Explain your vote in 3-5 sentences
               - Reference the most compelling evidence that influenced your decision
               - State any conditions or concerns for the record
            
            FORMAT YOUR RESPONSE AS:
            VOTE: [Your vote]
            RATIONALE: [Your explanation]
            CONDITIONS: [Any conditions, or "None"]
            """,
            agent=agent,
            expected_output="Clear vote (STRONGLY SUPPORT/SUPPORT/CONDITIONAL/OPPOSE/STRONGLY OPPOSE/ABSTAIN) with rationale and any conditions.",
            tools=[]  # No tools needed for voting
        )
    
    # ========== SPECIALIZED TASKS FOR SPEAKER EXPERTS ==========
    
    def create_problem_statement_task(self, agent, policy_topic, background_context=""):
        """
        Task for Problem Statement Expert to explain the issue to all agents
        """
        return Task(
            description=f"""You are the Problem Statement Clarification Expert.
            
            POLICY TOPIC: {policy_topic}
            
            BACKGROUND CONTEXT:
            {background_context if background_context else "User has requested analysis of this policy."}
            
            YOUR TASK: Clearly articulate the problem statement for all expert agents
            
            1. PROBLEM DEFINITION:
               - What is the core issue or challenge being addressed?
               - Why is this policy being considered?
               - What are the current pain points or deficiencies?
            
            2. POLICY OBJECTIVES:
               - What are the stated goals of this policy?
               - What outcomes are expected?
               - What metrics define success?
            
            3. SCOPE AND BOUNDARIES:
               - What is included in this policy analysis?
               - What is explicitly out of scope?
               - What time horizon are we considering?
            
            4. KEY QUESTIONS FOR EXPERTS:
               - List 5-7 critical questions each expert should address
               - Frame questions specific to different domains (economic, social, legal, etc.)
            
            5. CONTEXT FOR DELIBERATION:
               - Relevant background information all experts should know
               - Any constraints or requirements (legal, budgetary, political)
               - Stakeholders affected by this decision
            
            Present this in a clear, structured format that ensures all experts
            have a shared understanding before beginning their analysis.
            """,
            agent=agent,
            expected_output="Comprehensive problem statement with policy objectives, scope, key questions for experts, and relevant context.",
            tools=[]  # No tools needed for problem statement
        )
    
    def create_turn_management_task(self, agent, expert_list, policy_topic):
        """
        Task for Turn Management Expert to orchestrate discussion
        """
        expert_names = "\n".join([f"- {expert}" for expert in expert_list])
        
        return Task(
            description=f"""You are the Discussion Turn Management Expert.
            
            POLICY: {policy_topic}
            
            EXPERT AGENTS PARTICIPATING:
            {expert_names}
            
            YOUR TASK: Manage the discussion flow to ensure fair and productive deliberation
            
            1. ESTABLISH DISCUSSION RULES:
               - Set time limits for each phase (opening, debate, voting)
               - Define speaking order and turn-taking protocol
               - Establish rules for respectful disagreement
               - Define when research phase ends and debate begins
            
            2. ORCHESTRATE DISCUSSION PHASES:
               
               PHASE 1 - RESEARCH (Sequential):
               - Each expert conducts research in their domain
               - Order: Economic → Social → Geospatial → Income → Resource → Adaptation → Legal → Feedback
               
               PHASE 2 - OPENING STATEMENTS (Round-robin):
               - Each expert presents their position and top 3 arguments
               - 2-3 minutes per expert
               - No interruptions during opening statements
               
               PHASE 3 - STRUCTURED DEBATE (Moderated):
               - Group experts by related domains
               - Allow cross-examination and response
               - Ensure all voices are heard equally
               - Facilitate consensus-building discussions
               
               PHASE 4 - SYNTHESIS (Collaborative):
               - Identify areas of consensus
               - Explore compromise solutions
               - Address outstanding concerns
               
               PHASE 5 - VOTING (Sequential):
               - Each expert casts their vote with rationale
               - No changing votes after casting
            
            3. ENSURE PARTICIPATION EQUITY:
               - Track speaking time for each expert
               - Invite quieter experts to contribute
               - Prevent any single expert from dominating
               - Balance technical depth with accessibility
            
            4. MAINTAIN FOCUS:
               - Redirect off-topic discussions
               - Summarize key points at phase transitions
               - Keep deliberation on schedule
            
            OUTPUT: Structured agenda with phase timings, speaking order, and facilitation guidelines.
            """,
            agent=agent,
            expected_output="Detailed discussion management plan with phases, speaking order, rules, and facilitation guidelines.",
            tools=[]
        )
    
    def create_voting_coordination_task(self, agent, policy_topic, all_votes):
        """
        Task for Voting & Announcement Expert to tally votes and announce results
        """
        return Task(
            description=f"""You are the Voting Coordinator and Results Announcer.
            
            POLICY DECISION: {policy_topic}
            
            ALL EXPERT VOTES:
            {all_votes}
            
            YOUR TASK: Conduct transparent vote tallying and announce the final decision
            
            1. VOTE TABULATION:
               - Count all votes by category:
                 * STRONGLY SUPPORT: [count]
                 * SUPPORT: [count]
                 * CONDITIONAL: [count]
                 * OPPOSE: [count]
                 * STRONGLY OPPOSE: [count]
                 * ABSTAIN: [count]
               - Calculate weighted score (Strongly Support=+2, Support=+1, Conditional=0, Oppose=-1, Strongly Oppose=-2)
               - Identify majority and minority positions
            
            2. CONSENSUS ANALYSIS:
               - Level of agreement: UNANIMOUS / STRONG CONSENSUS / MAJORITY / DIVIDED / NO CONSENSUS
               - Areas of agreement across experts
               - Key points of contention
               - Conditional votes and their requirements
            
            3. SYNTHESIZE RATIONALES:
               - Summarize arguments from supporting experts
               - Summarize arguments from opposing experts
               - Highlight most compelling evidence on each side
               - Note any critical warnings or conditions
            
            4. FINAL DECISION ANNOUNCEMENT:
               
               DECISION: [APPROVED / CONDITIONALLY APPROVED / REJECTED / REQUIRES FURTHER STUDY]
               
               VOTE BREAKDOWN: [Numbers and percentages]
               
               CONSENSUS LEVEL: [Your assessment]
               
               KEY SUPPORTING ARGUMENTS:
               - [Top 3 arguments for the decision]
               
               KEY CONCERNS RAISED:
               - [Top 3 concerns from dissenting or conditional votes]
               
               CONDITIONS FOR IMPLEMENTATION (if applicable):
               - [List all conditions from conditional votes]
               
               MINORITY OPINION SUMMARY:
               - [Respectful summary of dissenting views]
               
               NEXT STEPS:
               - [Recommended actions based on the decision]
            
            5. FORMAL RECORD:
               - Document the decision for official record
               - Ensure transparency and traceability
               - Note any abstentions and their reasons
            
            Present the final decision with authority, clarity, and respect for all perspectives.
            """,
            agent=agent,
            expected_output="Complete vote tally, consensus analysis, formal decision announcement with supporting/opposing arguments, conditions, and next steps.",
            tools=[]
        )
    
    # ========== DOMAIN-SPECIFIC TASK CREATORS ==========
    
    def create_economic_analysis_task(self, agent, policy_topic):
        """Task for Economic Experts (Macro, Micro, Policy Impact, Trade)"""
        return self.create_research_task(
            agent, 
            policy_topic,
            focus_area="""ECONOMIC IMPACT ANALYSIS:
            - Fiscal costs and revenue implications
            - GDP, growth, and productivity impacts
            - Market effects and business impacts
            - Trade and investment implications
            - Cost-benefit analysis with NPV/ROI calculations
            - Budget and deficit considerations"""
        )
    
    def create_social_welfare_task(self, agent, policy_topic):
        """Task for Social Welfare Experts (Healthcare, Education, Housing)"""
        return self.create_research_task(
            agent,
            policy_topic,
            focus_area="""SOCIAL WELFARE IMPACT ANALYSIS:
            - Healthcare accessibility and health outcomes
            - Educational impacts and skills development
            - Housing affordability and social safety nets
            - Impact on vulnerable and disadvantaged populations
            - Social equity and fairness considerations
            - Quality of life and well-being metrics"""
        )
    
    def create_geospatial_demographic_task(self, agent, policy_topic):
        """Task for Geospatial/Demographic Experts"""
        return self.create_research_task(
            agent,
            policy_topic,
            focus_area="""GEOSPATIAL & DEMOGRAPHIC ANALYSIS:
            - Geographic distribution of impacts (rural vs urban)
            - Demographic-specific effects (age, gender, ethnicity)
            - Regional inequality and spatial justice
            - Resource access and employment by location
            - Population mobility and migration patterns
            - Infrastructure and service distribution"""
        )
    
    def create_income_inequality_task(self, agent, policy_topic):
        """Task for Income Inequality Experts"""
        return self.create_research_task(
            agent,
            policy_topic,
            focus_area="""INCOME INEQUALITY ANALYSIS:
            - Effects on income distribution and wealth gaps
            - Progressive vs regressive impact analysis
            - Root causes of inequality addressed (or exacerbated)
            - Redistribution mechanisms and effectiveness
            - Impact on social mobility
            - Long-term inequality trajectories"""
        )
    
    def create_resource_allocation_task(self, agent, policy_topic):
        """Task for Resource Allocation Experts"""
        return self.create_research_task(
            agent,
            policy_topic,
            focus_area="""RESOURCE ALLOCATION ANALYSIS:
            - Optimal distribution of funds and resources
            - Resource efficiency and waste minimization
            - Prioritization frameworks and criteria
            - Real-time adaptation to changing needs
            - System bottlenecks and inefficiencies
            - Sustainability of resource commitments"""
        )
    
    def create_adaptation_feedback_task(self, agent, policy_topic):
        """Task for Adaptation & Feedback Experts"""
        return self.create_research_task(
            agent,
            policy_topic,
            focus_area="""ADAPTATION & MONITORING ANALYSIS:
            - Policy flexibility and adaptability mechanisms
            - Monitoring frameworks and KPIs
            - Feedback loops and adjustment triggers
            - Resilience to changing conditions
            - Continuous improvement processes
            - Long-term sustainability and evolution"""
        )
    
    def create_legal_compliance_task(self, agent, policy_topic):
        """Task for Legal Expert"""
        return self.create_research_task(
            agent,
            policy_topic,
            focus_area="""LEGAL COMPLIANCE ANALYSIS:
            - Constitutional compliance
            - Statutory and regulatory requirements
            - Legal precedents and case law
            - Ethical standards and principles
            - Rights and freedoms implications
            - Potential legal challenges and risks"""
        )
    
    # ========== COMPLETE WORKFLOW TASK GENERATOR ==========
    
    def create_full_deliberation_workflow(self, agents_dict, policy_topic, background_context=""):
        """
        Create complete task workflow for full multi-expert deliberation
        
        Args:
            agents_dict: Dictionary with agent instances keyed by role
                        e.g., {"problem_statement": agent1, "economic_macro": agent2, ...}
            policy_topic: The policy to analyze
            background_context: Optional background information
        
        Returns:
            List of tasks in execution order
        """
        tasks = []
        
        # PHASE 1: Problem Statement (Speaker Expert 1)
        if "problem_statement" in agents_dict:
            tasks.append(
                self.create_problem_statement_task(
                    agents_dict["problem_statement"],
                    policy_topic,
                    background_context
                )
            )
        
        # PHASE 2: Turn Management Setup (Speaker Expert 2)
        if "turn_management" in agents_dict:
            expert_names = [role for role in agents_dict.keys() if role not in ["problem_statement", "turn_management", "voting_announcement"]]
            tasks.append(
                self.create_turn_management_task(
                    agents_dict["turn_management"],
                    expert_names,
                    policy_topic
                )
            )
        
        # PHASE 3: Research Tasks (All Domain Experts)
        research_mapping = {
            "economic_macro": self.create_economic_analysis_task,
            "economic_micro": self.create_economic_analysis_task,
            "policy_impact": self.create_economic_analysis_task,
            "trade_investment": self.create_economic_analysis_task,
            "healthcare_welfare": self.create_social_welfare_task,
            "education_welfare": self.create_social_welfare_task,
            "housing_welfare": self.create_social_welfare_task,
            "geographic_poverty": self.create_geospatial_demographic_task,
            "demographic_policy": self.create_geospatial_demographic_task,
            "resource_access": self.create_geospatial_demographic_task,
            "inequality_causes": self.create_income_inequality_task,
            "income_redistribution": self.create_income_inequality_task,
            "inequality_impact": self.create_income_inequality_task,
            "resource_optimization": self.create_resource_allocation_task,
            "realtime_allocation": self.create_resource_allocation_task,
            "system_efficiency": self.create_resource_allocation_task,
            "policy_monitoring": self.create_adaptation_feedback_task,
            "adaptive_policy": self.create_adaptation_feedback_task,
            "legal": self.create_legal_compliance_task,
        }
        
        for role, task_creator in research_mapping.items():
            if role in agents_dict:
                tasks.append(task_creator(agents_dict[role], policy_topic))
        
        # PHASE 4: Debate Tasks (All Domain Experts)
        for role in research_mapping.keys():
            if role in agents_dict:
                tasks.append(
                    self.create_debate_task(
                        agents_dict[role],
                        policy_topic,
                        position_context="Review other experts' research findings above."
                    )
                )
        
        # PHASE 5: Voting Tasks (All Domain Experts)
        for role in research_mapping.keys():
            if role in agents_dict:
                tasks.append(
                    self.create_voting_task(
                        agents_dict[role],
                        policy_topic,
                        all_arguments="Review all debate contributions above."
                    )
                )
        
        # PHASE 6: Vote Tallying and Final Announcement (Speaker Expert 3)
        if "voting_announcement" in agents_dict:
            tasks.append(
                self.create_voting_coordination_task(
                    agents_dict["voting_announcement"],
                    policy_topic,
                    all_votes="Review all votes cast above."
                )
            )
        
        return tasks
    
    # ========== SIMPLIFIED WORKFLOWS ==========
    
    def create_quick_analysis_workflow(self, agents_dict, policy_topic):
        """
        Simplified workflow: Research → Vote → Announce
        For faster decision-making without full debate
        """
        tasks = []
        
        # Research phase
        research_agents = [k for k in agents_dict.keys() if k not in ["problem_statement", "turn_management", "voting_announcement"]]
        for role in research_agents:
            tasks.append(
                self.create_research_task(agents_dict[role], policy_topic, f"Analysis from {role} perspective")
            )
        
        # Voting phase
        for role in research_agents:
            tasks.append(
                self.create_voting_task(agents_dict[role], policy_topic, "Review all research above.")
            )
        
        # Announcement
        if "voting_announcement" in agents_dict:
            tasks.append(
                self.create_voting_coordination_task(
                    agents_dict["voting_announcement"],
                    policy_topic,
                    "Review all votes above."
                )
            )
        
        return tasks


# ========== CONVENIENCE FUNCTIONS ==========

def create_task_system():
    """Factory function to create task system instance"""
    return AgentTaskSystem()


# ========== USAGE EXAMPLE ==========

if __name__ == "__main__":
    print("""
    AgentTaskSystem - Usage Example
    =================================
    
    # Initialize the task system
    task_system = AgentTaskSystem()
    
    # Create a research task for any agent
    task = task_system.create_research_task(
        agent=my_agent,
        policy_topic="Universal Basic Income",
        focus_area="Economic feasibility and fiscal impact"
    )
    
    # Create a full deliberation workflow
    agents = {
        "problem_statement": problem_expert,
        "economic_macro": macro_expert,
        "social_welfare": welfare_expert,
        "voting_announcement": voting_expert,
        # ... more agents
    }
    
    tasks = task_system.create_full_deliberation_workflow(
        agents_dict=agents,
        policy_topic="Universal Basic Income",
        background_context="Government considering UBI pilot program"
    )
    
    # Use tasks with CrewAI
    from crewai import Crew
    crew = Crew(agents=list(agents.values()), tasks=tasks, verbose=True)
    result = crew.kickoff()
    """)
