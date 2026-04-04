'use client'

import Link from 'next/link'
import { useTheme } from 'next-themes'
import { Moon, Sun, Menu, LogOut } from 'lucide-react'
import { Button } from '../ui/button'
import { useSidebar } from '../ui/sidebar'
import { useAuthStore } from '../../state/authStore'

export function Header() {
  const { theme, setTheme } = useTheme()
  const sidebar = useSidebar()
  const user = useAuthStore((s) => s.user)
  const logout = useAuthStore((s) => s.logout)
  const authLoading = useAuthStore((s) => s.loading)

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-4">
          {sidebar && (
            <Button
              variant="ghost"
              size="icon"
              onClick={() => sidebar.toggleSidebar()}
              className="lg:hidden"
            >
              <Menu className="h-5 w-5" />
            </Button>
          )}
          <Link href="/" className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
              <span className="text-lg font-bold text-primary-foreground">H</span>
            </div>
            <span className="text-xl font-bold">HealthIQ AI</span>
          </Link>
        </div>

        <div className="flex items-center gap-2">
          {user ? (
            <>
              <span className="hidden text-sm text-muted-foreground sm:inline max-w-[10rem] truncate" title={user.email}>
                {user.email || user.id}
              </span>
              <Button
                variant="outline"
                size="sm"
                disabled={authLoading}
                onClick={() => {
                  void logout().then(() => {
                    window.location.href = '/login'
                  })
                }}
              >
                <LogOut className="h-4 w-4 mr-1" />
                Log out
              </Button>
            </>
          ) : (
            <Button variant="outline" size="sm" asChild>
              <Link href="/login">Sign in</Link>
            </Button>
          )}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          >
            <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            <span className="sr-only">Toggle theme</span>
          </Button>
        </div>
      </div>
    </header>
  )
}
