'use client';

import { useState, useEffect, useCallback } from 'react';
import { useUser } from '@clerk/nextjs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { SearchBar } from '@/components/ui/search-bar';
import { DataTable, Pagination, PageSizeSelector } from '@/components/ui/data-table';
import apiClient from '@/lib/api';
import { Person, Company } from '@/types';
import { User, Building, Mail, Phone, Globe, Linkedin, Twitter, Github, Plus, Filter, Eye, MessageSquare, Share2, Briefcase, GraduationCap, MapPin } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { cn } from '@/lib/utils';

export default function PeoplePage() {
  const { user } = useUser();
  const [people, setPeople] = useState<Person[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [companyFilter, setCompanyFilter] = useState<string | null>(null);
  const [verifiedFilter, setVerifiedFilter] = useState<boolean | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [total, setTotal] = useState(0);
  const [sortBy, setSortBy] = useState<string | null>('last_name');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');

  const fetchPeople = useCallback(async () => {
    if (!user) return;

    try {
      setIsLoading(true);
      setError(null);

      // Get access token from Clerk
      const token = await user.getToken();

      // Fetch companies for filter
      const companiesResponse = await apiClient.companies.list(token, { limit: 100 });
      setCompanies(companiesResponse.items);

      // Fetch people with filters
      const response = await apiClient.people.list(token, {
        skip: (page - 1) * pageSize,
        limit: pageSize,
        search: searchQuery || undefined,
      });

      setPeople(response.items);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch people');
      console.error('Error fetching people:', err);
    } finally {
      setIsLoading(false);
    }
  }, [user, page, pageSize, searchQuery, companyFilter, verifiedFilter]);

  useEffect(() => {
    fetchPeople();
  }, [fetchPeople]);

  useEffect(() => {
    // Reset to first page when filters change
    setPage(1);
  }, [companyFilter, searchQuery, verifiedFilter]);

  const handleSort = useCallback((key: string, direction: 'asc' | 'desc') => {
    setSortBy(key);
    setSortDirection(direction);
    fetchPeople();
  }, [fetchPeople]);

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
  }, []);

  const handlePageChange = useCallback((newPage: number) => {
    setPage(newPage);
  }, []);

  const handlePageSizeChange = useCallback((size: number) => {
    setPageSize(size);
    setPage(1);
  }, []);

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'N/A';
    try {
      return formatDistanceToNow(new Date(dateString), { addSuffix: true });
    } catch {
      return dateString;
    }
  };

  const getInitials = (firstName: string, lastName: string | null) => {
    return `${firstName.charAt(0)}${lastName ? lastName.charAt(0) : ''}`.toUpperCase();
  };

  const columns = [
    {
      key: 'avatar',
      header: '',
      sortable: false,
      render: (person: Person) => (
        <Avatar className="h-10 w-10">
          <AvatarImage src={person.avatar_url || undefined} />
          <AvatarFallback>
            {getInitials(person.first_name, person.last_name)}
          </AvatarFallback>
        </Avatar>
      ),
      className: 'w-[60px]',
    },
    {
      key: 'name',
      header: 'Name',
      sortable: true,
      render: (person: Person) => (
        <div>
          <div className="font-medium">
            {person.first_name} {person.last_name}
          </div>
          <div className="text-sm text-muted-foreground">
            {person.current_title}
          </div>
        </div>
      ),
      className: 'min-w-[200px]',
    },
    {
      key: 'company',
      header: 'Company',
      sortable: true,
      render: (person: Person) => (
        <div className="text-sm">
          {person.current_company_id ? (
            <Badge variant="outline" className="gap-1">
              <Building className="h-3 w-3" />
              {companies.find(c => c.id === person.current_company_id)?.name || person.current_company_id}
            </Badge>
          ) : (
            <span className="text-muted-foreground">N/A</span>
          )}
        </div>
      ),
      className: 'w-[180px]',
    },
    {
      key: 'location',
      header: 'Location',
      sortable: true,
      render: (person: Person) => (
        <div className="text-sm">
          {person.city && person.country ? (
            <Badge variant="outline" className="gap-1">
              <MapPin className="h-3 w-3" />
              {person.city}, {person.country}
            </Badge>
          ) : (
            <span className="text-muted-foreground">N/A</span>
          )}
        </div>
      ),
      className: 'w-[150px]',
    },
    {
      key: 'contact',
      header: 'Contact',
      sortable: false,
      render: (person: Person) => (
        <div className="flex flex-wrap gap-1">
          {person.email && (
            <Badge variant="outline" className="gap-1 text-xs">
              <Mail className="h-3 w-3" />
              Email
            </Badge>
          )}
          {person.phone && (
            <Badge variant="outline" className="gap-1 text-xs">
              <Phone className="h-3 w-3" />
              Phone
            </Badge>
          )}
          {person.linkedin_url && (
            <Badge variant="outline" className="gap-1 text-xs">
              <Linkedin className="h-3 w-3" />
              LinkedIn
            </Badge>
          )}
          {!person.email && !person.phone && !person.linkedin_url && (
            <span className="text-muted-foreground text-xs">N/A</span>
          )}
        </div>
      ),
      className: 'w-[180px]',
    },
    {
      key: 'verified',
      header: 'Verified',
      sortable: true,
      render: (person: Person) => (
        <Badge variant={person.is_verified ? 'default' : 'secondary'}>
          {person.is_verified ? '✓ Verified' : '✗ Not Verified'}
        </Badge>
      ),
      className: 'w-[120px]',
    },
    {
      key: 'last_updated',
      header: 'Last Updated',
      sortable: true,
      render: (person: Person) => (
        <div className="text-sm text-muted-foreground whitespace-nowrap">
          {formatDate(person.last_updated_at || person.created_at)}
        </div>
      ),
      className: 'w-[140px]',
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
    { label: 'Total People', value: total, icon: User },
    { label: 'Verified', value: people.filter(p => p.is_verified).length, icon: User },
    { label: 'With Companies', value: people.filter(p => p.current_company_id).length, icon: Building },
    { label: 'With Contact Info', value: people.filter(p => p.email || p.phone || p.linkedin_url).length, icon: Mail },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">People</h1>
            <p className="text-muted-foreground">
              Manage and explore your professional connections
            </p>
          </div>
          <Button className="gap-1">
            <Plus className="h-4 w-4" />
            Add Person
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
            Narrow down people by company, verification status, and more
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <label className="text-sm font-medium">Company</label>
              <select
                value={companyFilter || ''}
                onChange={(e) => setCompanyFilter(e.target.value || null)}
                className="w-full h-10 px-3 py-2 text-sm border rounded-md bg-background"
              >
                <option value="">All Companies</option>
                {companies.map((company) => (
                  <option key={company.id} value={company.id}>
                    {company.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Verification Status</label>
              <select
                value={verifiedFilter === null ? '' : verifiedFilter ? 'true' : 'false'}
                onChange={(e) => setVerifiedFilter(e.target.value === 'true' ? true : e.target.value === 'false' ? false : null)}
                className="w-full h-10 px-3 py-2 text-sm border rounded-md bg-background"
              >
                <option value="">All Statuses</option>
                <option value="true">Verified Only</option>
                <option value="false">Not Verified Only</option>
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Search</label>
              <SearchBar
                placeholder="Search people..."
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
                setCompanyFilter(null);
                setVerifiedFilter(null);
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

      {/* People Table */}
      <Card>
        <CardHeader>
          <CardTitle>All People</CardTitle>
          <CardDescription>
            {total} people found
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
                data={people}
                keyExtractor={(person) => person.id}
                onSort={handleSort}
                sortBy={sortBy}
                sortDirection={sortDirection}
                isLoading={isLoading}
                emptyMessage="No people found matching your criteria"
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
