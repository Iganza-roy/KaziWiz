"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, Rocket, Loader2 } from "lucide-react";

export default function NewPolicyPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    policy_topic: "",
    background_context: "",
    city_data: "",
    policy_type: "",
    time_range: "",
    interests: ""
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Create policy session
      const response = await fetch("http://localhost:8000/api/v1/policy/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error("Failed to create policy session");
      }

      const data = await response.json();
      
      // Start deliberation
      await fetch(`http://localhost:8000/api/v1/policy/start/${data.session_id}`, {
        method: "POST",
      });

      // Redirect to session viewer
      router.push(`/session/${data.session_id}`);
    } catch (error) {
      console.error("Error creating policy:", error);
      alert("Failed to create policy session. Please try again.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
        <div className="container mx-auto px-4 py-4">
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
              <h1 className="text-2xl font-bold text-white">Create New Policy</h1>
              <p className="text-sm text-slate-400">Start a new multi-agent deliberation</p>
            </div>
          </div>
        </div>
      </header>

      {/* Form */}
      <main className="container mx-auto px-4 py-12">
        <div className="max-w-3xl mx-auto">
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">Policy Details</CardTitle>
              <CardDescription className="text-slate-400">
                Provide information about the policy you want to analyze
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Policy Topic */}
                <div>
                  <label htmlFor="policy_topic" className="block text-sm font-medium text-slate-200 mb-2">
                    Policy Topic *
                  </label>
                  <input
                    type="text"
                    id="policy_topic"
                    required
                    value={formData.policy_topic}
                    onChange={(e) => setFormData({ ...formData, policy_topic: e.target.value })}
                    placeholder="e.g., Universal Basic Income in San Francisco"
                    className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                {/* Background Context */}
                <div>
                  <label htmlFor="background_context" className="block text-sm font-medium text-slate-200 mb-2">
                    Background Context *
                  </label>
                  <textarea
                    id="background_context"
                    required
                    value={formData.background_context}
                    onChange={(e) => setFormData({ ...formData, background_context: e.target.value })}
                    placeholder="Provide detailed context about the policy, its goals, and current situation..."
                    rows={6}
                    className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  />
                </div>

                {/* Optional Fields */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="policy_type" className="block text-sm font-medium text-slate-200 mb-2">
                      Policy Type
                    </label>
                    <select
                      id="policy_type"
                      value={formData.policy_type}
                      onChange={(e) => setFormData({ ...formData, policy_type: e.target.value })}
                      className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Select type...</option>
                      <option value="Economic">Economic</option>
                      <option value="Social">Social</option>
                      <option value="Environmental">Environmental</option>
                      <option value="Healthcare">Healthcare</option>
                      <option value="Education">Education</option>
                      <option value="Infrastructure">Infrastructure</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor="time_range" className="block text-sm font-medium text-slate-200 mb-2">
                      Time Range
                    </label>
                    <input
                      type="text"
                      id="time_range"
                      value={formData.time_range}
                      onChange={(e) => setFormData({ ...formData, time_range: e.target.value })}
                      placeholder="e.g., 5 years"
                      className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="city_data" className="block text-sm font-medium text-slate-200 mb-2">
                    City/Location Data
                  </label>
                  <input
                    type="text"
                    id="city_data"
                    value={formData.city_data}
                    onChange={(e) => setFormData({ ...formData, city_data: e.target.value })}
                    placeholder="e.g., San Francisco, CA - Population 870,000"
                    className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label htmlFor="interests" className="block text-sm font-medium text-slate-200 mb-2">
                    Specific Interests/Criteria
                  </label>
                  <input
                    type="text"
                    id="interests"
                    value={formData.interests}
                    onChange={(e) => setFormData({ ...formData, interests: e.target.value })}
                    placeholder="e.g., Economic impact, social equity, feasibility"
                    className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                {/* Submit Button */}
                <div className="flex gap-4 pt-4">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => router.push("/")}
                    className="flex-1"
                    disabled={loading}
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    className="flex-1 bg-blue-500 hover:bg-blue-600"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Creating Session...
                      </>
                    ) : (
                      <>
                        <Rocket className="w-4 h-4 mr-2" />
                        Start Deliberation
                      </>
                    )}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
