export default function AnalysisDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="container py-8">
      <h1 className="text-4xl font-bold mb-4">Analysis {params.id}</h1>
      <p className="text-muted-foreground">Detailed biomarker analysis will appear here.</p>
    </div>
  )
}
