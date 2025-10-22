"""
Agent System Module
Defines all 26+ expert agents for policy deliberation
"""

from crewai import Agent
from crewai.llm import LLM
import os
from .tools import ResearchTools
from .custom_llm import create_asi_cloud_llm


class DecisionAgentSystem:
    """Manages all expert agents in the deliberation system"""
    
    def __init__(self):
        # Initialize the LLM for all agents
        # Using asi1-mini with output validation
        self.llm = LLM(
            model="asi1-mini",
            api_key=os.environ.get("ASI_API_KEY"),
            base_url="https://inference.asicloud.cudos.org/v1",
            temperature=0.3
        )
        
        # Initialize research tools
        self.research_tools = ResearchTools()
        self.tools = self.research_tools.get_research_tools()
    
    # ========== Speaker Experts (Orchestration) ==========
    
    def problem_statement_expert(self):
        return Agent(
            role="Problem Statement Clarification Expert",
            goal="Clearly explain and articulate the problem statement to all agents",
            backstory="Communication expert specializing in problem framing and stakeholder alignment",
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )
    
    def turn_management_expert(self):
        return Agent(
            role="Discussion Turn Management Expert",
            goal="Manage the order and timing of agent contributions",
            backstory="Professional moderator with expertise in facilitation and equitable discussion management",
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )
    
    def voting_announcement_expert(self):
        return Agent(
            role="Voting Coordinator and Results Announcer",
            goal="Conduct transparent voting and announce final decisions",
            backstory="Governance specialist with expertise in voting systems and consensus-building",
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )
    
    # ========== Core Policy Experts ==========
    
    def economic_agent(self):
        return Agent(
            role="Economic Analyst",
            goal="Analyze economic trends, data, and impacts using web research and data analysis",
            backstory="Expert economic analyst with deep knowledge of urban economics and fiscal policy. Uses web search to find latest economic data, research papers, and expert opinions.",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def social_agent(self):
        return Agent(
            role="Social Dynamics Expert",
            goal="Analyze social trends and community behaviors using real-world data and research",
            backstory="Social scientist specializing in urban sociology and community dynamics. Conducts web research to find case studies, social impact reports, and community feedback.",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def geospatial_agent(self):
        return Agent(
            role="Geospatial Analyst",
            goal="Interpret geospatial data and location-based patterns using online GIS resources",
            backstory="GIS specialist with expertise in urban planning and spatial analysis. Searches for geographic data, maps, and location-based research.",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def income_agent(self):
        return Agent(
            role="Income Distribution Analyst",
            goal="Analyze income trends and distribution patterns using economic research",
            backstory="Economist specializing in income inequality and wealth distribution. Conducts web research to find income statistics, studies, and policy impacts.",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def resource_agent(self):
        return Agent(
            role="Resource Management Expert",
            goal="Analyze resource allocation and sustainability using environmental data",
            backstory="Sustainability expert with knowledge of resource management and infrastructure. Searches for environmental reports, resource allocation data, and best practices.",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def legal_agent(self):
        return Agent(
            role="Legal Adviser",
            goal="Ensure policies comply with legal and ethical standards using legal databases",
            backstory="Seasoned legal professional specializing in urban policy and taxation laws. Researches case law, legal precedents, and regulatory frameworks online.",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    # ========== Economic Experts (MoE) ==========
    
    def macro_economic_expert(self):
        return Agent(
            role="Macro-Economic Analysis Expert",
            goal="Analyze national-level economic models and GDP impacts using latest economic data",
            backstory="Senior economist with expertise in monetary policy and fiscal analysis. Uses web search to find GDP reports, central bank data, and economic forecasts.",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def micro_economic_expert(self):
        return Agent(
            role="Micro-Economic Analysis Expert",
            goal="Evaluate local economic impacts and business effects using market research",
            backstory="Regional economist specializing in small business economics. Searches for local business data, market trends, and consumer behavior studies.",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def policy_impact_expert(self):
        return Agent(
            role="Policy Impact Analysis Expert",
            goal="Evaluate policy outcomes using predictive modeling and case studies",
            backstory="Policy analyst specializing in econometric modeling and impact assessment. Researches similar policies implemented elsewhere and their outcomes.",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def trade_investment_expert(self):
        return Agent(
            role="Trade and Investment Analysis Expert",
            goal="Analyze international trade and investment impacts using global economic data",
            backstory="International economist with expertise in global trade dynamics. Searches for trade statistics, investment reports, and international economic analyses.",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    # ========== Social Welfare Experts (MoE) ==========
    
    def healthcare_welfare_expert(self):
        return Agent(
            role="Healthcare Accessibility Expert",
            goal="Analyze healthcare accessibility and resource allocation",
            backstory="Public health specialist with expertise in healthcare systems",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def education_welfare_expert(self):
        return Agent(
            role="Education and Skills Development Expert",
            goal="Evaluate education accessibility and workforce development",
            backstory="Education policy expert specializing in vocational training",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def housing_welfare_expert(self):
        return Agent(
            role="Housing and Social Safety Net Expert",
            goal="Analyze housing affordability and welfare policies",
            backstory="Social policy specialist with expertise in affordable housing",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    # ========== Geospatial and Demographic Experts (MoE) ==========
    
    def geographic_poverty_expert(self):
        return Agent(
            role="Geographic Poverty Analysis Expert",
            goal="Conduct spatial analysis of poverty distribution",
            backstory="Geographer specializing in poverty mapping and spatial inequality",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def demographic_policy_expert(self):
        return Agent(
            role="Demographic-Focused Policy Expert",
            goal="Design policies tailored to different demographic groups",
            backstory="Demographer specializing in population studies and culturally-sensitive policy",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def resource_access_expert(self):
        return Agent(
            role="Resource Access and Unemployment Expert",
            goal="Identify areas with high unemployment and low resource access",
            backstory="Labor economist specializing in unemployment analysis",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    # ========== Income Inequality Experts (MoE) ==========
    
    def inequality_causes_expert(self):
        return Agent(
            role="Income Inequality Causes Expert",
            goal="Identify root causes of income inequality",
            backstory="Sociologist specializing in inequality research and structural barriers",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def income_redistribution_expert(self):
        return Agent(
            role="Income Redistribution Policy Expert",
            goal="Design income redistribution policies",
            backstory="Fiscal policy expert specializing in redistributive economics",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def inequality_impact_expert(self):
        return Agent(
            role="Inequality Impact Assessment Expert",
            goal="Evaluate how inequality affects health and education outcomes",
            backstory="Social epidemiologist studying effects of inequality",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    # ========== Resource Allocation Experts (MoE) ==========
    
    def resource_optimization_expert(self):
        return Agent(
            role="Resource Distribution Optimization Expert",
            goal="Optimize allocation of funds and critical resources",
            backstory="Operations research specialist with expertise in optimization algorithms",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def realtime_allocation_expert(self):
        return Agent(
            role="Real-Time Resource Prioritization Expert",
            goal="Prioritize resource allocation during crises",
            backstory="Emergency management specialist with crisis response experience",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def system_efficiency_expert(self):
        return Agent(
            role="Welfare System Efficiency Expert",
            goal="Identify inefficiencies in welfare systems",
            backstory="Public administration expert specializing in government efficiency",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    # ========== Feedback and Adaptation Experts (MoE) ==========
    
    def policy_monitoring_expert(self):
        return Agent(
            role="Policy Outcome Monitoring Expert",
            goal="Monitor policy outcomes using KPIs and impact assessments",
            backstory="Program evaluator with expertise in performance measurement",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def adaptive_policy_expert(self):
        return Agent(
            role="Real-Time Policy Adaptation Expert",
            goal="Adjust policies based on feedback and emerging challenges",
            backstory="Adaptive management specialist and policy innovator",
            verbose=True,
            llm=self.llm,
            tools=self.tools,
            allow_delegation=False
        )
    
    def get_all_agent_definitions(self):
        """
        Get metadata for all agents for display purposes
        Returns list of dicts with agent info
        """
        return [
            # Orchestration Experts
            {"id": "problem_statement", "name": "Problem Statement Expert", "category": "orchestration", "emoji": "📢"},
            {"id": "turn_management", "name": "Turn Management Expert", "category": "orchestration", "emoji": "⚖️"},
            {"id": "voting_announcement", "name": "Voting Coordinator", "category": "orchestration", "emoji": "🗳️"},
            
            # Core Policy Experts
            {"id": "economic", "name": "Economic Analyst", "category": "core", "emoji": "💰"},
            {"id": "social", "name": "Social Dynamics Expert", "category": "core", "emoji": "👥"},
            {"id": "geospatial", "name": "Geospatial Analyst", "category": "core", "emoji": "🗺️"},
            {"id": "income", "name": "Income Distribution Analyst", "category": "core", "emoji": "💵"},
            {"id": "resource", "name": "Resource Management Expert", "category": "core", "emoji": "📊"},
            {"id": "legal", "name": "Legal Adviser", "category": "core", "emoji": "⚖️"},
            
            # Economic MoE
            {"id": "economic_macro", "name": "Macro-Economic Expert", "category": "economic_moe", "emoji": "🌐"},
            {"id": "economic_micro", "name": "Micro-Economic Expert", "category": "economic_moe", "emoji": "🏪"},
            {"id": "policy_impact", "name": "Policy Impact Expert", "category": "economic_moe", "emoji": "📈"},
            {"id": "trade_investment", "name": "Trade & Investment Expert", "category": "economic_moe", "emoji": "🌍"},
            
            # Social Welfare MoE
            {"id": "healthcare_welfare", "name": "Healthcare Expert", "category": "social_moe", "emoji": "🏥"},
            {"id": "education_welfare", "name": "Education Expert", "category": "social_moe", "emoji": "📚"},
            {"id": "housing_welfare", "name": "Housing Expert", "category": "social_moe", "emoji": "🏘️"},
            
            # Geospatial MoE
            {"id": "geographic_poverty", "name": "Geographic Poverty Expert", "category": "geospatial_moe", "emoji": "🗺️"},
            {"id": "demographic_policy", "name": "Demographic Policy Expert", "category": "geospatial_moe", "emoji": "👨‍👩‍👧‍👦"},
            {"id": "resource_access", "name": "Resource Access Expert", "category": "geospatial_moe", "emoji": "🚇"},
            
            # Income Inequality MoE
            {"id": "inequality_causes", "name": "Inequality Causes Expert", "category": "income_moe", "emoji": "⚖️"},
            {"id": "income_redistribution", "name": "Redistribution Policy Expert", "category": "income_moe", "emoji": "💸"},
            {"id": "inequality_impact", "name": "Inequality Impact Expert", "category": "income_moe", "emoji": "📉"},
            
            # Resource Allocation MoE
            {"id": "resource_optimization", "name": "Resource Optimization Expert", "category": "resource_moe", "emoji": "🎯"},
            {"id": "realtime_allocation", "name": "Real-Time Allocation Expert", "category": "resource_moe", "emoji": "⚡"},
            {"id": "system_efficiency", "name": "System Efficiency Expert", "category": "resource_moe", "emoji": "⚙️"},
            
            # Feedback MoE
            {"id": "policy_monitoring", "name": "Policy Monitoring Expert", "category": "feedback_moe", "emoji": "📊"},
            {"id": "adaptive_policy", "name": "Adaptive Policy Expert", "category": "feedback_moe", "emoji": "🔄"},
        ]
