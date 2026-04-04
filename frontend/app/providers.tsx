'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ThemeProvider } from 'next-themes'
import { useEffect, useState } from 'react'
import { useAuthStore } from './state/authStore'

export default function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000,
        retry: 1,
      },
    },
  }))

  const initializeAuth = useAuthStore((s) => s.initialize)
  useEffect(() => {
    initializeAuth()
  }, [initializeAuth])

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider
        attribute="class"
        defaultTheme="dark"
        enableSystem={false}
        storageKey="healthiq-theme"
      >
        {children}
      </ThemeProvider>
    </QueryClientProvider>
  )
}
