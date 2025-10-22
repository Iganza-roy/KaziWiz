"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { ArrowLeft, Loader2, CheckCircle2, Circle, Clock, X } from "lucide-react";
import { useWebSocket, useWebSocketEvent } from "@/hooks/use-websocket";
import AgentCard from "@/components/AgentCard";

const PHASES = [
  { id: 1, name: "Initialization", icon: "🚀" },
  { id: 2, name: "Problem Statement", icon: "📝" },
  { id: 3, name: "Research & Analysis", icon: "🔍" },
  { id: 4, name: "Structured Debate", icon: "💬" },
  { id: 5, name: "Democratic Voting", icon: "🗳️" },
  { id: 6, name: "Results Analysis", icon: "📊" },
  { id: 7, name: "Final Report", icon: "🎉" }
];

const ALL_AGENTS = [
  // Orchestration Experts
  { id: "problem_statement", name: "Problem Statement Expert", category: "orchestration", emoji: "📢" },
  { id: "turn_management", name: "Turn Management Expert", category: "orchestration", emoji: "⚖️" },
  { id: "voting_announcement", name: "Voting Coordinator", category: "orchestration", emoji: "🗳️" },
  
  // Core Policy Experts
  { id: "economic", name: "Economic Analyst", category: "core", emoji: "💰" },
  { id: "social", name: "Social Dynamics Expert", category: "core", emoji: "👥" },
  { id: "geospatial", name: "Geospatial Analyst", category: "core", emoji: "🗺️" },
  { id: "income", name: "Income Distribution Analyst", category: "core", emoji: "💵" },
  { id: "resource", name: "Resource Management Expert", category: "core", emoji: "📊" },
  { id: "legal", name: "Legal Adviser", category: "core", emoji: "⚖️" },
  
  // Economic MoE
  { id: "economic_macro", name: "Macro-Economic Expert", category: "economic_moe", emoji: "🌐" },
  { id: "economic_micro", name: "Micro-Economic Expert", category: "economic_moe", emoji: "🏪" },
  { id: "policy_impact", name: "Policy Impact Expert", category: "economic_moe", emoji: "📈" },
  { id: "trade_investment", name: "Trade & Investment Expert", category: "economic_moe", emoji: "🌍" },
  
  // Social Welfare MoE
  { id: "healthcare_welfare", name: "Healthcare Expert", category: "social_moe", emoji: "🏥" },
  { id: "education_welfare", name: "Education Expert", category: "social_moe", emoji: "📚" },
  { id: "housing_welfare", name: "Housing Expert", category: "social_moe", emoji: "🏘️" },
  
  // Geospatial MoE
  { id: "geographic_poverty", name: "Geographic Poverty Expert", category: "geospatial_moe", emoji: "🗺️" },
  { id: "demographic_policy", name: "Demographic Policy Expert", category: "geospatial_moe", emoji: "👨‍👩‍👧‍👦" },
  { id: "resource_access", name: "Resource Access Expert", category: "geospatial_moe", emoji: "🚇" },
  
  // Income Inequality MoE
  { id: "inequality_causes", name: "Inequality Causes Expert", category: "income_moe", emoji: "⚖️" },
  { id: "income_redistribution", name: "Redistribution Policy Expert", category: "income_moe", emoji: "💸" },
  { id: "inequality_impact", name: "Inequality Impact Expert", category: "income_moe", emoji: "📉" },
  
  // Resource Allocation MoE
  { id: "resource_optimization", name: "Resource Optimization Expert", category: "resource_moe", emoji: "🎯" },
  { id: "realtime_allocation", name: "Real-Time Allocation Expert", category: "resource_moe", emoji: "⚡" },
  { id: "system_efficiency", name: "System Efficiency Expert", category: "resource_moe", emoji: "⚙️" },
  
  // Feedback MoE
  { id: "policy_monitoring", name: "Policy Monitoring Expert", category: "feedback_moe", emoji: "📊" },
  { id: "adaptive_policy", name: "Adaptive Policy Expert", category: "feedback_moe", emoji: "🔄" },
];

interface AgentState {
  status: "idle" | "working" | "complete" | "error";
  action?: string;
  outputs: { round?: number; phase?: string; content: string; timestamp: Date }[];
  vote?: string;
  progress?: string;
}

