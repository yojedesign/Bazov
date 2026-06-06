'use client';

import { useState, useEffect, useCallback } from 'react';
import { useUser } from '@clerk/nextjs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import apiClient from '@/lib/api';
import { BarChart3, LineChart, PieChart, TrendingUp, TrendingDown, Users, Bell, Building, Clock, AlertCircle, Activity, Brain, Target, CheckCircle, XCircle } from 'lucide-react';

// Simple chart components (placeholder for real chart libraries)
function BarChart({ data, title }: { data: { label: string; value: number }[]; title: string }) {
  const maxValue = Math.max(...data.map(d => d.value), 1);

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-medium">{title}</h3>
      <div className="flex items-end gap-2 h-40">
        {data.map((d, index) => (
          <div key={index} className="flex-1 flex flex-col items-center gap-1">
            <div
              className="w-full bg-primary rounded-t-md transition-all duration-300"
              style={{ height: `${(d.value / maxValue) * 100}%` }}
            />
            <span className="text-xs text-muted-foreground truncate w-full text-center">{d.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function LineChart({ data, title }: { data: { label: string; value: number }[]; title: string }) {
  const maxValue = Math.max(...data.map(d => d.value), 1);
  const points = data.map((d, i) => ({
    x: (i / (data.length - 1)) * 100,
    y: 100 - (d.value / maxValue) * 100,
    label: d.label,
    value: d.value,
  }));

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-medium">{title}</h3>
      <div className="relative h-40 border rounded-md p-4">
        <svg width="100%" height="100%" viewBox="0 0 100 100">
          {/* Grid lines */}
          <line x1="0" y1="25" x2="100" y2="25" stroke="#e5e7eb" strokeWidth="0.5" />
          <line x1="0" y1="50" x2="100" y2="50" stroke="#e5e7eb" strokeWidth="0.5" />
          <line x1="0" y1="75" x2="100" y2="75" stroke="#e5e7eb" strokeWidth="0.5" />
          
          {/* Line */}
          <polyline
            points={points.map(p => `${p.x},${p.y}`).join(' ')}
            fill="none"
            stroke="#3b82f6"
            strokeWidth="2"
          />
          
          {/* Points */}
          {points.map((p, i) => (
            <circle
              key={i}
              cx={p.x}
              cy={p.y}
              r="2"
              fill="#3b82f6"
            />
          ))}
        </svg>
      </div>
    </div>
  );
}

function PieChart({ data, title }: { data: { label: string; value: number; color: string }[]; title: string }) {
  const total = data.reduce((sum, d) => sum + d.value, 0);
  let cumulative = 0;

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-medium">{title}</h3>
      <div className="flex items-center gap-4">
        <div className="relative h-32 w-32">
          <svg width="100%" height="100%" viewBox="-1 -1 2 2">
            {data.map((d, i) => {
              const startAngle = cumulative;
              const endAngle = cumulative + (d.value / total) * 2 * Math.PI;
              cumulative = endAngle;
              
              const startX = Math.cos(startAngle);
              const startY = Math.sin(startAngle);
              const endX = Math.cos(endAngle);
              const endY = Math.sin(endAngle);
              
              const largeArc = endAngle - startAngle > Math.PI ? 1 : 0;
              
              return (
                <path
                  key={i}
                  d={`M 0 0 L ${startX} ${startY} A 1 1 0 ${largeArc} 1 ${endX} ${endY} Z`}
                  fill={d.color}
                  stroke="white"
                  strokeWidth="0.02"
                />
              );
            })}
          </svg>
        </div>
        <div className="space-y-2">
          {data.map((d, i) => (
            <div key={i} className="flex items-center gap-2">
              <div className="h-3 w-3 rounded-full" style={{ backgroundColor: d.color }} />
              <span className="text-sm">{d.label}</span>
              <span className="text-sm text-muted-foreground ml-auto">
                {((d.value / total) * 100).toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, change, trend }: {
  icon: React.ElementType;
  label: string;
  value: string | number;
  change?: string;
  trend?: 'up' | 'down' | 'neutral';
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium">{label}</CardTitle>
        <div className="p-2 rounded-lg bg-muted">
          <Icon className="h-4 w-4 text-muted-foreground" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {change && (
          <p className={cn(
            'text-xs mt-1',
            trend === 'up' ? 'text-green-600' :
            trend === 'down' ? 'text-red-600' :
            'text-muted-foreground'
          )}>
            {change}
          </p>
        )}
      </CardContent>
    </Card>
  );
}

export default function AnalyticsPage() {
  const { user } = useUser();
  const [stats, setStats] = useState({
    totalSignals: 0,
    newSignals: 0,
    totalPeople: 0,
    totalCompanies: 0,
    networkGrowth: 0,
    engagement: 0,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState<'week' | 'month' | 'quarter' | 'year'>('month');

  const fetchAnalytics = useCallback(async () => {
    if (!user) return;

    try {
      setIsLoading(true);
      setError(null);

      // Get access token from Clerk
      const token = await user.getToken();

      // Fetch analytics data (placeholder - would call actual API endpoints)
      // For now, using mock data
      const mockStats = {
        totalSignals: 1247,
        newSignals: 42,
        totalPeople: 892,
        totalCompanies: 156,
        networkGrowth: 12.5,
        engagement: 78.3,
      };

      setStats(mockStats);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch analytics');
      console.error('Error fetching analytics:', err);
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  useEffect(() => {
    fetchAnalytics();
  }, [fetchAnalytics]);

  // Signal type distribution
  const signalTypeData = [
    { label: 'Hiring', value: 342, color: '#10b981' },
    { label: 'Funding', value: 218, color: '#3b82f6' },
    { label: 'Partnership', value: 189, color: '#8b5cf6' },
    { label: 'Leadership', value: 156, color: '#f59e0b' },
    { label: 'Product', value: 287, color: '#06b6d4' },
    { label: 'Other', value: 55, color: '#6b7280' },
  ];

  // Sentiment distribution
  const sentimentData = [
    { label: 'Positive', value: 789, color: '#10b981' },
    { label: 'Neutral', value: 345, color: '#6b7280' },
    { label: 'Negative', value: 113, color: '#ef4444' },
  ];

  // Signals over time
  const signalsOverTime = [
    { label: 'Jan', value: 89 },
    { label: 'Feb', value: 102 },
    { label: 'Mar', value: 124 },
    { label: 'Apr', value: 98 },
    { label: 'May', value: 135 },
    { label: 'Jun', value: 117 },
    { label: 'Jul', value: 142 },
    { label: 'Aug', value: 128 },
    { label: 'Sep', value: 156 },
    { label: 'Oct', value: 131 },
    { label: 'Nov', value: 167 },
    { label: 'Dec', value: 142 },
  ];

  // Top companies by signals
  const topCompanies = [
    { label: 'TechCorp', value: 45 },
    { label: 'Innovate', value: 38 },
    { label: 'NextGen', value: 32 },
    { label: 'Alpha', value: 28 },
    { label: 'Beta', value: 24 },
    { label: 'Gamma', value: 21 },
    { label: 'Delta', value: 18 },
    { label: 'Epsilon', value: 15 },
  ];

  // ML Model Performance (from ML endpoints)
  const mlPerformance = [
    { label: 'Signal Classifier', value: 92.4, color: '#10b981' },
    { label: 'Relationship Strength', value: 87.2, color: '#3b82f6' },
    { label: 'Recommendation', value: 84.5, color: '#8b5cf6' },
    { label: 'Anomaly Detection', value: 91.8, color: '#f59e0b' },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Analytics</h1>
            <p className="text-muted-foreground">
              Insights and performance metrics for your relationship intelligence
            </p>
          </div>
          <div className="flex gap-2">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value as 'week' | 'month' | 'quarter' | 'year')}
              className="h-10 px-3 py-2 text-sm border rounded-md bg-background"
            >
              <option value="week">Last Week</option>
              <option value="month">Last Month</option>
              <option value="quarter">Last Quarter</option>
              <option value="year">Last Year</option>
            </select>
            <Button size="sm" onClick={fetchAnalytics}>
              Refresh
            </Button>
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
        <StatCard
          icon={Bell}
          label="Total Signals"
          value={stats.totalSignals.toLocaleString()}
          change="+12% MoM"
          trend="up"
        />
        <StatCard
          icon={Bell}
          label="New Signals"
          value={stats.newSignals}
          change="+8 today"
          trend="up"
        />
        <StatCard
          icon={Users}
          label="Total People"
          value={stats.totalPeople.toLocaleString()}
          change="+45 this month"
          trend="up"
        />
        <StatCard
          icon={Building}
          label="Total Companies"
          value={stats.totalCompanies.toLocaleString()}
          change="+3 new"
          trend="up"
        />
        <StatCard
          icon={Network}
          label="Network Growth"
          value={`${stats.networkGrowth}%`}
          change="+2.5%"
          trend="up"
        />
        <StatCard
          icon={Activity}
          label="Engagement"
          value={`${stats.engagement}%`}
          change="-1.2%"
          trend="down"
        />
      </div>

      {/* Charts Row 1 */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Signal Types Distribution</CardTitle>
            <CardDescription>Breakdown of signals by type</CardDescription>
          </CardHeader>
          <CardContent>
            <PieChart data={signalTypeData} title="" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Sentiment Analysis</CardTitle>
            <CardDescription>Signal sentiment distribution</CardDescription>
          </CardHeader>
          <CardContent>
            <PieChart data={sentimentData} title="" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>ML Model Performance</CardTitle>
            <CardDescription>Accuracy scores for ML models</CardDescription>
          </CardHeader>
          <CardContent>
            <BarChart
              data={mlPerformance.map(d => ({ label: d.label, value: d.value }))}
              title=""
            />
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Signals Over Time</CardTitle>
            <CardDescription>Signal volume trend</CardDescription>
          </CardHeader>
          <CardContent>
            <LineChart data={signalsOverTime} title="" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Top Companies by Signals</CardTitle>
            <CardDescription>Companies generating the most signals</CardDescription>
          </CardHeader>
          <CardContent>
            <BarChart data={topCompanies} title="" />
          </CardContent>
        </Card>
      </div>

      {/* ML Insights */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold tracking-tight">Machine Learning Insights</h2>
        
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Signal Classifier</CardTitle>
              <Badge variant="default" className="text-xs">Active</Badge>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-600">92.4%</div>
              <p className="text-xs text-muted-foreground mt-1">Accuracy</p>
              <div className="mt-4 space-y-1">
                <div className="flex justify-between text-xs">
                  <span>Precision</span>
                  <span>91.8%</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Recall</span>
                  <span>93.1%</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>F1 Score</span>
                  <span>92.4%</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Relationship Strength</CardTitle>
              <Badge variant="default" className="text-xs">Active</Badge>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-600">87.2%</div>
              <p className="text-xs text-muted-foreground mt-1">Accuracy</p>
              <div className="mt-4 space-y-1">
                <div className="flex justify-between text-xs">
                  <span>Strong</span>
                  <span>234</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Medium</span>
                  <span>456</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Weak</span>
                  <span>123</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Anomaly Detection</CardTitle>
              <Badge variant="default" className="text-xs">Active</Badge>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-600">91.8%</div>
              <p className="text-xs text-muted-foreground mt-1">Accuracy</p>
              <div className="mt-4 space-y-1">
                <div className="flex justify-between text-xs">
                  <span>Detected</span>
                  <span className="text-red-600">42</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>False Positives</span>
                  <span>3</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>True Positives</span>
                  <span className="text-green-600">39</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Recommendation Engine</CardTitle>
              <Badge variant="default" className="text-xs">Active</Badge>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-purple-600">84.5%</div>
              <p className="text-xs text-muted-foreground mt-1">Accuracy</p>
              <div className="mt-4 space-y-1">
                <div className="flex justify-between text-xs">
                  <span>Accepted</span>
                  <span className="text-green-600">156</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Rejected</span>
                  <span className="text-red-600">23</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Click Rate</span>
                  <span>78.2%</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent ML Activity</CardTitle>
          <CardDescription>Latest machine learning operations</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { type: 'Signal Classified', detail: 'Hiring signal from TechCorp', time: '2 min ago', status: 'success' },
              { type: 'Relationship Analyzed', detail: 'John Doe - Jane Smith connection', time: '5 min ago', status: 'success' },
              { type: 'Anomaly Detected', detail: 'Unusual activity pattern detected', time: '15 min ago', status: 'warning' },
              { type: 'Recommendation Generated', detail: '12 new connection suggestions', time: '1 hour ago', status: 'success' },
              { type: 'Model Retrained', detail: 'Signal classifier v2.1.0', time: '3 hours ago', status: 'success' },
            ].map((activity, index) => (
              <div key={index} className="flex items-center gap-4 p-3 border rounded-lg">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-muted">
                  {activity.status === 'success' ? (
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  ) : activity.status === 'warning' ? (
                    <AlertCircle className="h-4 w-4 text-orange-600" />
                  ) : (
                    <XCircle className="h-4 w-4 text-red-600" />
                  )}
                </div>
                <div className="flex-1">
                  <p className="font-medium">{activity.type}</p>
                  <p className="text-sm text-muted-foreground">{activity.detail}</p>
                </div>
                <div className="text-sm text-muted-foreground">
                  {activity.time}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
