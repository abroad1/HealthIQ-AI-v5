'use client'

import { SidebarProvider } from '../components/ui/sidebar'
import { Header } from '../components/layout/Header'
import { AppSidebar } from '../components/layout/AppSidebar'
import { Footer } from '../components/layout/Footer'

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider defaultOpen={true}>
      <div className="min-h-screen flex w-full flex-col">
        <Header />
        <div className="flex flex-1">
          <AppSidebar />
          <main className="flex-1">
            {children}
          </main>
        </div>
        <Footer />
      </div>
    </SidebarProvider>
  )
}
