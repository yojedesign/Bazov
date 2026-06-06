'use client';

import { useUser } from '@clerk/nextjs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Users, Bell, BarChart3, Network, TrendingUp, Clock, UserPlus } from 'lucide-react';
import Link from 'next/link';

export default function DashboardPage() {
  const { user } = useUser();

  const stats = [
    { label: 'Total Connections', value: '1,234', icon: Users, change: '+12%' },
    { label: 'New Signals', value: '42', icon: Bell, change: '+8' },
    { label: 'Network Growth', value: '89%', icon: Network, change: '+5%' },
    { label: 'Engagement', value: '74%', icon: TrendingUp, change: '+3%' },
  ];

  const quickActions = [
    { label: 'Add Connection', href: '/dashboard/people/new', icon: UserPlus },
    { label: 'View Signals', href: '/dashboard/signals', icon: Bell },
    { label: 'Analyze Network', href: '/dashboard/analytics', icon: BarChart3 },
    { label: 'Recent Activity', href: '/dashboard/activity', icon: Clock },
  ];

  return (
    <div className="space-y-8">
      {/* Welcome section */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">
          Welcome back, {user?.firstName || 'User'}! 👋
        </h1>
        <p className="text-muted-foreground">
          Here's what's happening in your professional network today.
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.label} className="hover:shadow-md transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">{stat.label}</CardTitle>
              <div className="p-2 rounded-lg bg-muted">
                <stat.icon className="h-4 w-4 text-muted-foreground" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">{stat.change}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick actions */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold tracking-tight">Quick Actions</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {quickActions.map((action) => (
            <Card key={action.label} className="hover:shadow-md transition-shadow cursor-pointer">
              <Link href={action.href} className="block">
                <CardHeader className="flex flex-row items-center gap-4 pb-2">
                  <div className="p-2 rounded-lg bg-primary text-primary-foreground">
                    <action.icon className="h-5 w-5" />
                  </div>
                  <CardTitle className="text-lg font-medium">{action.label}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>
                    Click to {action.label.toLowerCase()}
                  </CardDescription>
                </CardContent>
              </Link>
            </Card>
          ))}
        </div>
      </div>

      {/* Recent activity placeholder */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold tracking-tight">Recent Activity</h2>
        <Card>
          <CardHeader>
            <CardTitle>Activity Feed</CardTitle>
            <CardDescription>
              Your recent network activity and signals
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center gap-4 p-4 border rounded-lg">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted">
                  <Users className="h-5 w-5 text-muted-foreground" />
                </div>
                <div className="flex-1">
                  <p className="font-medium">New connection added</p>
                  <p className="text-sm text-muted-foreground">2 hours ago</p>
                </div>
              </div>
              <div className="flex items-center gap-4 p-4 border rounded-lg">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted">
                  <Bell className="h-5 w-5 text-muted-foreground" />
                </div>
                <div className="flex-1">
                  <p className="font-medium">New signal detected</p>
                  <p className="text-sm text-muted-foreground">5 hours ago</p>
                </div>
              </div>
              <div className="flex items-center gap-4 p-4 border rounded-lg">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted">
                  <BarChart3 className="h-5 w-5 text-muted-foreground" />
                </div>
                <div className="flex-1">
                  <p className="font-medium">Network analysis complete</p>
                  <p className="text-sm text-muted-foreground">1 day ago</p>
                </div>
              </div>
            </div>
            <div className="pt-4">
              <Button variant="outline" className="w-full">
                View all activity
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
