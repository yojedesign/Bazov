// User types
export interface User {
  id: string;
  clerk_id: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
  username: string | null;
  avatar_url: string | null;
  theme: string;
  language: string;
  timezone: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  last_login_at: string | null;
}

// Company types
export interface Company {
  id: string;
  name: string;
  domain: string | null;
  industry: string | null;
  size: string | null;
  founded_year: number | null;
  description: string | null;
  logo_url: string | null;
  website_url: string | null;
  linkedin_url: string | null;
  twitter_url: string | null;
  city: string | null;
  state: string | null;
  country: string | null;
  address: string | null;
  revenue_range: string | null;
  funding_stage: string | null;
  last_funding_date: string | null;
  last_funding_amount: number | null;
  is_public: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

// Person types
export interface Person {
  id: string;
  linkedin_id: string | null;
  twitter_id: string | null;
  github_id: string | null;
  first_name: string;
  last_name: string;
  full_name: string | null;
  current_title: string | null;
  current_company_id: string | null;
  bio: string | null;
  summary: string | null;
  profile_url: string | null;
  avatar_url: string | null;
  linkedin_url: string | null;
  twitter_url: string | null;
  github_url: string | null;
  personal_website: string | null;
  email: string | null;
  phone: string | null;
  city: string | null;
  state: string | null;
  country: string | null;
  education: string | null;
  skills: string | null;
  experience: string | null;
  is_public: boolean;
  is_verified: boolean;
  last_updated_at: string | null;
  created_at: string;
  updated_at: string;
}

// Relationship types
export interface Relationship {
  id: string;
  from_person_id: string;
  to_person_id: string;
  relationship_type: string;
  from_date: string | null;
  to_date: string | null;
  current: boolean;
  source: string;
  source_url: string | null;
  notes: string | null;
  strength: number | null;
  created_at: string;
  updated_at: string;
}

// Signal types
export interface Signal {
  id: string;
  signal_type: string;
  title: string;
  content: string;
  summary: string | null;
  source_url: string | null;
  source_type: string;
  source_author: string | null;
  source_published_at: string | null;
  company_id: string | null;
  person_id: string | null;
  confidence: number;
  sentiment: string;
  sentiment_score: number | null;
  categories: string | null;
  tags: string | null;
  is_processed: boolean;
  processed_at: string | null;
  created_at: string;
  updated_at: string;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

// Graph types
export interface GraphNode {
  id: string;
  label: string;
  type: 'person' | 'company';
  avatar?: string;
  properties?: Record<string, any>;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  label?: string;
  properties?: Record<string, any>;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface PathNode {
  id: string;
  label: string;
  type: 'person' | 'company';
}

export interface PathEdge {
  source: string;
  target: string;
  type: string;
}

export interface RelationshipPath {
  nodes: PathNode[];
  edges: PathEdge[];
  distance: number;
}

// Request types
export interface GraphRequest {
  person_ids?: string[];
  company_ids?: string[];
  depth?: number;
  include_companies?: boolean;
}

export interface PathRequest {
  from_person_id: string;
  to_person_id: string;
  max_depth?: number;
}

// UI State types
export interface ToastMessage {
  id: string;
  title: string;
  description?: string;
  variant: 'default' | 'destructive' | 'success' | 'warning' | 'info';
  duration?: number;
}

export interface ModalState {
  isOpen: boolean;
  type: string;
  data?: any;
}

// Filter types
export interface SignalFilter {
  signal_type?: string;
  company_id?: string;
  person_id?: string;
  date_range?: {
    start: string;
    end: string;
  };
  sentiment?: string;
  confidence_min?: number;
}

export interface RelationshipFilter {
  relationship_type?: string;
  from_person_id?: string;
  to_person_id?: string;
  current?: boolean;
  date_range?: {
    start: string;
    end: string;
  };
}

export interface PersonFilter {
  company_id?: string;
  search?: string;
  is_verified?: boolean;
}

export interface CompanyFilter {
  industry?: string;
  size?: string;
  search?: string;
  is_verified?: boolean;
}