export default function SessionPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.id as string;
  const { isConnected, subscribeToSession } = useWebSocket();

  const [session, setSession] = useState<any>(null);
  const [currentPhase, setCurrentPhase] = useState(0);
  const [currentPhaseName, setCurrentPhaseName] = useState("");
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [agentStates, setAgentStates] = useState<Record<string, AgentState>>({});
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  // Fetch session data
  useEffect(() => {
    const fetchSession = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/policy/session/${sessionId}`);
        if (!response.ok) throw new Error("Session not found");
        const data = await response.json();
        setSession(data);
        setCurrentPhase(data.current_phase);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching session:", error);
        setLoading(false);
      }
    };

    fetchSession();
  }, [sessionId]);

  // Subscribe to WebSocket events
  useEffect(() => {
    if (isConnected && sessionId) {
      subscribeToSession(sessionId);
    }
  }, [isConnected, sessionId, subscribeToSession]);

  // Listen for phase changes
  useWebSocketEvent("phase_changed", (data) => {
    console.log("Phase changed:", data);
    setCurrentPhase(data.phase);
    setEvents(prev => [...prev, { type: "phase_changed", data, timestamp: new Date() }]);
  });

  useWebSocketEvent("phase_started", (data) => {
    console.log("Phase started:", data);
    setCurrentPhase(data.phase);
    setCurrentPhaseName(data.phase_name);
    setEvents(prev => [...prev, { type: "phase_started", data, timestamp: new Date() }]);
  });

  useWebSocketEvent("phase_completed", (data) => {
    console.log("Phase completed:", data);
    setCurrentPhase(data.phase);
    setCurrentPhaseName(data.phase_name);
    setEvents(prev => [...prev, { type: "phase_completed", data, timestamp: new Date() }]);
  });

  useWebSocketEvent("debate_round_started", (data) => {
    console.log("Debate round started:", data);
    setEvents(prev => [...prev, { type: "debate_round_started", data, timestamp: new Date() }]);
  });

  useWebSocketEvent("consensus_check", (data) => {
    console.log("Consensus check:", data);
    setEvents(prev => [...prev, { type: "consensus_check", data, timestamp: new Date() }]);
  });

  useWebSocketEvent("consensus_reached", (data) => {
    console.log("Consensus reached:", data);
    setEvents(prev => [...prev, { type: "consensus_reached", data, timestamp: new Date() }]);
  });

  // Listen for session events
  useWebSocketEvent("session_created", (data) => {
    console.log("Session created:", data);
    setEvents(prev => [...prev, { type: "session_created", data, timestamp: new Date() }]);
  });

  useWebSocketEvent("deliberation_started", (data) => {
    console.log("Deliberation started:", data);
    setEvents(prev => [...prev, { type: "deliberation_started", data, timestamp: new Date() }]);
  });

  useWebSocketEvent("deliberation_complete", (data) => {
    console.log("Deliberation complete:", data);
    setEvents(prev => [...prev, { type: "deliberation_complete", data, timestamp: new Date() }]);
  });

  // Listen for agent events
  useWebSocketEvent("agent_created", (data) => {
    console.log("Agent created:", data);
    setAgentStates(prev => ({
      ...prev,
      [data.agent_id]: { status: "idle", outputs: [] }
    }));
  });

  useWebSocketEvent("agent_started", (data) => {
    console.log("Agent started:", data);
    setAgentStates(prev => ({
      ...prev,
      [data.agent_id]: {
        ...prev[data.agent_id],
        status: "working",
        action: data.action,
        progress: data.progress,
        outputs: prev[data.agent_id]?.outputs || []
      }
    }));
  });

  useWebSocketEvent("agent_completed", (data) => {
    console.log("Agent completed:", data);
    setAgentStates(prev => {
      const existingOutputs = prev[data.agent_id]?.outputs || [];
      return {
        ...prev,
        [data.agent_id]: {
          ...prev[data.agent_id],
          status: "complete",
          outputs: [
            ...existingOutputs,
            {
              round: data.round,
              phase: currentPhaseName,
              content: data.output,
              timestamp: new Date()
            }
          ],
          action: undefined
        }
      };
    });
  });

  useWebSocketEvent("vote_cast", (data) => {
    console.log("Vote cast:", data);
    setAgentStates(prev => ({
      ...prev,
      [data.agent_id]: {
        ...prev[data.agent_id],
        vote: data.vote
      }
    }));
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-400 animate-spin mx-auto mb-4" />
          <p className="text-slate-300 text-lg">Loading session...</p>
        </div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <p className="text-slate-300 text-lg mb-4">Session not found</p>
          <Button onClick={() => router.push("/")}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                onClick={() => router.push("/")}
                className="text-slate-300 hover:text-white"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-white">{session.policy_topic}</h1>
                <p className="text-sm text-slate-400">Session ID: {sessionId.substring(0, 8)}...</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Badge variant={isConnected ? "default" : "destructive"}>
                {isConnected ? "Connected" : "Disconnected"}
              </Badge>
              <Badge variant="outline" className="text-slate-300">
                {session.status}
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Phase Stepper */}
        <Card className="bg-slate-800/50 border-slate-700 mb-6">
          <CardHeader>
            <CardTitle className="text-white">Deliberation Progress</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between gap-2 overflow-x-auto pb-4">
              {PHASES.map((phase, index) => (
                <div key={phase.id} className="flex items-center">
                  <div className="flex flex-col items-center">
                    <div
                      className={`w-12 h-12 rounded-full flex items-center justify-center text-xl ${
                        currentPhase > phase.id
                          ? "bg-green-500 text-white"
                          : currentPhase === phase.id
                          ? "bg-blue-500 text-white animate-pulse"
                          : "bg-slate-700 text-slate-400"
                      }`}
                    >
                      {currentPhase > phase.id ? (
                        <CheckCircle2 className="w-6 h-6" />
                      ) : currentPhase === phase.id ? (
                        <Clock className="w-6 h-6 animate-spin" />
                      ) : (
                        <Circle className="w-6 h-6" />
                      )}
                    </div>
                    <p className="text-xs text-slate-300 mt-2 text-center whitespace-nowrap">
                      {phase.icon} {phase.name}
                    </p>
                  </div>
                  {index < PHASES.length - 1 && (
                    <div
                      className={`w-16 h-1 mx-2 ${
                        currentPhase > phase.id ? "bg-green-500" : "bg-slate-700"
                      }`}
                    />
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Agent Grid - 26 Agents */}
        <Card className="bg-slate-800/50 border-slate-700 mb-6">
          <CardHeader>
            <CardTitle className="text-white">Expert Agents ({ALL_AGENTS.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {ALL_AGENTS.map((agent) => (
                <AgentCard
                  key={agent.id}
                  agent={agent}
                  status={agentStates[agent.id]?.status || "idle"}
                  action={agentStates[agent.id]?.action}
                  outputs={agentStates[agent.id]?.outputs || []}
                  vote={agentStates[agent.id]?.vote}
                  progress={agentStates[agent.id]?.progress}
                  onViewDetails={() => setSelectedAgent(agent.id)}
                />
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Activity Feed */}
        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white">Activity Feed</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {events.length === 0 ? (
                <p className="text-slate-400 text-center py-8">
                  Waiting for deliberation events...
                </p>
              ) : (
                events.map((event, index) => {
                  const getEventIcon = (type: string) => {
                    switch (type) {
                      case 'phase_started': return '🚀';
                      case 'phase_completed': return '✅';
                      case 'debate_round_started': return '💬';
                      case 'consensus_check': return '📊';
                      case 'consensus_reached': return '🎯';
                      case 'deliberation_started': return '🏁';
                      case 'deliberation_complete': return '🎉';
                      default: return '📝';
                    }
                  };

                  const getEventMessage = (event: any) => {
                    switch (event.type) {
                      case 'phase_started':
                        return `${event.data.phase_name} phase started: ${event.data.message}`;
                      case 'phase_completed':
                        return `${event.data.phase_name} phase completed`;
                      case 'debate_round_started':
                        return `Debate Round ${event.data.round}/${event.data.total_rounds}: ${event.data.message}`;
                      case 'consensus_check':
                        return `Consensus Check (Round ${event.data.round}): ${event.data.consensus_level}% agreement - ${event.data.message}`;
                      case 'consensus_reached':
                        return `🎯 ${event.data.message} (Round ${event.data.round})`;
                      case 'deliberation_started':
                        return `Deliberation started on: ${event.data.policy_topic}`;
                      case 'deliberation_complete':
                        return `Deliberation completed in ${event.data.duration_seconds}s with ${event.data.total_agents} agents`;
                      default:
                        return event.type;
                    }
                  };

                  return (
                    <div
                      key={index}
                      className={`p-4 rounded-lg border ${
                        event.type === 'consensus_reached' 
                          ? 'bg-green-900/20 border-green-600'
                          : event.type.includes('phase')
                          ? 'bg-blue-900/20 border-blue-600'
                          : event.type.includes('debate')
                          ? 'bg-purple-900/20 border-purple-600'
                          : 'bg-slate-900/50 border-slate-600'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <span className="text-xl">{getEventIcon(event.type)}</span>
                          <Badge variant="outline" className="text-blue-400">
                            {event.type.replace(/_/g, ' ')}
                          </Badge>
                        </div>
                        <span className="text-xs text-slate-500">
                          {event.timestamp.toLocaleTimeString()}
                        </span>
                      </div>
                      <p className="text-sm text-slate-200 font-medium">
                        {getEventMessage(event)}
                      </p>
                    </div>
                  );
                })
              )}
            </div>
          </CardContent>
        </Card>
      </main>

      {/* Agent Details Modal */}
      <Dialog open={selectedAgent !== null} onOpenChange={(open: boolean) => !open && setSelectedAgent(null)}>
        <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-3 text-2xl">
              {selectedAgent && (
                <>
                  <span className="text-3xl">
                    {ALL_AGENTS.find(a => a.id === selectedAgent)?.emoji}
                  </span>
                  <span>
                    {ALL_AGENTS.find(a => a.id === selectedAgent)?.name}
                  </span>
                </>
              )}
            </DialogTitle>
            <DialogDescription className="text-slate-400">
              All outputs and results from this agent
            </DialogDescription>
          </DialogHeader>

          {selectedAgent && agentStates[selectedAgent] && (
            <div className="space-y-4 mt-4">
              {/* Agent Info */}
              <div className="flex items-center gap-4 p-4 bg-slate-800/50 rounded-lg border border-slate-700">
                <Badge variant="outline" className="text-sm">
                  {ALL_AGENTS.find(a => a.id === selectedAgent)?.category.replace(/_/g, ' ')}
                </Badge>
                <Badge
                  variant="outline"
                  className={`text-sm ${
                    agentStates[selectedAgent].status === "complete"
                      ? "bg-green-500/20 text-green-300"
                      : agentStates[selectedAgent].status === "working"
                      ? "bg-blue-500/20 text-blue-300"
                      : "bg-slate-500/20 text-slate-300"
                  }`}
                >
                  {agentStates[selectedAgent].status.toUpperCase()}
                </Badge>
                {agentStates[selectedAgent].vote && (
                  <Badge variant="outline" className="text-sm bg-purple-500/20 text-purple-300">
                    Vote Cast
                  </Badge>
                )}
              </div>

              {/* Vote */}
              {agentStates[selectedAgent].vote && (
                <div className="p-4 bg-purple-900/20 rounded-lg border border-purple-600">
                  <h3 className="text-lg font-semibold mb-2 text-purple-300">🗳️ Vote</h3>
                  <p className="text-slate-200">{agentStates[selectedAgent].vote}</p>
                </div>
              )}

              {/* All Outputs */}
              <div className="space-y-3">
                <h3 className="text-lg font-semibold text-slate-200">
                  📝 All Results ({agentStates[selectedAgent].outputs.length})
                </h3>
                
                {agentStates[selectedAgent].outputs.length === 0 ? (
                  <p className="text-slate-400 text-center py-8">No outputs yet</p>
                ) : (
                  agentStates[selectedAgent].outputs.map((output, index) => (
                    <div
                      key={index}
                      className="p-4 bg-slate-800/50 rounded-lg border border-slate-700"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <Badge variant="outline" className="text-xs bg-blue-500/20 text-blue-300">
                            Result #{index + 1}
                          </Badge>
                          {output.round && (
                            <Badge variant="outline" className="text-xs bg-purple-500/20 text-purple-300">
                              Round {output.round}
                            </Badge>
                          )}
                          {output.phase && (
                            <Badge variant="outline" className="text-xs bg-green-500/20 text-green-300">
                              {output.phase}
                            </Badge>
                          )}
                        </div>
                        <span className="text-xs text-slate-500">
                          {output.timestamp.toLocaleTimeString()}
                        </span>
                      </div>
                      <div className="p-3 bg-slate-950/50 rounded border border-slate-700 max-h-96 overflow-y-auto">
                        <pre className="text-sm text-slate-300 whitespace-pre-wrap break-words font-mono">
                          {output.content}
                        </pre>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
