import { Metadata } from 'next'
import DevApiProbe from '../components/DevApiProbe'
import { InsightsPanel } from '../components/insights/InsightsPanel'

export const metadata: Metadata = {
  title: 'HealthIQ AI v5 - Demo & Development Tools',
  description: 'Development tools and demo harness for HealthIQ AI v5 backend integration',
}

export default function DemoPage() {
  // Mock insights data for demonstration
  const mockInsights = [
    {
      id: "metabolic_insight_1",
      category: "metabolic",
      summary: "Your metabolic cluster suggests insulin resistance risk, amplified by reported low activity levels.",
      evidence: {
        biomarkers: ["glucose", "hba1c", "insulin"],
        scores: { glucose: 0.75, hba1c: 0.68, insulin: 0.82 },
        lifestyle_factors: ["exercise", "diet"]
      },
      confidence: 0.85,
      severity: "warning" as const,
      recommendations: [
        "Increase physical activity to at least 150 minutes per week",
        "Consider reducing refined carbohydrate intake",
        "Monitor blood glucose levels regularly"
      ],
      biomarkers_involved: ["glucose", "hba1c", "insulin"],
      lifestyle_factors: ["exercise", "diet"],
      created_at: new Date().toISOString()
    },
    {
      id: "cardiovascular_insight_1",
      category: "cardiovascular",
      summary: "Elevated cholesterol patterns indicate increased cardiovascular risk, particularly given your current lifestyle factors.",
      evidence: {
        biomarkers: ["total_cholesterol", "ldl_cholesterol", "hdl_cholesterol"],
        scores: { total_cholesterol: 0.72, ldl_cholesterol: 0.78, hdl_cholesterol: 0.45 },
        lifestyle_factors: ["diet", "exercise", "smoking"]
      },
      confidence: 0.88,
      severity: "warning" as const,
      recommendations: [
        "Focus on heart-healthy diet with reduced saturated fats",
        "Increase cardiovascular exercise",
        "Consider discussing statin therapy with your healthcare provider"
      ],
      biomarkers_involved: ["total_cholesterol", "ldl_cholesterol", "hdl_cholesterol"],
      lifestyle_factors: ["diet", "exercise"],
      created_at: new Date().toISOString()
    },
    {
      id: "inflammatory_insight_1",
      category: "inflammatory",
      summary: "Elevated inflammatory markers suggest chronic inflammation, potentially linked to your stress levels and sleep patterns.",
      evidence: {
        biomarkers: ["crp", "esr"],
        scores: { crp: 0.65, esr: 0.58 },
        lifestyle_factors: ["stress", "sleep"]
      },
      confidence: 0.75,
      severity: "info" as const,
      recommendations: [
        "Implement stress management techniques",
        "Improve sleep quality and duration",
        "Consider anti-inflammatory dietary changes"
      ],
      biomarkers_involved: ["crp", "esr"],
      lifestyle_factors: ["stress", "sleep"],
      created_at: new Date().toISOString()
    }
  ];

  return (
    <main className="min-h-screen">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">
          HealthIQ AI v5 - Demo & Development
        </h1>
        <p className="text-center text-lg text-muted-foreground">
          Backend Integration Demo and Development Tools
        </p>
        
        {/* Insights Panel Demo */}
        <div className="mt-8">
          <InsightsPanel insights={mockInsights} />
        </div>
        
        <div className="mt-8 p-8 border border-dashed border-gray-300 rounded-lg text-center">
          <p className="text-gray-600">
            🚧 Development Tools and Backend Demo
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Use the Dev API Probe (bottom right) to test backend integration
          </p>
        </div>
      </div>
      {process.env.NODE_ENV === 'development' && <DevApiProbe />}
    </main>
  )
}
