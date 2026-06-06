'use client';

import { useState, useEffect, useCallback } from 'react';
import { useUser } from '@clerk/nextjs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { SearchBar } from '@/components/ui/search-bar';
import { DataTable, Pagination, PageSizeSelector } from '@/components/ui/data-table';
import apiClient from '@/lib/api';
import { Signal } from '@/types';
import { Calendar, User, Building, TrendingUp, TrendingDown, AlertCircle, Plus, Filter, Eye, MessageSquare, Share2 } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

// Signal type colors
const signalTypeColors: Record<string, string> = {
  hiring: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  funding: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  partnership: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
  leadership: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
  product: 'bg-cyan-100 text-cyan-800 dark:bg-cyan-900 dark:text-cyan-200',
  acquisition: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  expansion: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200',
  default: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
};

// Sentiment colors
const sentimentColors: Record<string, string> = {
  positive: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  negative: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  neutral: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
};

// Signal type icons
const signalTypeIcons: Record<string, React.ReactNode> = {
  hiring: <User className="h-3 w-3" />,
  funding: <TrendingUp className="h-3 w-3" />,
  partnership: <Building className="h-3 w-3" />,
  leadership: <User className="h-3 w-3" />,
  product: <Plus className="h-3 w-3" />,
  acquisition: <Building className="h-3 w-3" />,
  expansion: <TrendingUp className="h-3 w-3" />,
};

