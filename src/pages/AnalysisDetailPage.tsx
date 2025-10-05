import { useParams } from 'react-router-dom'

export default function AnalysisDetailPage() {
  const { id } = useParams()
  
  return (
    <div className="container py-8">
      <h1 className="text-4xl font-bold mb-4">Analysis {id}</h1>
      <p className="text-muted-foreground">Detailed biomarker analysis will appear here.</p>
    </div>
  )
}
