"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Rocket, Users, Zap, BarChart3, Shield, Clock } from "lucide-react";
import { useWebSocket } from "@/hooks/use-websocket";

export default function Home() {
  const router = useRouter();
  const { isConnected, connectionStatus } = useWebSocket();
  const [stats, setStats] = useState({
    totalAgents: 26,
    activeSessions: 0,
    completedPolicies: 0,
  });

  useEffect(() => {
    // Fetch stats from API
    fetch("http://localhost:8000/api/v1/agents")
      .then((res) => res.json())
      .then((data) => {
        setStats((prev) => ({ ...prev, totalAgents: data.agents?.length || 26 }));
      })
      .catch(console.error);
  }, []);

  const startNewDeliberation = () => {
    // Navigate to new policy creation
    router.push("/policy/new");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-500 rounded-lg">
                <Rocket className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">AI Policy Deliberation</h1>
                <p className="text-sm text-slate-400">Multi-Agent Decision System</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Badge variant={isConnected ? "default" : "destructive"}>
                {connectionStatus}
              </Badge>
              <Button onClick={startNewDeliberation} size="lg" className="bg-blue-500 hover:bg-blue-600">
                <Zap className="w-4 h-4 mr-2" />
                New Policy
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-5xl font-bold text-white mb-4">
            Deliberate with <span className="text-blue-400">26 AI Agents</span>
          </h2>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Watch in real-time as specialized agents analyze, debate, and vote on policy proposals with
            SHAP/LIME explainability insights
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-slate-200">Total Agents</CardTitle>
              <Users className="w-4 h-4 text-blue-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">{stats.totalAgents}</div>
              <p className="text-xs text-slate-400 mt-1">Specialized AI agents ready</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-slate-200">Active Sessions</CardTitle>
              <Clock className="w-4 h-4 text-purple-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">{stats.activeSessions}</div>
              <p className="text-xs text-slate-400 mt-1">Deliberations in progress</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-slate-200">Completed</CardTitle>
              <BarChart3 className="w-4 h-4 text-green-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">{stats.completedPolicies}</div>
              <p className="text-xs text-slate-400 mt-1">Policy analyses done</p>
            </CardContent>
          </Card>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card className="bg-gradient-to-br from-blue-500/10 to-blue-500/5 border-blue-500/20">
            <CardHeader>
              <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4">
                <Rocket className="w-6 h-6 text-blue-400" />
              </div>
              <CardTitle className="text-white">Real-Time Streaming</CardTitle>
              <CardDescription className="text-slate-400">
                Watch agents think, debate, and vote as it happens via WebSocket
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="bg-gradient-to-br from-purple-500/10 to-purple-500/5 border-purple-500/20">
            <CardHeader>
              <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4">
                <BarChart3 className="w-6 h-6 text-purple-400" />
              </div>
              <CardTitle className="text-white">SHAP/LIME Analysis</CardTitle>
              <CardDescription className="text-slate-400">
                Understand why agents voted the way they did with explainability charts
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="bg-gradient-to-br from-green-500/10 to-green-500/5 border-green-500/20">
            <CardHeader>
              <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center mb-4">
                <Shield className="w-6 h-6 text-green-400" />
              </div>
              <CardTitle className="text-white">7-Phase Process</CardTitle>
              <CardDescription className="text-slate-400">
                From initiation to final report with comprehensive analysis at each stage
              </CardDescription>
            </CardHeader>
          </Card>
        </div>

        {/* CTA Section */}
        <div className="mt-16 text-center">
          <Card className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 border-blue-500/30 max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className="text-3xl text-white">Ready to Start?</CardTitle>
              <CardDescription className="text-slate-300 text-lg">
                Create a new policy proposal and watch the AI agents deliberate
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button 
                onClick={startNewDeliberation} 
                size="lg" 
                className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-6 text-lg"
              >
                <Rocket className="w-5 h-5 mr-2" />
                Start New Deliberation
              </Button>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
