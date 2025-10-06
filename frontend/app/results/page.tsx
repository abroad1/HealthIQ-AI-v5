'use client'

import { useEffect, useState, Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import BiomarkerDials from '@/components/biomarkers/BiomarkerDials'
import { InsightsPanel } from '@/components/insights/InsightsPanel'
import ClusterSummary from '@/components/clusters/ClusterSummary'
import { getAnalysisResult } from '@/lib/api'

function ResultsContent() {
  const searchParams = useSearchParams()
  const analysisId = searchParams.get('analysis_id')
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!analysisId) return
    const fetchData = async () => {
      try {
        const result = await getAnalysisResult(analysisId)
        setData(result)
      } catch (err) {
        console.error('Error fetching analysis result', err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [analysisId])

  if (loading) return <p className="p-8">Loading analysis results...</p>
  if (!data) return <p className="p-8 text-red-600">No data found.</p>

  // Transform biomarkers array to object format expected by BiomarkerDials
  const biomarkersObject = data.biomarkers?.reduce((acc: any, biomarker: any) => {
    acc[biomarker.biomarker_name] = {
      value: biomarker.value,
      unit: biomarker.unit,
      status: biomarker.status,
      referenceRange: biomarker.reference_range ? {
        min: biomarker.reference_range.min,
        max: biomarker.reference_range.max,
        unit: biomarker.reference_range.unit
      } : undefined,
      date: data.created_at
    };
    return acc;
  }, {}) || {};

  return (
    <div className="min-h-screen bg-gray-50 p-6 space-y-8">
      <h1 className="text-2xl font-semibold">Health Analysis Results</h1>
      <BiomarkerDials biomarkers={biomarkersObject} />
      <ClusterSummary clusters={data.clusters || []} />
      <InsightsPanel insights={data.insights || []} />
    </div>
  )
}

export default function ResultsPage() {
  return (
    <Suspense fallback={<p className="p-8">Loading...</p>}>
      <ResultsContent />
    </Suspense>
  )
}
