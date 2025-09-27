import { Metadata } from 'next'
import DevApiProbe from './components/DevApiProbe'

export const metadata: Metadata = {
  title: 'HealthIQ AI v5 - Precision Biomarker Intelligence',
  description: 'AI-powered biomarker analysis platform for personalized health insights',
}

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">
          HealthIQ AI v5
        </h1>
        <p className="text-center text-lg text-muted-foreground">
          Precision Biomarker Intelligence Platform
        </p>
        <div className="mt-8 p-8 border border-dashed border-gray-300 rounded-lg text-center">
          <p className="text-gray-600">
            🚧 Frontend architecture migration in progress
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Next.js 14+ App Router structure being implemented
          </p>
        </div>
      </div>
      {process.env.NODE_ENV === 'development' && <DevApiProbe />}
    </main>
  )
}
