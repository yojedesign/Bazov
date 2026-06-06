'use client';

import type { Metadata } from 'next';
import { usePathname } from 'next/navigation';
import { UserButton, useUser } from '@clerk/nextjs';
import Link from 'next/link';
import { Home, Users, Bell, BarChart3, Settings, HelpCircle, Network } from 'lucide-react';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export const metadata: Metadata = {
  title: 'Dashboard',
  description: 'Your relationship intelligence dashboard',
};

const navigationItems = [
  { href: '/dashboard', icon: Home, label: 'Home' },
  { href: '/dashboard/network', icon: Network, label: 'Network' },
  { href: '/dashboard/signals', icon: Bell, label: 'Signals' },
  { href: '/dashboard/analytics', icon: BarChart3, label: 'Analytics' },
  { href: '/dashboard/people', icon: Users, label: 'People' },
  { href: '/dashboard/settings', icon: Settings, label: 'Settings' },
];

const bottomNavigationItems = [
  { href: '/dashboard/help', icon: HelpCircle, label: 'Help' },
];

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname();
  const { user } = useUser();

  return (
    <div className="flex min-h-screen bg-background">
      {/* Sidebar */}
      <aside className="hidden w-64 flex-col border-r border-border bg-card p-6 lg:flex">
        <div className="flex items-center gap-3 pb-8">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground font-bold text-lg">
            B
          </div>
          <span className="font-bold text-lg">Bazov</span>
        </div>
        
        <nav className="flex-1 space-y-1">
          {navigationItems.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-accent text-accent-foreground'
                    : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                }`}
              >
                <item.icon className="h-4 w-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>
        
        <nav className="space-y-1 pt-4 border-t border-border">
          {bottomNavigationItems.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-accent text-accent-foreground'
                    : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                }`}
              >
                <item.icon className="h-4 w-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>
        
        {/* User profile */}
        <div className="pt-4 border-t border-border">
          <UserButton afterSignOutUrl="/" />
        </div>
      </aside>

      {/* Mobile header */}
      <header className="flex h-16 items-center justify-between border-b border-border bg-card px-4 lg:hidden">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground font-bold text-lg">
            B
          </div>
          <span className="font-bold text-lg">Bazov</span>
        </div>
        <UserButton afterSignOutUrl="/" />
      </header>

      {/* Mobile navigation */}
      <nav className="flex justify-around border-b border-border bg-card px-4 py-2 lg:hidden">
        {navigationItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center gap-1 py-2 text-xs font-medium transition-colors ${
                isActive
                  ? 'text-accent-foreground'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* Main content */}
      <main className="flex-1 p-4 lg:p-8">
        {children}
      </main>
    </div>
  );
}
