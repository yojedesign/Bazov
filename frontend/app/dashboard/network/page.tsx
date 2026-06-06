'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useUser } from '@clerk/nextjs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { SearchBar } from '@/components/ui/search-bar';
import apiClient from '@/lib/api';
import { Person, Company, Relationship, GraphData, GraphNode, GraphEdge } from '@/types';
import { User, Building, Network, Search, Filter, Eye, MessageSquare, Share2, ZoomIn, ZoomOut, RotateCcw, Download, Users, Link2 } from 'lucide-react';
import { cn, generateInitials } from '@/lib/utils';

// Network visualization component using SVG
function NetworkGraph({
  nodes,
  edges,
  onNodeClick,
  onNodeHover,
  className,
}: {
  nodes: GraphNode[];
  edges: GraphEdge[];
  onNodeClick?: (node: GraphNode) => void;
  onNodeHover?: (node: GraphNode | null) => void;
  className?: string;
}) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
  const [transform, setTransform] = useState({ x: 0, y: 0, scale: 1 });
  const [dragging, setDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  // Simple force-directed layout simulation
  const [positions, setPositions] = useState<Record<string, { x: number; y: number }>>({});

  useEffect(() => {
    // Initialize positions in a circle
    const newPositions: Record<string, { x: number; y: number }> = {};
    const centerX = dimensions.width / 2;
    const centerY = dimensions.height / 2;
    const radius = Math.min(dimensions.width, dimensions.height) * 0.4;

    nodes.forEach((node, index) => {
      const angle = (2 * Math.PI * index) / nodes.length;
      newPositions[node.id] = {
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
      };
    });

    setPositions(newPositions);
  }, [nodes, dimensions]);

  // Simulate force-directed layout
  useEffect(() => {
    if (nodes.length === 0) return;

    const centerX = dimensions.width / 2;
    const centerY = dimensions.height / 2;

    // Simple repulsion and attraction simulation
    const newPositions = { ...positions };
    const repulsion = 10000;
    const stiffness = 0.1;
    const damping = 0.8;

    // Apply repulsion between all nodes
    nodes.forEach((nodeA, i) => {
      nodes.forEach((nodeB, j) => {
        if (i === j) return;

        const posA = newPositions[nodeA.id] || { x: centerX, y: centerY };
        const posB = newPositions[nodeB.id] || { x: centerX, y: centerY };

        const dx = posB.x - posA.x;
        const dy = posB.y - posA.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance > 0) {
          const force = repulsion / (distance * distance);
          const fx = (dx / distance) * force;
          const fy = (dy / distance) * force;

          newPositions[nodeA.id] = {
            x: posA.x - fx,
            y: posA.y - fy,
          };
          newPositions[nodeB.id] = {
            x: posB.x + fx,
            y: posB.y + fy,
          };
        }
      });
    });

    // Apply attraction along edges
    edges.forEach((edge) => {
      const posA = newPositions[edge.source] || { x: centerX, y: centerY };
      const posB = newPositions[edge.target] || { x: centerX, y: centerY };

      const dx = posB.x - posA.x;
      const dy = posB.y - posA.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance > 0) {
        const force = stiffness * (distance - 100);
        const fx = (dx / distance) * force;
        const fy = (dy / distance) * force;

        newPositions[edge.source] = {
          x: posA.x + fx,
          y: posA.y + fy,
        };
        newPositions[edge.target] = {
          x: posB.x - fx,
          y: posB.y - fy,
        };
      }
    });

    // Apply damping and center gravity
    nodes.forEach((node) => {
      const pos = newPositions[node.id] || { x: centerX, y: centerY };
      const dx = centerX - pos.x;
      const dy = centerY - pos.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance > dimensions.width * 0.4) {
        newPositions[node.id] = {
          x: pos.x + dx * 0.01,
          y: pos.y + dy * 0.01,
        };
      }
    });

    setPositions(newPositions);
  }, [nodes, edges, dimensions]);

  const handleWheel = useCallback((e: WheelEvent) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? 0.9 : 1.1;
    setTransform((prev) => ({
      ...prev,
      scale: Math.max(0.1, Math.min(10, prev.scale * delta)),
    }));
  }, []);

  const handleMouseDown = useCallback((e: React.MouseEvent<SVGSVGElement>) => {
    if (e.button === 0) {
      setDragging(true);
      setDragStart({ x: e.clientX - transform.x, y: e.clientY - transform.y });
    }
  }, [transform]);

  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (dragging) {
      setTransform((prev) => ({
        ...prev,
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y,
      }));
    }
  }, [dragging, dragStart]);

  const handleMouseUp = useCallback(() => {
    setDragging(false);
  }, []);

  useEffect(() => {
    const svg = svgRef.current;
    if (!svg) return;

    svg.addEventListener('wheel', handleWheel);
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    return () => {
      svg.removeEventListener('wheel', handleWheel);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [handleWheel, handleMouseMove, handleMouseUp]);

  const handleResetView = () => {
    setTransform({ x: 0, y: 0, scale: 1 });
  };

  const handleZoomIn = () => {
    setTransform((prev) => ({ ...prev, scale: Math.min(10, prev.scale * 1.2) }));
  };

  const handleZoomOut = () => {
    setTransform((prev) => ({ ...prev, scale: Math.max(0.1, prev.scale / 1.2) }));
  };

  // Get node color based on type
  const getNodeColor = (node: GraphNode) => {
    switch (node.type) {
      case 'person':
        return '#3b82f6';
      case 'company':
        return '#10b981';
      default:
        return '#6b7280';
    }
  };

  // Get edge color based on type
  const getEdgeColor = (edge: GraphEdge) => {
    switch (edge.type) {
      case 'colleague':
        return '#3b82f6';
      case 'friend':
        return '#10b981';
      case 'family':
        return '#ef4444';
      case 'business':
        return '#8b5cf6';
      default:
        return '#6b7280';
    }
  };

  return (
    <div className={cn('relative w-full h-[600px] bg-muted/50 rounded-lg overflow-hidden', className)}>
      <svg
        ref={svgRef}
        width="100%"
        height="100%"
        viewBox={`0 0 ${dimensions.width} ${dimensions.height}`}
        onMouseDown={handleMouseDown}
        className="cursor-grab active:cursor-grabbing"
      >
        <defs>
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="9"
            refY="3.5"
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" fill="#6b7280" />
          </marker>
        </defs>

        {/* Edges */}
        <g transform={`translate(${transform.x}, ${transform.y}) scale(${transform.scale})`}>
          {edges.map((edge, index) => {
            const sourcePos = positions[edge.source] || { x: dimensions.width / 2, y: dimensions.height / 2 };
            const targetPos = positions[edge.target] || { x: dimensions.width / 2, y: dimensions.height / 2 };
            const color = getEdgeColor(edge);

            return (
              <g key={`edge-${edge.id || index}`}>
                <line
                  x1={sourcePos.x}
                  y1={sourcePos.y}
                  x2={targetPos.x}
                  y2={targetPos.y}
                  stroke={color}
                  strokeWidth={1.5 / transform.scale}
                  strokeOpacity={0.6}
                  markerEnd="url(#arrowhead)"
                />
              </g>
            );
          })}

          {/* Nodes */}
          {nodes.map((node, index) => {
            const pos = positions[node.id] || { x: dimensions.width / 2, y: dimensions.height / 2 };
            const color = getNodeColor(node);

            return (
              <g
                key={`node-${node.id}`}
                transform={`translate(${pos.x}, ${pos.y})`}
                onClick={() => onNodeClick?.(node)}
                onMouseEnter={() => onNodeHover?.(node)}
                onMouseLeave={() => onNodeHover?.(null)}
                className="cursor-pointer hover:scale-110 transition-transform"
              >
                {/* Glow effect */}
                <circle
                  cx={0}
                  cy={0}
                  r={node.type === 'person' ? 20 : 25}
                  fill={color}
                  opacity={0.2}
                  filter="url(#glow)"
                />
                
                {/* Main node */}
                <circle
                  cx={0}
                  cy={0}
                  r={node.type === 'person' ? 16 : 20}
                  fill={color}
                  stroke="white"
                  strokeWidth={2}
                />

                {/* Avatar for person nodes */}
                {node.type === 'person' && node.avatar && (
                  <image
                    href={node.avatar}
                    x={-12}
                    y={-12}
                    width={24}
                    height={24}
                    clipPath="circle(12px at 0 0)"
                  />
                )}

                {/* Label */}
                <text
                  x={0}
                  y={node.type === 'person' ? 25 : 30}
                  textAnchor="middle"
                  className="text-xs fill-white font-medium"
                  style={{ pointerEvents: 'none' }}
                >
                  {node.label.length > 12 ? `${node.label.substring(0, 10)}...` : node.label}
                </text>
              </g>
            );
          })}
        </g>
      </svg>

      {/* Controls */}
      <div className="absolute top-4 left-4 flex gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={handleZoomIn}
          className="h-8 w-8 p-0"
        >
          <ZoomIn className="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={handleZoomOut}
          className="h-8 w-8 p-0"
        >
          <ZoomOut className="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={handleResetView}
          className="h-8 w-8 p-0"
        >
          <RotateCcw className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}

export default function NetworkPage() {
  const { user } = useUser();
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], edges: [] });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [depth, setDepth] = useState(2);
  const [includeCompanies, setIncludeCompanies] = useState(true);

  const fetchGraph = useCallback(async () => {
    if (!user) return;

    try {
      setIsLoading(true);
      setError(null);

      // Get access token from Clerk
      const token = await user.getToken();

      // Fetch graph data from API
      const response = await apiClient.relationships.getGraph(token, {
        depth,
        include_companies: includeCompanies,
      });

      setGraphData(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch network data');
      console.error('Error fetching network:', err);
    } finally {
      setIsLoading(false);
    }
  }, [user, depth, includeCompanies]);

  useEffect(() => {
    fetchGraph();
  }, [fetchGraph]);

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
  }, []);

  const handleNodeClick = useCallback((node: GraphNode) => {
    setSelectedNode(node);
  }, []);

  const handleNodeHover = useCallback((node: GraphNode | null) => {
    // Could highlight connected nodes/edges
  }, []);

  // Stats for the page
  const stats = [
    { label: 'Total Nodes', value: graphData.nodes.length, icon: Users },
    { label: 'Total Connections', value: graphData.edges.length, icon: Link2 },
    { label: 'People', value: graphData.nodes.filter(n => n.type === 'person').length, icon: User },
    { label: 'Companies', value: graphData.nodes.filter(n => n.type === 'company').length, icon: Building },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Network</h1>
            <p className="text-muted-foreground">
              Visualize and explore your professional relationships
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" className="gap-1">
              <Download className="h-4 w-4" />
              Export
            </Button>
          </div>
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

      {/* Controls */}
      <Card>
        <CardHeader>
          <CardTitle>Network Controls</CardTitle>
          <CardDescription>
            Customize your network visualization
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <label className="text-sm font-medium">Search</label>
              <SearchBar
                placeholder="Search nodes..."
                onSearch={handleSearch}
                className="w-full"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Connection Depth</label>
              <select
                value={depth}
                onChange={(e) => setDepth(Number(e.target.value))}
                className="w-full h-10 px-3 py-2 text-sm border rounded-md bg-background"
              >
                <option value={1}>1st Degree</option>
                <option value={2}>2nd Degree</option>
                <option value={3}>3rd Degree</option>
                <option value={4}>4th Degree</option>
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Include Companies</label>
              <select
                value={includeCompanies ? 'true' : 'false'}
                onChange={(e) => setIncludeCompanies(e.target.value === 'true')}
                className="w-full h-10 px-3 py-2 text-sm border rounded-md bg-background"
              >
                <option value="true">Yes</option>
                <option value="false">No</option>
              </select>
            </div>
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={fetchGraph}
              className="gap-1"
            >
              <Filter className="h-4 w-4" />
              Refresh Network
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Network Visualization */}
      <Card>
        <CardHeader>
          <CardTitle>Network Graph</CardTitle>
          <CardDescription>
            Interactive visualization of your professional relationships
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error ? (
            <div className="flex items-center justify-center py-12 text-destructive">
              {error}
            </div>
          ) : isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
              <span className="ml-3 text-muted-foreground">Loading network...</span>
            </div>
          ) : graphData.nodes.length === 0 ? (
            <div className="flex items-center justify-center py-12 text-muted-foreground">
              No network data available. Try adjusting your filters.
            </div>
          ) : (
            <>
              <NetworkGraph
                nodes={graphData.nodes}
                edges={graphData.edges}
                onNodeClick={handleNodeClick}
                onNodeHover={handleNodeHover}
              />

              {/* Node Details Panel */}
              {selectedNode && (
                <Card className="mt-4">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Network className="h-5 w-5" />
                      {selectedNode.label}
                    </CardTitle>
                    <CardDescription>
                      {selectedNode.type === 'person' ? 'Person' : 'Company'}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center gap-4">
                        {selectedNode.type === 'person' ? (
                          <Avatar className="h-16 w-16">
                            <AvatarImage src={selectedNode.avatar || undefined} />
                            <AvatarFallback>
                              {generateInitials(selectedNode.label)}
                            </AvatarFallback>
                          </Avatar>
                        ) : (
                          <div className="h-16 w-16 rounded-lg bg-emerald-100 flex items-center justify-center">
                            <Building className="h-8 w-8 text-emerald-600" />
                          </div>
                        )}
                        <div>
                          <h3 className="font-semibold text-lg">{selectedNode.label}</h3>
                          <Badge variant={selectedNode.type === 'person' ? 'default' : 'outline'}>
                            {selectedNode.type}
                          </Badge>
                        </div>
                      </div>
                      
                      <div className="grid gap-2">
                        <div className="flex items-center gap-2">
                          <Users className="h-4 w-4 text-muted-foreground" />
                          <span className="text-sm">
                            {graphData.edges.filter(e => e.source === selectedNode.id || e.target === selectedNode.id).length} connections
                          </span>
                        </div>
                        {selectedNode.properties?.title && (
                          <div className="flex items-center gap-2">
                            <Briefcase className="h-4 w-4 text-muted-foreground" />
                            <span className="text-sm">{selectedNode.properties.title}</span>
                          </div>
                        )}
                        {selectedNode.properties?.company && (
                          <div className="flex items-center gap-2">
                            <Building className="h-4 w-4 text-muted-foreground" />
                            <span className="text-sm">{selectedNode.properties.company}</span>
                          </div>
                        )}
                      </div>

                      <div className="flex gap-2">
                        <Button variant="outline" size="sm" className="gap-1 flex-1">
                          <Eye className="h-4 w-4" />
                          View Profile
                        </Button>
                        <Button variant="outline" size="sm" className="gap-1 flex-1">
                          <MessageSquare className="h-4 w-4" />
                          Message
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}
            </>
          )}
        </CardContent>
      </Card>

      {/* Legend */}
      <Card>
        <CardHeader>
          <CardTitle>Legend</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center gap-2">
              <div className="h-4 w-4 rounded-full bg-blue-500" />
              <span className="text-sm">Person</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-4 w-4 rounded-full bg-emerald-500" />
              <span className="text-sm">Company</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-4 w-16 border-t-2 border-blue-500" />
              <span className="text-sm">Colleague</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-4 w-16 border-t-2 border-emerald-500" />
              <span className="text-sm">Business</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-4 w-16 border-t-2 border-purple-500" />
              <span className="text-sm">Friend</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
