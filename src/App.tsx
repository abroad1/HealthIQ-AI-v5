import { Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ThemeProvider } from 'next-themes'
import { useState } from 'react'
import LandingPage from './routes/LandingPage'
import AppLayout from './layouts/AppLayout'
import DashboardPage from './routes/DashboardPage'
import AnalysisPage from './routes/AnalysisPage'
import AnalysisDetailPage from './routes/AnalysisDetailPage'
import ReportsPage from './routes/ReportsPage'
import ProfilePage from './routes/ProfilePage'
import SettingsPage from './routes/SettingsPage'
import UploadPage from './routes/UploadPage'
import ResultsPage from './routes/ResultsPage'

function App() {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000,
        retry: 1,
      },
    },
  }))

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider
        attribute="class"
        defaultTheme="dark"
        enableSystem={false}
        storageKey="healthiq-theme"
      >
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/" element={<AppLayout />}>
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="analysis" element={<AnalysisPage />} />
            <Route path="analysis/:id" element={<AnalysisDetailPage />} />
            <Route path="reports" element={<ReportsPage />} />
            <Route path="profile" element={<ProfilePage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route path="upload" element={<UploadPage />} />
            <Route path="results" element={<ResultsPage />} />
          </Route>
        </Routes>
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export default App
