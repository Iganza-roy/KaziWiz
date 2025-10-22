"""
Integrated Policy Deliberation System with WebSocket Event Streaming
Connects real AI agents to the web application for live visualization
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from crewai import Crew, Process
import logging

from .agent_system import DecisionAgentSystem
from .task_system import AgentTaskSystem
from .output_validator import OutputValidator

logger = logging.getLogger(__name__)


class IntegratedDeliberationSystem:
    """
    Real-time policy deliberation system with WebSocket event streaming
    Manages 26+ expert agents through all deliberation phases
    """
    
    def __init__(self, event_emitter: Optional[Callable] = None):
        """
        Initialize the deliberation system
        
        Args:
            event_emitter: Async function to emit WebSocket events
                          signature: async def emit(event: str, data: dict, session_id: str)
        """
        self.agent_system = DecisionAgentSystem()
        self.task_system = AgentTaskSystem()
        self.event_emitter = event_emitter
        self.agents = {}
        self.results = {}
        
        logger.info("🚀 Integrated Deliberation System initialized")
    
    async def emit_event(self, event: str, data: dict, session_id: str):
        """Emit WebSocket event if emitter is available"""
        if self.event_emitter:
            try:
                logger.info(f"🔔 Emitting '{event}' to session {session_id}")
                await self.event_emitter(event, data, session_id)
                logger.info(f"✅ Emitted '{event}' successfully")
            except Exception as e:
                logger.error(f"❌ Error emitting event {event}: {e}", exc_info=True)
        else:
            logger.warning(f"⚠️ No event emitter - cannot emit '{event}'")
    
    async def run_deliberation(
        self,
        session_id: str,
        policy_topic: str,
        background_context: str = ""
    ) -> Dict[str, Any]:
        """
        Execute complete deliberation workflow with real-time event streaming
        
        Phases:
        1. Initialization - Setup all agents
        2. Problem Statement - Clarify the policy challenge
        3. Research - All experts conduct analysis (26 agents)
        4. Debate - Structured argumentation (23 agents)
        5. Voting - Democratic decision making (23 agents)
        6. Results - Tally votes and announce decision
        7. Final Report - Generate comprehensive summary
        """
        start_time = datetime.now()
        
        try:
            # PHASE 1: Initialization
            await self.emit_event('phase_started', {
                'phase': 1,
                'phase_name': 'Initialization',
                'message': 'Initializing all expert agents...'
            }, session_id)
            
            agents = await self.initialize_agents(session_id)
            
            await self.emit_event('phase_completed', {
                'phase': 1,
                'phase_name': 'Initialization',
                'agent_count': len(agents)
            }, session_id)
            
            # PHASE 2: Problem Statement
            await self.phase_problem_statement(session_id, agents, policy_topic, background_context)
            
            # PHASE 3: Research
            await self.phase_research(session_id, agents, policy_topic)
            
            # PHASE 4: Debate
            await self.phase_debate(session_id, agents, policy_topic)
            
            # PHASE 5: Voting
            await self.phase_voting(session_id, agents, policy_topic)
            
            # PHASE 6: Results
            await self.phase_results(session_id, agents, policy_topic)
            
            # PHASE 7: Final Report
            await self.phase_final_report(session_id, policy_topic)
            
            duration = (datetime.now() - start_time).total_seconds()
            
            await self.emit_event('deliberation_complete', {
                'session_id': session_id,
                'duration_seconds': duration,
                'total_agents': len(agents),
                'final_decision': self.results.get('final_decision', 'Unknown')
            }, session_id)
            
            return {
                'success': True,
                'duration': duration,
                'results': self.results
            }
            
        except Exception as e:
            logger.error(f"Deliberation error: {e}", exc_info=True)
            await self.emit_event('deliberation_error', {
                'error': str(e),
                'phase': 'Unknown'
            }, session_id)
            return {
                'success': False,
                'error': str(e)
            }
    
    async def initialize_agents(self, session_id: str) -> Dict[str, Any]:
        """Phase 1: Initialize all 26+ expert agents"""
        agents = {}
        agent_definitions = self.agent_system.get_all_agent_definitions()
        
        # Mapping of agent IDs to method names
        method_map = {
            # Orchestration
            "problem_statement": "problem_statement_expert",
            "turn_management": "turn_management_expert",
            "voting_announcement": "voting_announcement_expert",
            
            # Core
            "economic": "economic_agent",
            "social": "social_agent",
            "geospatial": "geospatial_agent",
            "income": "income_agent",
            "resource": "resource_agent",
            "legal": "legal_agent",
            
            # Economic MoE
            "economic_macro": "macro_economic_expert",
            "economic_micro": "micro_economic_expert",
            "policy_impact": "policy_impact_expert",
            "trade_investment": "trade_investment_expert",
            
            # Social MoE
            "healthcare_welfare": "healthcare_welfare_expert",
            "education_welfare": "education_welfare_expert",
            "housing_welfare": "housing_welfare_expert",
            
            # Geospatial MoE
            "geographic_poverty": "geographic_poverty_expert",
            "demographic_policy": "demographic_policy_expert",
            "resource_access": "resource_access_expert",
            
            # Income MoE
            "inequality_causes": "inequality_causes_expert",
            "income_redistribution": "income_redistribution_expert",
            "inequality_impact": "inequality_impact_expert",
            
            # Resource MoE
            "resource_optimization": "resource_optimization_expert",
            "realtime_allocation": "realtime_allocation_expert",
            "system_efficiency": "system_efficiency_expert",
            
            # Feedback MoE
            "policy_monitoring": "policy_monitoring_expert",
            "adaptive_policy": "adaptive_policy_expert",
        }
        
        for agent_def in agent_definitions:
            agent_id = agent_def['id']
            
            # Emit agent creation event
            await self.emit_event('agent_created', {
                'agent_id': agent_id,
                'agent_name': agent_def['name'],
                'category': agent_def['category'],
                'status': 'initialized'
            }, session_id)
            
            # Create agent instance using method map
            method_name = method_map.get(agent_id)
            if method_name and hasattr(self.agent_system, method_name):
                agents[agent_id] = getattr(self.agent_system, method_name)()
            else:
                logger.warning(f"No method found for agent {agent_id}")
        
        self.agents = agents
        logger.info(f"✅ Initialized {len(agents)} agents")
        return agents
    
    async def phase_problem_statement(
        self,
        session_id: str,
        agents: Dict,
        policy_topic: str,
        context: str
    ):
        """Phase 2: Problem Statement Clarification"""
        await self.emit_event('phase_started', {
            'phase': 2,
            'phase_name': 'Problem Statement',
            'message': 'Clarifying the policy challenge...'
        }, session_id)
        
        agent = agents['problem_statement']
        await self.emit_event('agent_started', {
            'agent_id': 'problem_statement',
            'agent_name': 'Problem Statement Expert',
            'action': 'clarifying problem'
        }, session_id)
        
        task = self.task_system.create_problem_statement_task(agent, policy_topic, context)
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        # Run in thread pool to avoid blocking
        result = await asyncio.to_thread(crew.kickoff)
        result_str = str(result)
        
        # Validate output to prevent code hallucinations
        is_valid, reason = OutputValidator.is_valid_policy_output(result_str)
        if not is_valid:
            logger.warning(f"⚠️ Invalid output detected ({reason}), using fallback")
            result_str = OutputValidator.create_fallback_response(
                "Problem Statement Expert",
                policy_topic
            )
        else:
            # Try to clean up any code remnants
            result_str = OutputValidator.extract_policy_content(result_str)
        
        self.results['problem_statement'] = result_str
        
        await self.emit_event('agent_completed', {
            'agent_id': 'problem_statement',
            'output': str(result)[:500]  # Truncate for WebSocket
        }, session_id)
        
        await self.emit_event('phase_completed', {
            'phase': 2,
            'phase_name': 'Problem Statement'
        }, session_id)
    
    async def phase_research(self, session_id: str, agents: Dict, policy_topic: str):
        """Phase 3: Research Phase - All experts conduct analysis"""
        await self.emit_event('phase_started', {
            'phase': 3,
            'phase_name': 'Research & Analysis',
            'message': 'All experts conducting research...',
            'total_agents': len([a for a in agents if a not in ['problem_statement', 'turn_management', 'voting_announcement']])
        }, session_id)
        
        research_groups = {
            "Economic Analysis": ['economic', 'economic_macro', 'economic_micro', 'policy_impact', 'trade_investment'],
            "Social Welfare": ['social', 'healthcare_welfare', 'education_welfare', 'housing_welfare'],
            "Geospatial": ['geospatial', 'geographic_poverty', 'demographic_policy', 'resource_access'],
            "Income Inequality": ['income', 'inequality_causes', 'income_redistribution', 'inequality_impact'],
            "Resource Management": ['resource', 'resource_optimization', 'realtime_allocation', 'system_efficiency'],
            "Adaptation": ['policy_monitoring', 'adaptive_policy'],
            "Legal": ['legal']
        }
        
        research_results = {}
        completed_count = 0
        total_count = sum(len(group) for group in research_groups.values())
        
        for group_name, agent_ids in research_groups.items():
            for agent_id in agent_ids:
                if agent_id not in agents:
                    continue
                
                await self.emit_event('agent_started', {
                    'agent_id': agent_id,
                    'agent_name': agent_id.replace('_', ' ').title(),
                    'action': 'conducting research',
                    'group': group_name
                }, session_id)
                
                # Create appropriate task based on group
                if 'economic' in agent_id.lower():
                    task = self.task_system.create_economic_analysis_task(agents[agent_id], policy_topic)
                elif 'social' in agent_id.lower() or 'healthcare' in agent_id.lower() or 'education' in agent_id.lower() or 'housing' in agent_id.lower():
                    task = self.task_system.create_social_welfare_task(agents[agent_id], policy_topic)
                elif 'geo' in agent_id.lower() or 'demographic' in agent_id.lower():
                    task = self.task_system.create_geospatial_demographic_task(agents[agent_id], policy_topic)
                elif 'income' in agent_id.lower() or 'inequality' in agent_id.lower():
                    task = self.task_system.create_income_inequality_task(agents[agent_id], policy_topic)
                elif 'resource' in agent_id.lower() or 'allocation' in agent_id.lower() or 'efficiency' in agent_id.lower():
                    task = self.task_system.create_resource_allocation_task(agents[agent_id], policy_topic)
                elif 'monitoring' in agent_id.lower() or 'adaptive' in agent_id.lower():
                    task = self.task_system.create_adaptation_feedback_task(agents[agent_id], policy_topic)
                elif 'legal' in agent_id.lower():
                    task = self.task_system.create_legal_compliance_task(agents[agent_id], policy_topic)
                else:
                    task = self.task_system.create_research_task(agents[agent_id], policy_topic, agent_id.replace('_', ' ').title())
                
                crew = Crew(agents=[agents[agent_id]], tasks=[task], process=Process.sequential, verbose=False)
                result = await asyncio.to_thread(crew.kickoff)
                result_str = str(result)
                
                # Validate output to prevent code hallucinations
                is_valid, reason = OutputValidator.is_valid_policy_output(result_str)
                if not is_valid:
                    logger.warning(f"⚠️ Agent {agent_id} generated invalid output ({reason}), using fallback")
                    result_str = OutputValidator.create_fallback_response(
                        agent_id.replace('_', ' ').title(),
                        policy_topic
                    )
                else:
                    result_str = OutputValidator.extract_policy_content(result_str)
                
                research_results[agent_id] = result_str
                completed_count += 1
                
                await self.emit_event('agent_completed', {
                    'agent_id': agent_id,
                    'output': str(result)[:500],
                    'progress': f"{completed_count}/{total_count}"
                }, session_id)
        
        self.results['research'] = research_results
        
        await self.emit_event('phase_completed', {
            'phase': 3,
            'phase_name': 'Research & Analysis',
            'completed_agents': completed_count
        }, session_id)
    
    async def phase_debate(self, session_id: str, agents: Dict, policy_topic: str):
        """Phase 4: Dynamic Debate Phase - Agents respond to each other until consensus"""
        await self.emit_event('phase_started', {
            'phase': 4,
            'phase_name': 'Structured Debate',
            'message': 'Experts engaging in dynamic debate...'
        }, session_id)
        
        domain_experts = [
            a for a in agents.keys()
            if a not in ['problem_statement', 'turn_management', 'voting_announcement']
        ]
        
        # Multi-round debate until consensus or max rounds
        max_rounds = 3
        debate_history = []
        consensus_reached = False
        
        for round_num in range(1, max_rounds + 1):
            await self.emit_event('debate_round_started', {
                'round': round_num,
                'total_rounds': max_rounds,
                'message': f'Round {round_num}: Agents presenting arguments and rebuttals...'
            }, session_id)
            
            round_arguments = {}
            
            for i, agent_id in enumerate(domain_experts):
                await self.emit_event('agent_started', {
                    'agent_id': agent_id,
                    'agent_name': agent_id.replace('_', ' ').title(),
                    'action': f'debating (Round {round_num})',
                    'progress': f"Round {round_num}: {i+1}/{len(domain_experts)}"
                }, session_id)
                
                # Build context from previous arguments
                context = self._build_debate_context(debate_history, round_num, agent_id)
                
                # Create task with previous arguments as context
                task_description = f"""
                **Round {round_num} Debate on: {policy_topic}**
                
                Previous Arguments from Other Experts:
                {context}
                
                Your Task:
                1. Consider the arguments presented by other experts above
                2. Identify points of agreement and disagreement
                3. Present YOUR perspective on {policy_topic}
                4. Respond to arguments you disagree with (provide counter-arguments)
                5. Build upon arguments you agree with (provide supporting evidence)
                6. Propose synthesis or compromise positions where appropriate
                
                Be specific, evidence-based, and engage directly with others' points.
                """
                
                from crewai import Task
                task = Task(
                    description=task_description,
                    agent=agents[agent_id],
                    expected_output=f"Detailed argument with responses to other experts' points"
                )
                
                crew = Crew(
                    agents=[agents[agent_id]], 
                    tasks=[task], 
                    process=Process.sequential, 
                    verbose=False
                )
                result = await asyncio.to_thread(crew.kickoff)
                
                argument = str(result)
                round_arguments[agent_id] = argument
                
                # Add to debate history
                debate_history.append({
                    'round': round_num,
                    'agent_id': agent_id,
                    'agent_name': agent_id.replace('_', ' ').title(),
                    'argument': argument
                })
                
                await self.emit_event('agent_completed', {
                    'agent_id': agent_id,
                    'output': argument[:500],
                    'round': round_num
                }, session_id)
            
            # Check for consensus after each round
            if round_num < max_rounds:
                consensus_level = await self._assess_consensus(session_id, round_arguments, agents)
                
                await self.emit_event('consensus_check', {
                    'round': round_num,
                    'consensus_level': consensus_level,
                    'message': f'Consensus level: {consensus_level}% - {"Continuing debate..." if consensus_level < 70 else "High agreement reached!"}'
                }, session_id)
                
                if consensus_level >= 70:
                    consensus_reached = True
                    await self.emit_event('consensus_reached', {
                        'round': round_num,
                        'message': 'Strong consensus reached among experts!'
                    }, session_id)
                    break
        
        self.results['debate'] = {
            'history': debate_history,
            'rounds': round_num,
            'consensus_reached': consensus_reached
        }
        
        await self.emit_event('phase_completed', {
            'phase': 4,
            'phase_name': 'Structured Debate',
            'total_rounds': round_num,
            'consensus_reached': consensus_reached
        }, session_id)
    
    def _build_debate_context(self, debate_history: list, current_round: int, current_agent: str) -> str:
        """Build context from previous debate rounds"""
        if not debate_history:
            return "No previous arguments yet. You are among the first to speak."
        
        # Get arguments from previous round or earlier in current round
        relevant_args = [
            arg for arg in debate_history 
            if arg['round'] < current_round or (arg['round'] == current_round and arg['agent_id'] != current_agent)
        ]
        
        if not relevant_args:
            return "No previous arguments in this round yet."
        
        # Format last 5 arguments for context
        context_parts = []
        for arg in relevant_args[-5:]:
            context_parts.append(f"""
            **{arg['agent_name']} (Round {arg['round']}):**
            {arg['argument'][:300]}...
            """)
        
        return "\n".join(context_parts)
    
    async def _assess_consensus(self, session_id: str, round_arguments: dict, agents: dict) -> int:
        """Assess consensus level among agents (0-100%)"""
        # Simple heuristic: Check for agreement keywords and sentiment similarity
        # In production, you'd use NLP/LLM to analyze semantic similarity
        
        agreement_keywords = ['agree', 'support', 'concur', 'consensus', 'aligned', 'correct']
        disagreement_keywords = ['disagree', 'oppose', 'against', 'however', 'but', 'contrary']
        
        total_score = 0
        for argument in round_arguments.values():
            arg_lower = argument.lower()
            agreement_count = sum(1 for kw in agreement_keywords if kw in arg_lower)
            disagreement_count = sum(1 for kw in disagreement_keywords if kw in arg_lower)
            
            # Score based on agreement vs disagreement ratio
            if agreement_count + disagreement_count > 0:
                score = (agreement_count / (agreement_count + disagreement_count)) * 100
                total_score += score
        
        consensus_level = int(total_score / len(round_arguments)) if round_arguments else 0
        return min(max(consensus_level, 0), 100)  # Clamp to 0-100
    
    async def phase_voting(self, session_id: str, agents: Dict, policy_topic: str):
        """Phase 5: Voting Phase - Democratic decision making"""
        await self.emit_event('phase_started', {
            'phase': 5,
            'phase_name': 'Democratic Voting',
            'message': 'Experts casting votes...'
        }, session_id)
        
        domain_experts = [
            a for a in agents.keys()
            if a not in ['problem_statement', 'turn_management', 'voting_announcement']
        ]
        
        voting_results = {}
        for i, agent_id in enumerate(domain_experts):
            await self.emit_event('agent_started', {
                'agent_id': agent_id,
                'agent_name': agent_id.replace('_', ' ').title(),
                'action': 'voting',
                'progress': f"{i+1}/{len(domain_experts)}"
            }, session_id)
            
            task = self.task_system.create_voting_task(agents[agent_id], policy_topic)
            crew = Crew(agents=[agents[agent_id]], tasks=[task], process=Process.sequential, verbose=False)
            result = await asyncio.to_thread(crew.kickoff)
            
            voting_results[agent_id] = str(result)
            
            await self.emit_event('vote_cast', {
                'agent_id': agent_id,
                'vote': str(result)[:200]
            }, session_id)
            
            await self.emit_event('agent_completed', {
                'agent_id': agent_id,
                'output': str(result)[:500]
            }, session_id)
        
        self.results['voting'] = voting_results
        
        await self.emit_event('phase_completed', {
            'phase': 5,
            'phase_name': 'Democratic Voting',
            'total_votes': len(voting_results)
        }, session_id)
    
    async def phase_results(self, session_id: str, agents: Dict, policy_topic: str):
        """Phase 6: Results Analysis and Announcement"""
        await self.emit_event('phase_started', {
            'phase': 6,
            'phase_name': 'Results Analysis',
            'message': 'Tallying votes and analyzing results...'
        }, session_id)
        
        agent = agents['voting_announcement']
        await self.emit_event('agent_started', {
            'agent_id': 'voting_announcement',
            'agent_name': 'Voting Coordinator',
            'action': 'announcing results'
        }, session_id)
        
        task = self.task_system.create_voting_coordination_task(agent, policy_topic, "Review all votes above")
        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
        result = await asyncio.to_thread(crew.kickoff)
        
        self.results['final_announcement'] = str(result)
        
        # Try to extract decision
        result_str = str(result).upper()
        if 'APPROVED' in result_str or 'APPROVE' in result_str:
            final_decision = 'APPROVED'
        elif 'REJECTED' in result_str or 'REJECT' in result_str:
            final_decision = 'REJECTED'
        else:
            final_decision = 'CONDITIONAL'
        
        self.results['final_decision'] = final_decision
        
        await self.emit_event('results_announced', {
            'decision': final_decision,
            'announcement': str(result)[:500]
        }, session_id)
        
        await self.emit_event('phase_completed', {
            'phase': 6,
            'phase_name': 'Results Analysis',
            'final_decision': final_decision
        }, session_id)
    
    async def phase_final_report(self, session_id: str, policy_topic: str):
        """Phase 7: Final Report Generation"""
        await self.emit_event('phase_started', {
            'phase': 7,
            'phase_name': 'Final Report',
            'message': 'Generating comprehensive report...'
        }, session_id)
        
        # Generate summary report
        report = {
            'policy_topic': policy_topic,
            'timestamp': datetime.now().isoformat(),
            'problem_statement': self.results.get('problem_statement', ''),
            'research_count': len(self.results.get('research', {})),
            'debate_count': len(self.results.get('debate', {})),
            'votes_count': len(self.results.get('voting', {})),
            'final_decision': self.results.get('final_decision', 'Unknown'),
            'final_announcement': self.results.get('final_announcement', '')
        }
        
        self.results['final_report'] = report
        
        await self.emit_event('report_generated', {
            'report': report
        }, session_id)
        
        await self.emit_event('phase_completed', {
            'phase': 7,
            'phase_name': 'Final Report'
        }, session_id)
