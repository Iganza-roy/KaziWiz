"""
Task System Module
Defines tasks for all deliberation phases
"""

from crewai import Task


class AgentTaskSystem:
    """Centralized task creation system for all agents"""
    
    def __init__(self):
        self.search_tools = []  # Can add tools later if needed
    
    def create_problem_statement_task(self, agent, policy_topic, context=""):
        """Phase 2: Problem Statement Clarification"""
        return Task(
            description=f"""Clearly explain and articulate the policy problem: {policy_topic}
            
            {context}
            
            ⚠️ IMPORTANT: Provide a policy analysis in natural language - NOT code or programming examples!
            
            YOUR TASK:
            1. Define the core problem in clear, accessible language
            2. Break down the challenge into key components
            3. Identify the main stakeholders affected
            4. Explain why this policy matters
            5. Set the stage for expert deliberation
            
            OUTPUT FORMAT: Write your response as a clear policy problem statement with paragraphs.
            DO NOT output code, programming syntax, or unrelated content.
            
            Ensure all participating experts understand the problem before analysis begins.
            """,
            agent=agent,
            expected_output="Clear problem statement that all experts can understand and analyze. Must be in natural language, NOT code.",
        )
    
    def create_turn_management_task(self, agent, expert_list, policy_topic):
        """Phase 3: Turn Management Setup"""
        experts = ", ".join(expert_list)
        return Task(
            description=f"""Establish discussion management for policy: {policy_topic}
            
            PARTICIPATING EXPERTS:
            {experts}
            
            YOUR TASK:
            1. Establish clear discussion rules and flow
            2. Outline the deliberation process phases
            3. Ensure fair participation from all experts
            4. Set expectations for evidence-based debate
            5. Create a structured timeline for deliberation
            
            Maintain neutrality and facilitate productive discussion.
            """,
            agent=agent,
            expected_output="Discussion management plan with clear rules and deliberation structure.",
        )
    
    def create_research_task(self, agent, policy_topic, focus_area):
        """Phase 4: Research Tasks with Web Search"""
        return Task(
            description=f"""Research and analyze: {policy_topic}
            
            YOUR FOCUS AREA: {focus_area}
            
            ⚠️ IMPORTANT: Provide policy analysis in natural language - NOT code or programming examples!
            
            🔍 **USE YOUR WEB SEARCH TOOL TO:**
            - Search for latest statistics, reports, and data
            - Find case studies of similar policies
            - Look up expert opinions and research papers
            - Discover recent news and developments
            - Gather evidence from credible sources
            
            STEP 1 - WEB RESEARCH:
            - Use the search tool to find relevant, current information
            - Gather data from government sources, think tanks, academic studies
            - Look for real-world examples and case studies
            - Find expert analyses and policy evaluations
            - Collect specific statistics and numbers
            
            STEP 2 - ANALYSIS:
            - Evaluate impacts from your expertise perspective based on findings
            - Identify specific implications for your domain
            - Assess feasibility and effectiveness using researched evidence
            - Consider unintended consequences found in case studies
            
            STEP 3 - POSITION (Write in clear paragraphs, NOT code):
            - State your stance: SUPPORT / OPPOSE / CONDITIONAL / NEUTRAL
            - Provide 3-5 key evidence-based arguments (with sources from web research)
            - Cite specific data, studies, or examples you found
            - Highlight critical considerations
            - Suggest improvements or conditions if applicable
            
            📊 **CITE YOUR SOURCES**: Include specific references to data, studies, or reports you found
            
            OUTPUT FORMAT: Write your analysis as a policy brief with clear paragraphs and bullet points.
            DO NOT output code, programming syntax, or unrelated content.
            Be thorough, objective, and evidence-based using real web-sourced information.
            """,
            agent=agent,
            expected_output=f"Comprehensive research analysis from {focus_area} perspective with web-sourced evidence and clear position. Must be in natural language policy analysis format, NOT code.",
        )
    
    def create_debate_task(self, agent, policy_topic, context=""):
        """Phase 5: Debate Tasks"""
        return Task(
            description=f"""Participate in structured debate: {policy_topic}
            
            ⚠️ IMPORTANT: Provide debate arguments in natural language - NOT code!
            
            {context}
            
            PHASE 1 - OPENING STATEMENT:
            - State your position clearly (SUPPORT/OPPOSE/CONDITIONAL)
            - Present your top 3 arguments
            - Reference your research findings
            
            PHASE 2 - ARGUMENTATION:
            - Present evidence supporting your position
            - Reference data and precedents
            - Address potential counterarguments
            - Highlight risks and benefits from your expertise
            
            PHASE 3 - SYNTHESIS:
            - Acknowledge valid points from other perspectives
            - Explain why your position best serves the goal
            - Propose conditions or modifications if applicable
            - Make your case to decision-makers
            
            OUTPUT FORMAT: Write clear arguments as paragraphs with evidence.
            DO NOT output code or programming examples.
            
            Be objective, collaborative, and focused on the best solution.
            """,
            agent=agent,
            expected_output="Structured debate contribution with opening statement, arguments, and synthesis. Must be in natural language, NOT code.",
        )
    
    def create_voting_task(self, agent, policy_topic, arguments_summary=""):
        """Phase 6: Voting Tasks"""
        return Task(
            description=f"""Cast your vote on policy: {policy_topic}
            
            {arguments_summary}
            
            YOUR DECISION:
            1. Review all research and debate contributions
            2. Consider evidence from your expertise area
            3. Weigh benefits against risks
            4. Make your final decision
            
            VOTE FORMAT:
            - Decision: [APPROVE / REJECT / APPROVE WITH CONDITIONS]
            - Confidence: [HIGH / MEDIUM / LOW]
            - Key Reason: [1-2 sentence explanation]
            - Critical Conditions (if applicable): [List any necessary conditions]
            
            Vote based on evidence and your expert judgment.
            """,
            agent=agent,
            expected_output="Clear vote with decision, confidence level, reasoning, and any conditions.",
        )
    
    def create_voting_coordination_task(self, agent, policy_topic, votes_summary=""):
        """Phase 7: Vote Tallying and Announcement"""
        return Task(
            description=f"""Tally votes and announce final decision: {policy_topic}
            
            {votes_summary}
            
            YOUR TASK:
            1. Count all votes cast by expert agents
            2. Analyze voting patterns and consensus levels
            3. Identify majority position and dissenting views
            4. Summarize key arguments for and against
            5. Announce the final collective decision
            6. Explain the rationale based on expert consensus
            7. List any important conditions or caveats
            
            FINAL ANNOUNCEMENT FORMAT:
            - DECISION: [APPROVED / REJECTED / CONDITIONALLY APPROVED]
            - VOTE TALLY: [X in favor, Y opposed, Z conditional]
            - CONSENSUS LEVEL: [Strong / Moderate / Divided]
            - KEY ARGUMENTS FOR: [Summary]
            - KEY ARGUMENTS AGAINST: [Summary]
            - CONDITIONS (if applicable): [List]
            - IMPLEMENTATION RECOMMENDATIONS: [List]
            
            Ensure transparency and clarity in the final announcement.
            """,
            agent=agent,
            expected_output="Comprehensive final decision announcement with vote tally and reasoning.",
        )
    
    # Specialized research tasks for different expert groups
    
    def create_economic_analysis_task(self, agent, policy_topic):
        return self.create_research_task(agent, policy_topic, "Economic Impact and Fiscal Analysis")
    
    def create_social_welfare_task(self, agent, policy_topic):
        return self.create_research_task(agent, policy_topic, "Social Welfare and Community Impact")
    
    def create_geospatial_demographic_task(self, agent, policy_topic):
        return self.create_research_task(agent, policy_topic, "Geospatial and Demographic Analysis")
    
    def create_income_inequality_task(self, agent, policy_topic):
        return self.create_research_task(agent, policy_topic, "Income Distribution and Inequality")
    
    def create_resource_allocation_task(self, agent, policy_topic):
        return self.create_research_task(agent, policy_topic, "Resource Management and Allocation")
    
    def create_adaptation_feedback_task(self, agent, policy_topic):
        return self.create_research_task(agent, policy_topic, "Policy Adaptation and Monitoring")
    
    def create_legal_compliance_task(self, agent, policy_topic):
        return self.create_research_task(agent, policy_topic, "Legal Compliance and Regulatory Framework")
