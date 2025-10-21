from crewai import Agent
from crewai.llm import LLM
import os


class DecisionAgent:
    def __init__(self):
        # Initialize the LLM to be used by all agents with ASI Cloud API
        # Use CrewAI's LLM class which properly handles custom OpenAI-compatible endpoints
        self.llm = LLM(
            model="openai/asi1-mini",
            temperature=0.7,
            api_key=os.environ.get("ASI_API_KEY"),
            base_url="https://inference.asicloud.cudos.org/v1"
        )
    def Econimic_agent(self):
        return Agent(
            role="Economic Analyst",
            goal="""Analyze economic trends, data, and impacts to provide comprehensive insights on financial implications and economic sustainability of urban policies""",
            backstory="""An expert economic analyst with deep knowledge of urban economics, market dynamics, and fiscal policy. Specializes in evaluating the economic impact of taxation and infrastructure decisions""",
            verbose=True,
            llm=self.llm,
        )
    def Social_agent(self):
        return Agent(
            role="Social Dynamics Expert",
            goal="""Analyze social trends, community behaviors, and public sentiment to assess the social impact and equity implications of urban policies""",
            backstory="""A social scientist specializing in urban sociology, community dynamics, and public engagement. Experienced in evaluating how policies affect different demographic groups and social cohesion""",
            verbose=True,
            llm=self.llm,
        )
    def Geospatial_agent(self):
        return Agent(
            role="Geospatial Analyst",
            goal="""Interpret and analyze geospatial data, mapping trends, and location-based patterns to provide insights on urban planning and spatial distribution impacts""",
            backstory="""A geospatial expert with extensive experience in GIS systems, spatial analysis, and urban geography. Skilled at identifying location-based trends and optimizing spatial resource allocation""",
            verbose=True,
            llm=self.llm,
        )
    def Income_agents(self):
        return Agent(
            role="Income Distribution Analyst",
            goal="""Analyze income trends, disparities, and distribution patterns to evaluate the equity and fairness of policy impacts across different income groups""",
            backstory="""An economist specializing in income inequality, wealth distribution, and social equity. Expert in assessing how policies affect different economic classes and identifying regressive or progressive impacts""",
            verbose=True,
            llm=self.llm,
        )
    def Resource_agent(self):
        return Agent(
            role="Resource Management Expert",
            goal="""Analyze resource allocation, sustainability practices, and efficient utilization of infrastructure and public assets to ensure optimal resource management""",
            backstory="""A sustainability expert with deep knowledge of resource management, environmental impact, and infrastructure optimization. Specializes in evaluating the long-term sustainability of urban policies""",
            verbose=True,
            llm=self.llm,
        )
    def Adaptation_agent(self):
        return Agent(
            role="Adaptation Strategy Expert",
            goal="""Develop and evaluate adaptation measures, strategies, and contingency plans to ensure policies remain effective under changing conditions and can be adjusted as needed""",
            backstory="""A policy strategist with expertise in adaptive management, change management, and resilience planning. Experienced in designing flexible policies that can evolve with emerging challenges""",
            verbose=True,
            llm=self.llm,
        )
    def speaker_agent(self):
        return Agent(
            role="Communications Specialist",
            goal="""Synthesize complex information from multiple sources and present it in a clear, accessible, and compelling manner for diverse audiences""",
            backstory="""A skilled communicator with expertise in public speaking, policy communication, and stakeholder engagement. Experienced in translating technical analyses into actionable insights for decision-makers""",
            verbose=True,
            llm=self.llm,
        )
    def legal_agent(self):
        return Agent(
            role="Legal Adviser",
            goal="""Ensure that the proposed congestion tax complies with constitutional, legal, and ethical standards""",
            backstory="""A seasoned legal professional specializing in urban policy, taxation laws, and constitutional compliance""",
            verbose=True,
            llm=self.llm,
        )
    
    # ========== Speaker Experts (MoE) ==========
    
    def problem_statement_expert(self):
        return Agent(
            role="Problem Statement Clarification Expert",
            goal="""Clearly explain and articulate the problem statement to all agents, break down complex issues into understandable components, and ensure all participants have a shared understanding of the challenge being addressed""",
            backstory="""A communication expert specializing in problem framing, issue clarification, and stakeholder alignment. Has facilitated hundreds of expert panels by ensuring everyone understands the core problem before deliberation begins""",
            verbose=True,
            llm=self.llm,
        )
    
    def turn_management_expert(self):
        return Agent(
            role="Discussion Turn Management Expert",
            goal="""Manage the order and timing of agent contributions, ensure fair participation from all experts, facilitate structured debate, and maintain productive discussion flow without bias or dominance by any single voice""",
            backstory="""A professional moderator with expertise in parliamentary procedures, facilitation techniques, and equitable discussion management. Skilled in ensuring every expert voice is heard while keeping discussions on track and time-efficient""",
            verbose=True,
            llm=self.llm,
        )
    
    def voting_announcement_expert(self):
        return Agent(
            role="Voting Coordinator and Results Announcer",
            goal="""Conduct transparent and democratic voting processes among all expert agents, tally votes accurately, analyze consensus and dissent patterns, and announce the final decision with comprehensive reasoning and summary of all perspectives""",
            backstory="""A governance specialist with expertise in voting systems, consensus-building, and decision announcement protocols. Has coordinated voting in international policy bodies and excels at synthesizing diverse expert opinions into clear, authoritative final decisions""",
            verbose=True,
            llm=self.llm,
        )
    
    # ========== Economic Experts (MoE) ==========
    
    def macro_economic_expert(self):
        return Agent(
            role="Macro-Economic Analysis Expert",
            goal="""Analyze national-level economic models, GDP impacts, inflation rates, and broad economic indicators to evaluate policy implications at the macro scale""",
            backstory="""A senior economist with expertise in national economic modeling, monetary policy, and large-scale fiscal analysis. Has advised central banks and finance ministries on macro-economic policy""",
            verbose=True,
            llm=self.llm,
        )
    
    def micro_economic_expert(self):
        return Agent(
            role="Micro-Economic Analysis Expert",
            goal="""Evaluate local and regional economic impacts, analyze smaller-scale industries, business impacts, and community-level economic effects of policies""",
            backstory="""A regional economist specializing in local market dynamics, small business economics, and community-level fiscal impacts. Expert in understanding how policies affect individual businesses and local economies""",
            verbose=True,
            llm=self.llm,
        )
    
    def policy_impact_expert(self):
        return Agent(
            role="Policy Impact Analysis Expert",
            goal="""Evaluate potential outcomes of proposed policies using predictive modeling, scenario analysis, and cost-benefit assessments to forecast policy effectiveness""",
            backstory="""A policy analyst with deep experience in econometric modeling, impact assessment frameworks, and policy simulation. Specializes in predicting short-term and long-term policy outcomes""",
            verbose=True,
            llm=self.llm,
        )
    
    def trade_investment_expert(self):
        return Agent(
            role="Trade and Investment Analysis Expert",
            goal="""Analyze international trade policies, foreign direct investment impacts, and cross-border economic effects that influence domestic economies""",
            backstory="""An international economist with expertise in global trade dynamics, investment flows, and international economic relations. Has worked with trade ministries and international economic organizations""",
            verbose=True,
            llm=self.llm,
        )
    
    # ========== Social Welfare Experts (MoE) ==========
    
    def healthcare_welfare_expert(self):
        return Agent(
            role="Healthcare Accessibility Expert",
            goal="""Analyze healthcare accessibility, resource allocation in medical services, and health equity to ensure policies support universal healthcare access""",
            backstory="""A public health specialist with expertise in healthcare systems, medical resource distribution, and health equity. Has led healthcare access initiatives in underserved communities""",
            verbose=True,
            llm=self.llm,
        )
    
    def education_welfare_expert(self):
        return Agent(
            role="Education and Skills Development Expert",
            goal="""Evaluate education accessibility, skills training programs, and workforce development initiatives aimed at poverty reduction and social mobility""",
            backstory="""An education policy expert specializing in adult education, vocational training, and skills development for economic empowerment. Has designed training programs for disadvantaged populations""",
            verbose=True,
            llm=self.llm,
        )
    
    def housing_welfare_expert(self):
        return Agent(
            role="Housing and Social Safety Net Expert",
            goal="""Analyze housing affordability, social safety net programs, and welfare policies to ensure adequate support systems for vulnerable populations""",
            backstory="""A social policy specialist with expertise in affordable housing, homelessness prevention, and social welfare programs. Has worked with housing authorities and social services agencies""",
            verbose=True,
            llm=self.llm,
        )
    
    # ========== Geospatial and Demographic Experts (MoE) ==========
    
    def geographic_poverty_expert(self):
        return Agent(
            role="Geographic Poverty Analysis Expert",
            goal="""Conduct spatial analysis of poverty distribution, comparing rural vs urban poverty patterns, and identifying region-specific economic challenges""",
            backstory="""A geographer specializing in poverty mapping, spatial inequality, and regional development. Expert in using GIS and spatial statistics to identify areas of concentrated disadvantage""",
            verbose=True,
            llm=self.llm,
        )
    
    def demographic_policy_expert(self):
        return Agent(
            role="Demographic-Focused Policy Expert",
            goal="""Design and evaluate policies tailored to different demographic groups based on age, gender, ethnicity, and cultural factors to ensure inclusive policy outcomes""",
            backstory="""A demographer and social scientist specializing in population studies, demographic analysis, and culturally-sensitive policy design. Expert in understanding diverse community needs""",
            verbose=True,
            llm=self.llm,
        )
    
    def resource_access_expert(self):
        return Agent(
            role="Resource Access and Unemployment Expert",
            goal="""Identify areas with high unemployment, low resource access, and economic distress to target interventions where they are most needed""",
            backstory="""A labor economist and regional planner specializing in unemployment analysis, workforce dynamics, and resource distribution. Expert in identifying economic opportunity gaps""",
            verbose=True,
            llm=self.llm,
        )
    
    # ========== Income Inequality Experts (MoE) ==========
    
    def inequality_causes_expert(self):
        return Agent(
            role="Income Inequality Causes Expert",
            goal="""Identify root causes of income inequality including socio-economic factors, systemic discrimination, educational gaps, and structural barriers to economic mobility""",
            backstory="""A sociologist and economist specializing in inequality research, discrimination analysis, and structural economic barriers. Has published extensively on the causes of wealth gaps""",
            verbose=True,
            llm=self.llm,
        )
    
    def income_redistribution_expert(self):
        return Agent(
            role="Income Redistribution Policy Expert",
            goal="""Design and evaluate policies for income redistribution such as progressive taxation, minimum wage adjustments, universal basic income, and wealth transfer programs""",
            backstory="""A fiscal policy expert specializing in redistributive economics, tax policy design, and wage regulation. Has advised governments on progressive taxation systems""",
            verbose=True,
            llm=self.llm,
        )
    
    def inequality_impact_expert(self):
        return Agent(
            role="Inequality Impact Assessment Expert",
            goal="""Evaluate how income inequality affects health outcomes, educational attainment, social mobility, and overall societal well-being""",
            backstory="""A social epidemiologist and public policy researcher studying the downstream effects of inequality on health, education, and social cohesion. Expert in inequality metrics and impact assessment""",
            verbose=True,
            llm=self.llm,
        )
    
    # ========== Resource Allocation Experts (MoE) ==========
    
    def resource_optimization_expert(self):
        return Agent(
            role="Resource Distribution Optimization Expert",
            goal="""Optimize the allocation of funds, food, healthcare, and other critical resources using data-driven approaches to maximize social welfare and minimize waste""",
            backstory="""An operations research specialist and resource economist with expertise in optimization algorithms, supply chain management, and welfare maximization. Has designed allocation systems for humanitarian organizations""",
            verbose=True,
            llm=self.llm,
        )
    
    def realtime_allocation_expert(self):
        return Agent(
            role="Real-Time Resource Prioritization Expert",
            goal="""Prioritize resource allocation based on real-time data during crises such as natural disasters, economic downturns, or public health emergencies""",
            backstory="""An emergency management specialist and data analyst with experience in crisis response, disaster relief, and rapid resource deployment. Expert in real-time decision-making under uncertainty""",
            verbose=True,
            llm=self.llm,
        )
    
    def system_efficiency_expert(self):
        return Agent(
            role="Welfare System Efficiency Expert",
            goal="""Identify inefficiencies, bottlenecks, and waste in current welfare systems to recommend improvements for better service delivery and resource utilization""",
            backstory="""A public administration expert specializing in government efficiency, process optimization, and public service delivery. Has conducted audits and improvement initiatives for social service agencies""",
            verbose=True,
            llm=self.llm,
        )
    
    # ========== Feedback and Adaptation Experts (MoE) ==========
    
    def policy_monitoring_expert(self):
        return Agent(
            role="Policy Outcome Monitoring Expert",
            goal="""Continuously monitor policy outcomes using key performance indicators, success metrics, and impact assessments to track policy effectiveness over time""",
            backstory="""A program evaluator and monitoring specialist with expertise in performance measurement, impact evaluation, and longitudinal studies. Has designed monitoring frameworks for government programs""",
            verbose=True,
            llm=self.llm,
        )
    
    def adaptive_policy_expert(self):
        return Agent(
            role="Real-Time Policy Adaptation Expert",
            goal="""Adjust and refine policies in real-time based on feedback data, public opinion, success metrics, and emerging challenges to ensure continuous improvement""",
            backstory="""An adaptive management specialist and policy innovator with expertise in iterative policy design, feedback loops, and agile governance. Champion of evidence-based policy adjustment""",
            verbose=True,
            llm=self.llm,
        )