export default function SignalsPage() {
  const { user } = useUser();
  const [signals, setSignals] = useState<Signal[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [signalTypeFilter, setSignalTypeFilter] = useState<string | null>(null);
  const [sentimentFilter, setSentimentFilter] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [total, setTotal] = useState(0);
  const [signalTypes, setSignalTypes] = useState<string[]>([]);
  const [sortBy, setSortBy] = useState<string | null>('created_at');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');

  const fetchSignals = useCallback(async () => {
    if (!user) return;

    try {
      setIsLoading(true);
      setError(null);

      // Get access token from Clerk
      const token = await user.getToken();

      // Fetch signal types
      const typesResponse = await apiClient.signals.getTypes();
      setSignalTypes(typesResponse.types);

      // Fetch signals with filters
      const response = await apiClient.signals.list(token, {
        skip: (page - 1) * pageSize,
        limit: pageSize,
        signal_type: signalTypeFilter || undefined,
        search: searchQuery || undefined,
      });

      setSignals(response.items);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch signals');
      console.error('Error fetching signals:', err);
    } finally {
      setIsLoading(false);
    }
  }, [user, page, pageSize, signalTypeFilter, searchQuery, sentimentFilter]);

  useEffect(() => {
    fetchSignals();
  }, [fetchSignals]);

  useEffect(() => {
    // Reset to first page when filters change
    setPage(1);
  }, [signalTypeFilter, searchQuery, sentimentFilter]);

  const handleSort = useCallback((key: string, direction: 'asc' | 'desc') => {
    setSortBy(key);
    setSortDirection(direction);
    // For now, we'll just re-fetch with the new sort
    // In a real implementation, you'd pass sort params to the API
    fetchSignals();
  }, [fetchSignals]);

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
  }, []);

  const handlePageChange = useCallback((newPage: number) => {
    setPage(newPage);
  }, []);

  const handlePageSizeChange = useCallback((size: number) => {
    setPageSize(size);
    setPage(1); // Reset to first page when changing page size
  }, []);

  const getSignalTypeColor = (type: string) => {
    return signalTypeColors[type.toLowerCase()] || signalTypeColors.default;
  };

  const getSentimentColor = (sentiment: string) => {
    return sentimentColors[sentiment.toLowerCase()] || sentimentColors.neutral;
  };

  const getSignalTypeIcon = (type: string) => {
    return signalTypeIcons[type.toLowerCase()] || <AlertCircle className="h-3 w-3" />;
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'N/A';
    try {
      return formatDistanceToNow(new Date(dateString), { addSuffix: true });
    } catch {
      return dateString;
    }
  };

  const columns = [
    {
      key: 'signal_type',
      header: 'Type',
      sortable: true,
      render: (signal: Signal) => (
        <Badge className={cn('gap-1', getSignalTypeColor(signal.signal_type))}>
          {getSignalTypeIcon(signal.signal_type)}
          {signal.signal_type}
        </Badge>
      ),
      className: 'w-[120px]',
    },
    {
      key: 'title',
      header: 'Title',
      sortable: true,
      render: (signal: Signal) => (
        <div className="font-medium line-clamp-2">{signal.title}</div>
      ),
      className: 'min-w-[200px]',
    },
    {
      key: 'content',
      header: 'Content',
      sortable: false,
      render: (signal: Signal) => (
        <div className="text-sm text-muted-foreground line-clamp-2">{signal.content}</div>
      ),
      className: 'min-w-[250px]',
    },
    {
      key: 'sentiment',
      header: 'Sentiment',
      sortable: true,
      render: (signal: Signal) => (
        <Badge className={cn(getSentimentColor(signal.sentiment))}>
          {signal.sentiment}
        </Badge>
      ),
      className: 'w-[100px]',
    },
    {
      key: 'confidence',
      header: 'Confidence',
      sortable: true,
      render: (signal: Signal) => (
        <div className="flex items-center gap-2">
          <div className="h-2 w-16 bg-muted rounded-full overflow-hidden">
            <div
              className="h-full bg-primary rounded-full"
              style={{ width: `${(signal.confidence || 0) * 100}%` }}
            />
          </div>
          <span className="text-sm font-medium">
            {(signal.confidence * 100).toFixed(0)}%
          </span>
        </div>
      ),
      className: 'w-[150px]',
    },
    {
      key: 'source',
      header: 'Source',
      sortable: true,
      render: (signal: Signal) => (
        <div className="text-sm">
          {signal.source_type}
          {signal.source_author && (
            <div className="text-muted-foreground">by {signal.source_author}</div>
          )}
        </div>
      ),
      className: 'w-[150px]',
    },
    {
      key: 'created_at',
      header: 'Date',
      sortable: true,
      render: (signal: Signal) => (
        <div className="text-sm text-muted-foreground whitespace-nowrap">
          {formatDate(signal.created_at)}
        </div>
      ),
      className: 'w-[120px]',
    },
    {
      key: 'actions',
      header: 'Actions',
      sortable: false,
      render: () => (
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            <Eye className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            <MessageSquare className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            <Share2 className="h-4 w-4" />
          </Button>
        </div>
      ),
      className: 'w-[120px]',
    },
  ];

  const totalPages = Math.ceil(total / pageSize);

  // Stats for the page
  const stats = [
    { label: 'Total Signals', value: total, icon: AlertCircle },
    { label: 'New Today', value: signals.filter(s => 
      s.created_at && new Date(s.created_at).toDateString() === new Date().toDateString()
    ).length, icon: TrendingUp },
    { label: 'High Confidence', value: signals.filter(s => s.confidence >= 0.8).length, icon: TrendingUp },
    { label: 'Positive', value: signals.filter(s => s.sentiment === 'positive').length, icon: TrendingUp },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Signals</h1>
            <p className="text-muted-foreground">
              Track important events and changes in your network
            </p>
          </div>
          <Button className="gap-1">
            <Plus className="h-4 w-4" />
            Add Signal
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.label}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">{stat.label}</CardTitle>
              <div className="p-2 rounded-lg bg-muted">
                <stat.icon className="h-4 w-4 text-muted-foreground" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle>Filters</CardTitle>
          <CardDescription>
            Narrow down your signals by type, sentiment, and more
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <label className="text-sm font-medium">Signal Type</label>
              <select
                value={signalTypeFilter || ''}
                onChange={(e) => setSignalTypeFilter(e.target.value || null)}
                className="w-full h-10 px-3 py-2 text-sm border rounded-md bg-background"
              >
                <option value="">All Types</option>
                {signalTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Sentiment</label>
              <select
                value={sentimentFilter || ''}
                onChange={(e) => setSentimentFilter(e.target.value || null)}
                className="w-full h-10 px-3 py-2 text-sm border rounded-md bg-background"
              >
                <option value="">All Sentiments</option>
                <option value="positive">Positive</option>
                <option value="negative">Negative</option>
                <option value="neutral">Neutral</option>
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Search</label>
              <SearchBar
                placeholder="Search signals..."
                onSearch={handleSearch}
                className="w-full"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setSignalTypeFilter(null);
                setSentimentFilter(null);
                setSearchQuery('');
              }}
              className="gap-1"
            >
              <Filter className="h-4 w-4" />
              Clear Filters
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Signals Table */}
      <Card>
        <CardHeader>
          <CardTitle>All Signals</CardTitle>
          <CardDescription>
            {total} signals found
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error ? (
            <div className="flex items-center justify-center py-12 text-destructive">
              {error}
            </div>
          ) : (
            <>
              <DataTable
                columns={columns}
                data={signals}
                keyExtractor={(signal) => signal.id}
                onSort={handleSort}
                sortBy={sortBy}
                sortDirection={sortDirection}
                isLoading={isLoading}
                emptyMessage="No signals found matching your criteria"
              />
              
              {/* Pagination */}
              <div className="flex items-center justify-between pt-6">
                <PageSizeSelector
                  pageSize={pageSize}
                  onPageSizeChange={handlePageSizeChange}
                />
                <Pagination
                  currentPage={page}
                  totalPages={totalPages}
                  onPageChange={handlePageChange}
                />
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
