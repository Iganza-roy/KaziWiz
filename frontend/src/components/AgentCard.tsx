"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Loader2, CheckCircle2, Circle, Clock, ChevronDown, ChevronUp, Maximize2 } from "lucide-react";
import { useState } from "react";

interface AgentCardProps {
  agent: {
    id: string;
    name: string;
    category: string;
    emoji: string;
  };
  status: "idle" | "working" | "complete" | "error";
  action?: string;
  outputs: { round?: number; phase?: string; content: string; timestamp: Date }[];
  vote?: string;
  progress?: string;
  onViewDetails?: () => void;
}

const CATEGORY_COLORS = {
  orchestration: "bg-purple-500/20 text-purple-300 border-purple-500/30",
  core: "bg-blue-500/20 text-blue-300 border-blue-500/30",
  economic_moe: "bg-green-500/20 text-green-300 border-green-500/30",
  social_moe: "bg-pink-500/20 text-pink-300 border-pink-500/30",
  geospatial_moe: "bg-yellow-500/20 text-yellow-300 border-yellow-500/30",
  income_moe: "bg-orange-500/20 text-orange-300 border-orange-500/30",
  resource_moe: "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
  feedback_moe: "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
};

export default function AgentCard({ agent, status, action, outputs, vote, progress, onViewDetails }: AgentCardProps) {
  const [expanded, setExpanded] = useState(false);
  
  const categoryColor = CATEGORY_COLORS[agent.category as keyof typeof CATEGORY_COLORS] || CATEGORY_COLORS.core;
  const latestOutput = outputs.length > 0 ? outputs[outputs.length - 1] : null;

  const getStatusIcon = () => {
    switch (status) {
      case "working":
        return <Loader2 className="w-4 h-4 animate-spin text-blue-400" />;
      case "complete":
        return <CheckCircle2 className="w-4 h-4 text-green-400" />;
      case "error":
        return <Circle className="w-4 h-4 text-red-400" />;
      default:
        return <Circle className="w-4 h-4 text-slate-500" />;
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case "working":
        return "border-blue-500 bg-blue-500/10";
      case "complete":
        return "border-green-500 bg-green-500/10";
      case "error":
        return "border-red-500 bg-red-500/10";
      default:
        return "border-slate-700 bg-slate-800/30";
    }
  };

  return (
    <Card className={`${getStatusColor()} border transition-all duration-300 hover:shadow-lg`}>
      <CardHeader className="p-4 pb-3">
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center gap-2 flex-1 min-w-0">
            <span className="text-2xl flex-shrink-0">{agent.emoji}</span>
            <div className="flex-1 min-w-0">
              <CardTitle className="text-sm font-semibold text-white truncate">
                {agent.name}
              </CardTitle>
              <Badge
                variant="outline"
                className={`text-xs mt-1 ${categoryColor}`}
              >
                {agent.category.replace(/_/g, " ").replace(" moe", " MoE")}
              </Badge>
            </div>
          </div>
          <div className="flex-shrink-0">
            {getStatusIcon()}
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-4 pt-0 space-y-2">
        {/* Current Action */}
        {action && status === "working" && (
          <div className="text-xs text-slate-400 flex items-center gap-2">
            <Clock className="w-3 h-3 animate-pulse" />
            <span>{action}</span>
          </div>
        )}

        {/* Progress */}
        {progress && (
          <div className="text-xs text-slate-400">
            Progress: {progress}
          </div>
        )}

        {/* Vote */}
        {vote && (
          <div className="bg-slate-900/50 rounded p-2 border border-slate-700">
            <div className="text-xs font-semibold text-blue-400 mb-1">Vote Cast:</div>
            <div className="text-xs text-slate-300">{vote}</div>
          </div>
        )}

        {/* Output (Latest with count badge) */}
        {outputs.length > 0 && (
          <div className="border border-slate-700 rounded-lg overflow-hidden">
            <button
              onClick={() => setExpanded(!expanded)}
              className="w-full flex items-center justify-between p-2 bg-slate-900/50 hover:bg-slate-900/70 transition-colors"
            >
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold text-slate-300">
                  {status === "complete" ? "Results" : "Output"}
                </span>
                <Badge variant="outline" className="text-xs bg-blue-500/20 text-blue-300 border-blue-500/30">
                  {outputs.length} {outputs.length === 1 ? 'result' : 'results'}
                </Badge>
              </div>
              {expanded ? (
                <ChevronUp className="w-4 h-4 text-slate-400" />
              ) : (
                <ChevronDown className="w-4 h-4 text-slate-400" />
              )}
            </button>
            {expanded && (
              <div className="p-2 bg-slate-950/50">
                {/* Latest Output Preview */}
                {latestOutput && (
                  <div className="mb-2">
                    <div className="text-xs text-slate-400 mb-1">
                      Latest {latestOutput.round && `(Round ${latestOutput.round})`}:
                    </div>
                    <div className="p-2 bg-slate-900/50 rounded border border-slate-700 max-h-32 overflow-y-auto">
                      <pre className="text-xs text-slate-300 whitespace-pre-wrap break-words font-mono">
                        {latestOutput.content.substring(0, 200)}
                        {latestOutput.content.length > 200 && '...'}
                      </pre>
                    </div>
                  </div>
                )}
                
                {/* View All Button */}
                {outputs.length > 0 && onViewDetails && (
                  <Button
                    size="sm"
                    variant="outline"
                    className="w-full mt-2 text-xs"
                    onClick={(e) => {
                      e.stopPropagation();
                      onViewDetails();
                    }}
                  >
                    <Maximize2 className="w-3 h-3 mr-1" />
                    View All {outputs.length} Result{outputs.length !== 1 ? 's' : ''}
                  </Button>
                )}
              </div>
            )}
          </div>
        )}

        {/* Status Badge */}
        <div className="pt-1">
          <Badge
            variant="outline"
            className={`text-xs ${
              status === "working"
                ? "bg-blue-500/20 text-blue-300 border-blue-500/30"
                : status === "complete"
                ? "bg-green-500/20 text-green-300 border-green-500/30"
                : status === "error"
                ? "bg-red-500/20 text-red-300 border-red-500/30"
                : "bg-slate-700/20 text-slate-400 border-slate-600/30"
            }`}
          >
            {status.toUpperCase()}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}
