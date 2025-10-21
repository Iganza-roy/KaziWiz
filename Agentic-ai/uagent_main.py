

Advanced multi-expert policy analysis system with:
- Problem statement generation
- Automated research phase
- Structured debate management
- Democratic voting
- Final decision announcement
- uAgents integration support
- CrewAI adapter compatibility
- API registration for Agentverse
- Multi-modal kickoff methods

Policy Topic: Poverty Reduction and Economic Outcome in Urban Areas
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from textwrap import dedent
from crewai import Crew, Process
from dotenv import load_dotenv

# Import agent and task systems
from ai_agent import DecisionAgent
from ai_agent_task import AgentTaskSystem

# Try to import uAgents adapter for Agentverse integration (optional)
try:
    from uagents_adapter import CrewaiRegisterTool
    UAGENTS_AVAILABLE = True
except ImportError:
    UAGENTS_AVAILABLE = False
    print("Note: uagents_adapter not available. Agentverse integration disabled.")


class AutoPolicyDeliberationSystem:
    """
    Automated Policy Deliberation System with Enhanced Integration
    
    Orchestrates the entire decision-making process from problem definition
    through research, debate, voting, and final announcement.
    
    Features:
    - Multi-expert deliberation (26+ agents)
    - Automated research with tools
    - Structured debate and voting
    - uAgents/Agentverse integration
    - CrewAI adapter compatibility
    - Multiple kickoff modes
    """
    
    def __init__(self, policy_topic: str = "", background_context: str = "", 
                 city_data: str = "", policy_type: str = "", 
                 time_range: str = "", interests: str = ""):
        """
        Initialize the deliberation system with flexible parameters
        
        Args:
            policy_topic: Main policy being analyzed
            background_context: Detailed policy context
            city_data: Optional city-specific data
            policy_type: Type of policy (e.g., "Economic", "Social")
            time_range: Evaluation timeframe
            interests: Specific criteria to evaluate
        """
        self.agent_system = DecisionAgent()
        self.task_system = AgentTaskSystem()
        self.deliberation_results = {}
        
        # Policy parameters
        self.policy_topic = policy_topic or "Poverty Reduction and Economic Outcome in Urban Areas"
        self.background_context = background_context
        self.city_data = city_data
        self.policy_type = policy_type
        self.time_range = time_range
        self.interests = interests
        
        # Execution state
        self.agents = None
        self.is_initialized = False
        
        print("\n" + "="*80)
        print("AUTO-CODER POLICY DELIBERATION SYSTEM")
        print("="*80)
        print("Initializing multi-expert decision-making framework...")
        print("="*80 + "\n")
    
    def update_parameters(self, **kwargs):
        """
        Update policy parameters dynamically
        
        Args:
            **kwargs: Any parameter to update (policy_topic, background_context, etc.)
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                print(f"Updated {key}: {value}")
    
    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Enhanced kickoff method compatible with uAgents adapter
        
        This method provides compatibility with CrewAI adapter and uAgents
        integration, allowing the system to be registered and called via Agentverse.
        
        Args:
            inputs: Optional dictionary with parameters:
                   - policy_topic: str
                   - background_context: str
                   - city_data: str
                   - policy_type: str
                   - time_range: str
                   - interests: str
                   - mode: str ("full", "quick", "research_only", "debate_only")
        
        Returns:
            Dictionary with deliberation results
        """
        # Update parameters from inputs
        if inputs:
            self.update_parameters(**inputs)
        
        # Build complete context if using modular inputs
        if self.city_data or self.policy_type or self.time_range or self.interests:
            context_parts = []
            
            if self.city_data:
                context_parts.append(f"City/Region: {self.city_data}")
            if self.policy_type:
                context_parts.append(f"Policy Type: {self.policy_type}")
            if self.time_range:
                context_parts.append(f"Evaluation Timeframe: {self.time_range}")
            if self.interests:
                context_parts.append(f"Key Evaluation Criteria: {self.interests}")
            
            if not self.background_context:
                self.background_context = "\n".join(context_parts)
            else:
                self.background_context += "\n\n" + "\n".join(context_parts)
        
        # Determine execution mode
        mode = inputs.get("mode", "full") if inputs else "full"
        
        if mode == "full":
            return self.run_full_deliberation(self.policy_topic, self.background_context)
        elif mode == "quick":
            return self.run_quick_analysis()
        elif mode == "research_only":
            return self.run_research_only()
        elif mode == "debate_only":
            return self.run_debate_only()
        else:
            return self.run_full_deliberation(self.policy_topic, self.background_context)
    
    def run(self) -> Dict[str, Any]:
        """
        Standard run method for direct execution
        
        Returns:
            Complete deliberation results
        """
        return self.run_full_deliberation(self.policy_topic, self.background_context)
    
    def run_quick_analysis(self) -> Dict[str, Any]:
        """
        Quick analysis mode: Research → Vote → Announce (no debate)
        Faster execution for time-sensitive decisions
        """
        print("\n🚀 QUICK ANALYSIS MODE - Research → Vote → Announce\n")
        
        agents = self.initialize_agents_for_policy(self.policy_topic)
        
        # Quick workflow
        self.run_problem_statement_phase(agents, self.policy_topic, self.background_context)
        research_results = self.run_research_phase(agents, self.policy_topic)
        voting_results = self.run_voting_phase(agents, self.policy_topic)
        final_announcement = self.run_final_announcement(agents, self.policy_topic)
        final_report = self.generate_final_summary_report(self.policy_topic)
        
        return {
            'agents': agents,
            'results': self.deliberation_results,
            'final_report': final_report,
            'mode': 'quick'
        }
    
    def run_research_only(self) -> Dict[str, Any]:
        """
        Research-only mode: Initialize agents and conduct research phase only
        Useful for gathering data before decision-making
        """
        print("\n🔍 RESEARCH ONLY MODE - Data Gathering Phase\n")
        
        agents = self.initialize_agents_for_policy(self.policy_topic)
        self.run_problem_statement_phase(agents, self.policy_topic, self.background_context)
        research_results = self.run_research_phase(agents, self.policy_topic)
        
        return {
            'agents': agents,
            'research': research_results,
            'mode': 'research_only'
        }
    
    def run_debate_only(self) -> Dict[str, Any]:
        """
        Debate-only mode: Assumes research is complete, runs debate and voting
        Useful when research is pre-loaded
        """
        print("\n💬 DEBATE ONLY MODE - Argumentation and Voting\n")
        
        if not self.agents or not self.is_initialized:
            agents = self.initialize_agents_for_policy(self.policy_topic)
        else:
            agents = self.agents
        
        debate_results = self.run_debate_phase(agents, self.policy_topic)
        voting_results = self.run_voting_phase(agents, self.policy_topic)
        final_announcement = self.run_final_announcement(agents, self.policy_topic)
        
        return {
            'agents': agents,
            'debate': debate_results,
            'voting': voting_results,
            'final_announcement': final_announcement,
            'mode': 'debate_only'
        }
    
    def initialize_agents_for_policy(self, policy_topic: str) -> Dict[str, Any]:
        """
        PHASE 1: Initialize all agents for the deliberation
        
        Args:
            policy_topic: The policy being analyzed
            
        Returns:
            Dictionary of agent instances keyed by role
        """
        print("\n" + "="*80)
        print("PHASE 1: INITIALIZATION - AGENT SETUP")
        print("="*80)
        print(f"Policy Topic: {policy_topic}")
        print("\nInitializing expert agents...\n")
        
        agents = {}
        
        # Speaker Experts (Orchestration)
        print("📢 Speaker Experts:")
        agents['problem_statement'] = self.agent_system.problem_statement_expert()
        print("   ✓ Problem Statement Clarification Expert")
        
        agents['turn_management'] = self.agent_system.turn_management_expert()
        print("   ✓ Discussion Turn Management Expert")
        
        agents['voting_announcement'] = self.agent_system.voting_announcement_expert()
        print("   ✓ Voting Coordinator and Results Announcer")
        
        # Core Policy Experts
        print("\n💼 Core Policy Experts:")
        agents['economic'] = self.agent_system.Econimic_agent()
        print("   ✓ Economic Analyst")
        
        agents['social'] = self.agent_system.Social_agent()
        print("   ✓ Social Dynamics Expert")
        
        agents['geospatial'] = self.agent_system.Geospatial_agent()
        print("   ✓ Geospatial Analyst")
        
        agents['income'] = self.agent_system.Income_agents()
        print("   ✓ Income Distribution Analyst")
        
        agents['resource'] = self.agent_system.Resource_agent()
        print("   ✓ Resource Management Expert")
        
        agents['legal'] = self.agent_system.legal_agent()
        print("   ✓ Legal Adviser")
        
        # Economic Experts (MoE)
        print("\n💰 Economic Experts (MoE):")
        agents['economic_macro'] = self.agent_system.macro_economic_expert()
        print("   ✓ Macro-Economic Analysis Expert")
        
        agents['economic_micro'] = self.agent_system.micro_economic_expert()
        print("   ✓ Micro-Economic Analysis Expert")
        
        agents['policy_impact'] = self.agent_system.policy_impact_expert()
        print("   ✓ Policy Impact Analysis Expert")
        
        # Social Welfare Experts (MoE)
        print("\n🏥 Social Welfare Experts (MoE):")
        agents['healthcare_welfare'] = self.agent_system.healthcare_welfare_expert()
        print("   ✓ Healthcare Accessibility Expert")
        
        agents['education_welfare'] = self.agent_system.education_welfare_expert()
        print("   ✓ Education and Skills Development Expert")
        
        agents['housing_welfare'] = self.agent_system.housing_welfare_expert()
        print("   ✓ Housing and Social Safety Net Expert")
        
        # Geospatial & Demographic Experts (MoE)
        print("\n🗺️  Geospatial & Demographic Experts (MoE):")
        agents['geographic_poverty'] = self.agent_system.geographic_poverty_expert()
        print("   ✓ Geographic Poverty Analysis Expert")
        
        agents['demographic_policy'] = self.agent_system.demographic_policy_expert()
        print("   ✓ Demographic-Focused Policy Expert")
        
        agents['resource_access'] = self.agent_system.resource_access_expert()
        print("   ✓ Resource Access and Unemployment Expert")
        
        # Income Inequality Experts (MoE)
        print("\n⚖️  Income Inequality Experts (MoE):")
        agents['inequality_causes'] = self.agent_system.inequality_causes_expert()
        print("   ✓ Income Inequality Causes Expert")
        
        agents['income_redistribution'] = self.agent_system.income_redistribution_expert()
        print("   ✓ Income Redistribution Policy Expert")
        
        agents['inequality_impact'] = self.agent_system.inequality_impact_expert()
        print("   ✓ Inequality Impact Assessment Expert")
        
        # Resource Allocation Experts (MoE)
        print("\n📊 Resource Allocation Experts (MoE):")
        agents['resource_optimization'] = self.agent_system.resource_optimization_expert()
        print("   ✓ Resource Distribution Optimization Expert")
        
        agents['realtime_allocation'] = self.agent_system.realtime_allocation_expert()
        print("   ✓ Real-Time Resource Prioritization Expert")
        
        agents['system_efficiency'] = self.agent_system.system_efficiency_expert()
        print("   ✓ Welfare System Efficiency Expert")
        
        # Feedback & Adaptation Experts (MoE)
        print("\n🔄 Feedback & Adaptation Experts (MoE):")
        agents['policy_monitoring'] = self.agent_system.policy_monitoring_expert()
        print("   ✓ Policy Outcome Monitoring Expert")
        
        agents['adaptive_policy'] = self.agent_system.adaptive_policy_expert()
        print("   ✓ Real-Time Policy Adaptation Expert")
        
        print(f"\n✅ Initialized {len(agents)} expert agents")
        print("="*80 + "\n")
        
        # Store agents and mark as initialized
        self.agents = agents
        self.is_initialized = True
        
        return agents
    
    def run_problem_statement_phase(self, agents: Dict, policy_topic: str, context: str = ""):
        """
        PHASE 2: Problem Statement Clarification
        
        The problem statement expert explains the policy to all agents
        """
        print("\n" + "="*80)
        print("PHASE 2: PROBLEM STATEMENT CLARIFICATION")
        print("="*80)
        print("Expert: Problem Statement Clarification Expert")
        print("Task: Articulate the policy challenge for all agents\n")
        
        task = self.task_system.create_problem_statement_task(
            agents['problem_statement'],
            policy_topic,
            context
        )
        
        crew = Crew(
            agents=[agents['problem_statement']],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        self.deliberation_results['problem_statement'] = result
        
        print("\n✅ Problem Statement Phase Complete")
        print("="*80 + "\n")
        
        return result
    
    def run_turn_management_setup(self, agents: Dict, policy_topic: str):
        """
        PHASE 3: Turn Management Setup
        
        The turn management expert establishes discussion rules and flow
        """
        print("\n" + "="*80)
        print("PHASE 3: DISCUSSION MANAGEMENT SETUP")
        print("="*80)
        print("Expert: Discussion Turn Management Expert")
        print("Task: Establish debate rules and orchestration plan\n")
        
        # Get list of participating experts (exclude speaker experts)
        expert_list = [
            role for role in agents.keys() 
            if role not in ['problem_statement', 'turn_management', 'voting_announcement']
        ]
        
        task = self.task_system.create_turn_management_task(
            agents['turn_management'],
            expert_list,
            policy_topic
        )
        
        crew = Crew(
            agents=[agents['turn_management']],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        self.deliberation_results['turn_management'] = result
        
        print("\n✅ Turn Management Setup Complete")
        print("="*80 + "\n")
        
        return result
    
    def run_research_phase(self, agents: Dict, policy_topic: str):
        """
        PHASE 4: Research Phase - All Experts Conduct Analysis
        
        Each expert researches the policy from their domain perspective
        """
        print("\n" + "="*80)
        print("PHASE 4: RESEARCH PHASE - MULTI-EXPERT ANALYSIS")
        print("="*80)
        print("All domain experts conducting parallel research...\n")
        
        research_results = {}
        
        # Define research groups with their task creators
        research_groups = {
            "Economic Analysis": {
                'economic': self.task_system.create_economic_analysis_task,
                'economic_macro': self.task_system.create_economic_analysis_task,
                'economic_micro': self.task_system.create_economic_analysis_task,
                'policy_impact': self.task_system.create_economic_analysis_task,
            },
            "Social Welfare Analysis": {
                'social': self.task_system.create_social_welfare_task,
                'healthcare_welfare': self.task_system.create_social_welfare_task,
                'education_welfare': self.task_system.create_social_welfare_task,
                'housing_welfare': self.task_system.create_social_welfare_task,
            },
            "Geospatial & Demographic Analysis": {
                'geospatial': self.task_system.create_geospatial_demographic_task,
                'geographic_poverty': self.task_system.create_geospatial_demographic_task,
                'demographic_policy': self.task_system.create_geospatial_demographic_task,
                'resource_access': self.task_system.create_geospatial_demographic_task,
            },
            "Income Inequality Analysis": {
                'income': self.task_system.create_income_inequality_task,
                'inequality_causes': self.task_system.create_income_inequality_task,
                'income_redistribution': self.task_system.create_income_inequality_task,
                'inequality_impact': self.task_system.create_income_inequality_task,
            },
            "Resource Allocation Analysis": {
                'resource': self.task_system.create_resource_allocation_task,
                'resource_optimization': self.task_system.create_resource_allocation_task,
                'realtime_allocation': self.task_system.create_resource_allocation_task,
                'system_efficiency': self.task_system.create_resource_allocation_task,
            },
            "Adaptation & Monitoring Analysis": {
                'policy_monitoring': self.task_system.create_adaptation_feedback_task,
                'adaptive_policy': self.task_system.create_adaptation_feedback_task,
            },
            "Legal Compliance Analysis": {
                'legal': self.task_system.create_legal_compliance_task,
            }
        }
        
        # Run research for each group
        for group_name, group_agents in research_groups.items():
            print(f"\n{'='*80}")
            print(f"Research Group: {group_name}")
            print(f"{'='*80}\n")
            
            group_results = {}
            for role, task_creator in group_agents.items():
                if role in agents:
                    print(f"📝 {role.replace('_', ' ').title()} - Starting research...")
                    
                    task = task_creator(agents[role], policy_topic)
                    crew = Crew(
                        agents=[agents[role]],
                        tasks=[task],
                        process=Process.sequential,
                        verbose=True
                    )
                    
                    result = crew.kickoff()
                    group_results[role] = result
                    research_results[role] = result
                    
                    print(f"✅ {role.replace('_', ' ').title()} - Research complete\n")
            
            print(f"✅ {group_name} Complete\n")
        
        self.deliberation_results['research'] = research_results
        
        print("\n" + "="*80)
        print(f"✅ RESEARCH PHASE COMPLETE - {len(research_results)} Experts Analyzed")
        print("="*80 + "\n")
        
        return research_results
    
    def run_debate_phase(self, agents: Dict, policy_topic: str):
        """
        PHASE 5: Debate Phase - Structured Argumentation
        
        Experts present positions and engage in structured debate
        """
        print("\n" + "="*80)
        print("PHASE 5: DEBATE PHASE - STRUCTURED ARGUMENTATION")
        print("="*80)
        print("Experts presenting positions and engaging in debate...\n")
        
        debate_results = {}
        
        # Get all domain experts (exclude speaker experts)
        domain_experts = [
            role for role in agents.keys() 
            if role not in ['problem_statement', 'turn_management', 'voting_announcement']
        ]
        
        # Run debates
        for role in domain_experts:
            print(f"\n{'='*80}")
            print(f"💬 {role.replace('_', ' ').title()} - Opening Statement & Arguments")
            print(f"{'='*80}\n")
            
            # Create debate task with context from research
            context = "Review the research findings from all experts above."
            task = self.task_system.create_debate_task(
                agents[role],
                policy_topic,
                context
            )
            
            crew = Crew(
                agents=[agents[role]],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            debate_results[role] = result
            
            print(f"\n✅ {role.replace('_', ' ').title()} - Debate contribution complete")
        
        self.deliberation_results['debate'] = debate_results
        
        print("\n" + "="*80)
        print(f"✅ DEBATE PHASE COMPLETE - {len(debate_results)} Expert Contributions")
        print("="*80 + "\n")
        
        return debate_results
    
    def run_voting_phase(self, agents: Dict, policy_topic: str):
        """
        PHASE 6: Voting Phase - Final Decision Making
        
        Each expert casts their vote based on research and debate
        """
        print("\n" + "="*80)
        print("PHASE 6: VOTING PHASE - FINAL DECISION MAKING")
        print("="*80)
        print("Experts casting final votes...\n")
        
        voting_results = {}
        
        # Get all domain experts
        domain_experts = [
            role for role in agents.keys() 
            if role not in ['problem_statement', 'turn_management', 'voting_announcement']
        ]
        
        # Collect votes
        for role in domain_experts:
            print(f"\n{'='*80}")
            print(f"🗳️  {role.replace('_', ' ').title()} - Casting Vote")
            print(f"{'='*80}\n")
            
            # Create voting task
            arguments_summary = "Review all research and debate contributions above."
            task = self.task_system.create_voting_task(
                agents[role],
                policy_topic,
                arguments_summary
            )
            
            crew = Crew(
                agents=[agents[role]],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            voting_results[role] = result
            
            print(f"\n✅ {role.replace('_', ' ').title()} - Vote recorded")
        
        self.deliberation_results['voting'] = voting_results
        
        print("\n" + "="*80)
        print(f"✅ VOTING PHASE COMPLETE - {len(voting_results)} Votes Recorded")
        print("="*80 + "\n")
        
        return voting_results
    
    def run_final_announcement(self, agents: Dict, policy_topic: str):
        """
        PHASE 7: Final Announcement - Vote Tallying & Decision
        
        Voting coordinator tallies votes and announces final decision
        """
        print("\n" + "="*80)
        print("PHASE 7: FINAL ANNOUNCEMENT - DECISION DECLARATION")
        print("="*80)
        print("Expert: Voting Coordinator and Results Announcer")
        print("Task: Tally votes and announce final decision\n")
        
        # Compile all votes for the announcement task
        votes_summary = "Review all votes cast by experts above."
        
        task = self.task_system.create_voting_coordination_task(
            agents['voting_announcement'],
            policy_topic,
            votes_summary
        )
        
        crew = Crew(
            agents=[agents['voting_announcement']],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        self.deliberation_results['final_announcement'] = result
        
        print("\n✅ Final Announcement Complete")
        print("="*80 + "\n")
        
        return result
    
    def generate_final_summary_report(self, policy_topic: str):
        """
        PHASE 8: Generate Comprehensive Summary Report
        
        Compile all results into a final decision document
        """
        print("\n" + "="*80)
        print("PHASE 8: GENERATING FINAL SUMMARY REPORT")
        print("="*80 + "\n")
        
        report = []
        report.append("="*80)
        report.append("POLICY DELIBERATION FINAL REPORT")
        report.append("="*80)
        report.append(f"\nPolicy Topic: {policy_topic}")
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Experts: {len([k for k in self.deliberation_results.get('research', {}).keys()])}")
        report.append("\n" + "="*80)
        
        # Section 1: Problem Statement
        report.append("\n\n📋 SECTION 1: PROBLEM STATEMENT")
        report.append("="*80)
        if 'problem_statement' in self.deliberation_results:
            report.append(str(self.deliberation_results['problem_statement']))
        
        # Section 2: Research Findings Summary
        report.append("\n\n📊 SECTION 2: KEY RESEARCH FINDINGS")
        report.append("="*80)
        if 'research' in self.deliberation_results:
            for role, result in self.deliberation_results['research'].items():
                report.append(f"\n{role.replace('_', ' ').title()}:")
                report.append("-" * 80)
                report.append(str(result)[:500] + "..." if len(str(result)) > 500 else str(result))
        
        # Section 3: Debate Synthesis
        report.append("\n\n💬 SECTION 3: DEBATE SYNTHESIS")
        report.append("="*80)
        if 'debate' in self.deliberation_results:
            report.append(f"\nTotal Debate Contributions: {len(self.deliberation_results['debate'])}")
            report.append("\nKey Arguments Presented:")
            for role, result in self.deliberation_results['debate'].items():
                report.append(f"\n• {role.replace('_', ' ').title()}")
        
        # Section 4: Voting Results
        report.append("\n\n🗳️  SECTION 4: VOTING RESULTS")
        report.append("="*80)
        if 'voting' in self.deliberation_results:
            report.append(f"\nTotal Votes Cast: {len(self.deliberation_results['voting'])}")
            report.append("\nIndividual Votes:")
            for role, result in self.deliberation_results['voting'].items():
                report.append(f"\n{role.replace('_', ' ').title()}:")
                report.append(str(result)[:300] + "..." if len(str(result)) > 300 else str(result))
        
        # Section 5: Final Decision
        report.append("\n\n⚖️  SECTION 5: FINAL DECISION")
        report.append("="*80)
        if 'final_announcement' in self.deliberation_results:
            report.append(str(self.deliberation_results['final_announcement']))
        
        # Section 6: Conclusion
        report.append("\n\n✅ SECTION 6: CONCLUSION")
        report.append("="*80)
        report.append("\nThis comprehensive policy deliberation involved multi-expert analysis,")
        report.append("structured debate, and democratic voting to reach an evidence-based decision.")
        report.append("\n" + "="*80)
        report.append("END OF REPORT")
        report.append("="*80 + "\n")
        
        full_report = "\n".join(report)
        
        # Save report to file
        report_filename = f"policy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(full_report)
        
        print(f"✅ Final report saved to: {report_filename}")
        print("="*80 + "\n")
        
        return full_report
    
    def run_full_deliberation(self, policy_topic: str, background_context: str = ""):
        """
        Execute the complete deliberation workflow
        
        This is the main orchestration method that runs all phases sequentially:
        1. Agent Initialization
        2. Problem Statement
        3. Turn Management Setup
        4. Research Phase
        5. Debate Phase
        6. Voting Phase
        7. Final Announcement
        8. Summary Report Generation
        
        Args:
            policy_topic: The policy to deliberate on
            background_context: Optional background information
            
        Returns:
            Complete deliberation results including final report
        """
        print("\n" + "🚀"*40)
        print("STARTING FULL POLICY DELIBERATION WORKFLOW")
        print("🚀"*40 + "\n")
        
        start_time = datetime.now()
        
        try:
            # Phase 1: Initialize Agents
            agents = self.initialize_agents_for_policy(policy_topic)
            
            # Phase 2: Problem Statement
            problem_result = self.run_problem_statement_phase(agents, policy_topic, background_context)
            
            # Phase 3: Turn Management
            turn_result = self.run_turn_management_setup(agents, policy_topic)
            
            # Phase 4: Research
            research_results = self.run_research_phase(agents, policy_topic)
            
            # Phase 5: Debate
            debate_results = self.run_debate_phase(agents, policy_topic)
            
            # Phase 6: Voting
            voting_results = self.run_voting_phase(agents, policy_topic)
            
            # Phase 7: Final Announcement
            final_announcement = self.run_final_announcement(agents, policy_topic)
            
            # Phase 8: Generate Summary Report
            final_report = self.generate_final_summary_report(policy_topic)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print("\n" + "🎉"*40)
            print("DELIBERATION COMPLETE!")
            print("🎉"*40)
            print(f"\nTotal Duration: {duration:.2f} seconds")
            print(f"Total Experts: {len(agents)}")
            print(f"Research Reports: {len(research_results)}")
            print(f"Debate Contributions: {len(debate_results)}")
            print(f"Votes Cast: {len(voting_results)}")
            print("\n" + "="*80 + "\n")
            
            return {
                'agents': agents,
                'results': self.deliberation_results,
                'final_report': final_report,
                'duration_seconds': duration
            }
            
        except Exception as e:
            print(f"\n❌ ERROR DURING DELIBERATION: {str(e)}")
            import traceback
            traceback.print_exc()
            return None


# ========== MAIN EXECUTION ==========

def interactive_mode():
    """
    Interactive mode with user prompts for policy parameters
    Similar to parliament crew example
    """
    print("\n" + "="*80)
    print("## Welcome to the Auto-Coder Policy Deliberation System")
    print("="*80)
    
    # Gather user inputs
    policy_topic = input(
        dedent("""
        What policy topic would you like to analyze?
        (Press Enter for default: "Poverty Reduction and Economic Outcome in Urban Areas")
        > """)
    ).strip() or "Poverty Reduction and Economic Outcome in Urban Areas"
    
    city_data = input(
        dedent("""
        What city or region is being considered for this policy?
        (e.g., Mumbai, New York, London) (Optional)
        > """)
    ).strip()
    
    policy_type = input(
        dedent("""
        What type of policy is this?
        (e.g., Economic, Social, Environmental, Infrastructure) (Optional)
        > """)
    ).strip()
    
    time_range = input(
        dedent("""
        What is the evaluation timeframe?
        (e.g., 1 year, 5 years, 10 years) (Optional)
        > """)
    ).strip()
    
    interests = input(
        dedent("""
        What are the key evaluation criteria?
        (e.g., economic feasibility, social impact, environmental sustainability) (Optional)
        > """)
    ).strip()
    
    mode = input(
        dedent("""
        Select execution mode:
        1. Full Deliberation (Research → Debate → Vote → Announce)
        2. Quick Analysis (Research → Vote → Announce, no debate)
        3. Research Only (Data gathering only)
        4. Debate Only (Assumes research complete)
        Enter choice (1-4, default: 1): """)
    ).strip() or "1"
    
    mode_map = {
        "1": "full",
        "2": "quick",
        "3": "research_only",
        "4": "debate_only"
    }
    
    execution_mode = mode_map.get(mode, "full")
    
    # Initialize system
    system = AutoPolicyDeliberationSystem(
        policy_topic=policy_topic,
        city_data=city_data,
        policy_type=policy_type,
        time_range=time_range,
        interests=interests
    )
    
    # Execute deliberation
    print(f"\n{'='*80}")
    print(f"Starting {execution_mode.upper()} mode deliberation...")
    print(f"{'='*80}\n")
    
    results = system.kickoff(inputs={"mode": execution_mode})
    
    # Display results
    print("\n\n" + "="*80)
    print("## DELIBERATION COMPLETE")
    print("="*80 + "\n")
    
    if "final_report" in results:
        print("📄 Final Report Generated")
        print(f"Mode: {results.get('mode', 'unknown')}")
        if 'duration_seconds' in results:
            print(f"Duration: {results['duration_seconds']:.2f} seconds")
    
    return results


def register_with_agentverse(system: AutoPolicyDeliberationSystem, 
                             api_token: str,
                             agent_name: str = "AI Policy Deliberation Agent",
                             port: int = 8034,
                             mailbox: bool = True):
    """
    Register the deliberation system with Agentverse using uAgents adapter
    
    Args:
        system: AutoPolicyDeliberationSystem instance
        api_token: Agentverse API token
        agent_name: Name for the registered agent
        port: Port for agent communication
        mailbox: Whether to use mailbox for async communication
    
    Returns:
        Registration result with agent address
    """
    if not UAGENTS_AVAILABLE:
        print("❌ uAgents adapter not available. Cannot register with Agentverse.")
        return None
    
    print(f"\n{'='*80}")
    print("REGISTERING WITH AGENTVERSE")
    print(f"{'='*80}\n")
    
    # Create registration tool
    register_tool = CrewaiRegisterTool()
    
    # Define query parameters schema
    query_params = {
        "policy_topic": {"type": "str", "required": True},
        "background_context": {"type": "str", "required": False},
        "city_data": {"type": "str", "required": False},
        "policy_type": {"type": "str", "required": False},
        "time_range": {"type": "str", "required": False},
        "interests": {"type": "str", "required": False},
        "mode": {"type": "str", "required": False, "default": "full"}
    }
    
    # Example query for documentation
    example_query = dedent("""
    Analyze poverty reduction policies in Mumbai focusing on economic feasibility,
    social impact, and environmental sustainability over a 5-year timeframe.
    Consider both macro and micro-economic factors, geospatial distribution,
    and resource allocation efficiency.
    """).strip()
    
    # Register with Agentverse
    result = register_tool.run(
        tool_input={
            "crew_obj": system,
            "name": agent_name,
            "port": port,
            "description": dedent("""
                Advanced AI-powered policy deliberation system with 26+ expert agents.
                Conducts comprehensive analysis including:
                - Multi-expert research with economic, social, geospatial data
                - Structured debate and argumentation
                - Democratic voting with consensus analysis
                - Final decision announcement with recommendations
                
                Supports multiple execution modes:
                - Full Deliberation (complete workflow)
                - Quick Analysis (fast track without debate)
                - Research Only (data gathering)
                - Debate Only (argumentation and voting)
            """).strip(),
            "api_token": api_token,
            "mailbox": mailbox,
            "query_params": query_params,
            "example_query": example_query,
        }
    )
    
    # Extract agent address
    if isinstance(result, dict) and "address" in result:
        agent_address = result["address"]
        print(f"✅ Successfully registered with Agentverse!")
        print(f"Agent Address: {agent_address}")
        print(f"Agent Name: {agent_name}")
        print(f"Port: {port}")
        print(f"Mailbox: {'Enabled' if mailbox else 'Disabled'}")
    else:
        print(f"⚠️  Registration result: {result}")
    
    print(f"\n{'='*80}\n")
    
    return result


def main():
    """
    Main execution function with multiple modes
    
    Supports:
    1. Interactive mode (user prompts)
    2. Direct execution (programmatic)
    3. Agentverse registration (with API token)
    """
    
    # Load environment variables
    load_dotenv()
    
    # Check for command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Auto-Coder Policy Deliberation System")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Run in interactive mode with user prompts")
    parser.add_argument("--register", "-r", action="store_true",
                       help="Register with Agentverse (requires AV_API_KEY)")
    parser.add_argument("--mode", "-m", choices=["full", "quick", "research", "debate"],
                       default="full", help="Execution mode")
    parser.add_argument("--policy", "-p", type=str,
                       help="Policy topic to analyze")
    parser.add_argument("--port", type=int, default=8034,
                       help="Port for Agentverse registration")
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        return interactive_mode()
    
    # Registration mode
    if args.register:
        api_token = os.getenv("AV_API_KEY")
        if not api_token:
            print("❌ Error: AV_API_KEY not found in environment")
            print("Please set AV_API_KEY in your .env file for Agentverse registration")
            return None
        
        # Create system instance
        system = AutoPolicyDeliberationSystem()
        
        # Register with Agentverse
        result = register_with_agentverse(
            system=system,
            api_token=api_token,
            agent_name="AI Policy Deliberation Multi-Expert System",
            port=args.port,
            mailbox=True
        )
        
        # Keep running for async requests
        if result:
            print("Agent is now running and listening for requests...")
            print("Press Ctrl+C to stop")
            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\nShutting down agent...")
        
        return result
    
    # Direct execution mode
    policy_topic = args.policy or "Poverty Reduction and Economic Outcome in Urban Areas"
    
    background_context = """
    Urban poverty remains a critical challenge affecting millions of people in cities worldwide.
    This policy aims to address:
    
    1. ECONOMIC CHALLENGES:
       - High unemployment rates in urban areas
       - Limited economic mobility for low-income populations
       - Inadequate job creation and skills development
       - Informal economy and lack of social protections
    
    2. SOCIAL CHALLENGES:
       - Limited access to quality education and healthcare
       - Housing affordability crisis
       - Food insecurity and malnutrition
       - Social exclusion and inequality
    
    3. INFRASTRUCTURE CHALLENGES:
       - Inadequate public transportation
       - Limited access to basic services (water, sanitation)
       - Overcrowded and substandard housing
       - Insufficient public spaces and community facilities
    
    4. POLICY OBJECTIVES:
       - Improve economic mobility and income levels
       - Enhance access to education, healthcare, and housing
       - Create sustainable employment opportunities
       - Strengthen social safety nets and support systems
       - Reduce income inequality and wealth gaps
       - Improve urban infrastructure and service delivery
    """
    
    # Initialize system
    system = AutoPolicyDeliberationSystem(
        policy_topic=policy_topic,
        background_context=background_context
    )
    
    # Execute based on mode
    mode_map = {
        "full": "full",
        "quick": "quick",
        "research": "research_only",
        "debate": "debate_only"
    }
    
    execution_mode = mode_map.get(args.mode, "full")
    
    print(f"\nPolicy Topic: {policy_topic}")
    print(f"Execution Mode: {execution_mode.upper()}\n")
    print("Starting automated multi-expert deliberation...\n")
    
    results = system.kickoff(inputs={"mode": execution_mode})
    
    if results:
        print("\n✅ Deliberation completed successfully!")
        if 'final_report' in results:
            print(f"📄 Final report available")
        if 'duration_seconds' in results:
            print(f"⏱️  Total time: {results['duration_seconds']:.2f} seconds")
    else:
        print("\n❌ Deliberation failed. Check error messages above.")
    
    return results


if __name__ == "__main__":
    """
    Run the automated policy deliberation system
    
    Usage Examples:
    ---------------
    
    1. Direct execution (default mode):
       python uagent_main.py
    
    2. Interactive mode with user prompts:
       python uagent_main.py --interactive
       python uagent_main.py -i
    
    3. Quick analysis mode (no debate):
       python uagent_main.py --mode quick
       python uagent_main.py -m quick
    
    4. Research only mode:
       python uagent_main.py --mode research
    
    5. Custom policy topic:
       python uagent_main.py --policy "Universal Basic Income Policy"
       python uagent_main.py -p "Carbon Tax Implementation"
    
    6. Register with Agentverse:
       python uagent_main.py --register
       python uagent_main.py -r --port 8034
    
    7. Combined options:
       python uagent_main.py -i --mode quick
       python uagent_main.py -p "Healthcare Reform" -m research
    
    Execution Modes:
    ----------------
    - full: Complete workflow (Research → Debate → Vote → Announce)
    - quick: Fast track (Research → Vote → Announce, no debate)  
    - research: Research phase only (data gathering)
    - debate: Debate and voting only (assumes research complete)
    
    Requirements:
    -------------
    - ASI_API_KEY: Required for LLM access
    - SERPER_API_KEY: Optional for web searches
    - AV_API_KEY: Required only for Agentverse registration
    """
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║         AUTO-CODER POLICY DELIBERATION SYSTEM v2.0                        ║
    ║         Poverty Reduction and Economic Outcome in Urban Areas             ║
    ║                                                                            ║
    ║  Advanced Features:                                                        ║
    ║  • 26+ Expert Agents (Economic, Social, Geospatial, Income, Resource)    ║
    ║  • Automated Research with Knowledge Base & Web Search                    ║
    ║  • Structured Debate and Democratic Voting                                ║
    ║  • Multiple Execution Modes (Full, Quick, Research, Debate)              ║
    ║  • Interactive Mode with User Prompts                                     ║
    ║  • uAgents/Agentverse Integration                                         ║
    ║  • CrewAI Adapter Compatibility                                           ║
    ║  • Comprehensive Report Generation                                        ║
    ║                                                                            ║
    ║  Usage: python uagent_main.py [--interactive] [--mode MODE]              ║
    ║         python uagent_main.py --help  (for all options)                  ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    results = main()
