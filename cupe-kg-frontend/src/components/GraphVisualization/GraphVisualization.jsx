// src/components/GraphVisualization/GraphVisualization.jsx

import React, { useEffect, useRef, useState, useCallback } from 'react';
import { useMapContext } from '../../context/MapContext';
import './GraphVisualization.css';

const GraphVisualization = ({ isVisible, onNodeClick, onClose }) => {
  const canvasRef = useRef(null);
  const { locations, selectedLocation, selectLocation } = useMapContext();
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [hoveredNode, setHoveredNode] = useState(null);
  const [draggedNode, setDraggedNode] = useState(null);
  const [viewTransform, setViewTransform] = useState({ x: 0, y: 0, scale: 1 });
  const [isDragging, setIsDragging] = useState(false);
  const [lastMousePos, setLastMousePos] = useState({ x: 0, y: 0 });
  const animationRef = useRef(null);
  const [showLegend, setShowLegend] = useState(true);
  const [filterBy, setFilterBy] = useState('all'); // all, dynasty, category, period
  
  const colors = {
    dynasty: {
      'Mughal Empire': '#ff9800',
      'Vijayanagara Empire': '#4caf50', 
      'Chandela Dynasty': '#9c27b0',
      'Eastern Ganga Dynasty': '#f44336',
      'Satavahana and Vakataka': '#00bcd4',
      'Rashtrakuta Dynasty': '#795548',
      'Delhi Sultanate': '#607d8b',
      'default': '#757575'
    },
    category: {
      'historical': '#3f51b5',
      'religious': '#e91e63',
      'cultural': '#ff9800',
      'default': '#757575'
    },
    edge: 'rgba(255, 255, 255, 0.3)',
    text: '#ffffff',
    selectedNode: '#ffeb3b',
    hoveredNode: '#fff'
  };

  // Initialize graph data
  useEffect(() => {
    if (locations.length > 0) {
      initializeGraph();
    }
  }, [locations]);

  // Start animation loop
  useEffect(() => {
    if (isVisible && nodes.length > 0) {
      startAnimation();
    } else {
      stopAnimation();
    }
    
    return () => stopAnimation();
  }, [isVisible, nodes.length]);

  const initializeGraph = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // Create nodes from locations
    const newNodes = locations.map((location, index) => {
      const angle = (index / locations.length) * Math.PI * 2;
      const radius = Math.min(centerX, centerY) * 0.6;
      
      return {
        id: location.id,
        name: location.name,
        category: location.category,
        dynasty: location.dynasty,
        period: location.period,
        x: centerX + Math.cos(angle) * radius,
        y: centerY + Math.sin(angle) * radius,
        targetX: centerX + Math.cos(angle) * radius,
        targetY: centerY + Math.sin(angle) * radius,
        vx: 0,
        vy: 0,
        radius: 25,
        mass: 1,
        connections: 0,
        data: location
      };
    });

    // Create edges based on relationships
    const newEdges = [];
    
    newNodes.forEach((node1, i) => {
      newNodes.forEach((node2, j) => {
        if (i >= j) return; // Avoid duplicates and self-connections
        
        let connectionStrength = 0;
        let connectionType = [];
        
        // Same dynasty connection
        if (node1.dynasty === node2.dynasty && node1.dynasty) {
          connectionStrength += 0.8;
          connectionType.push('dynasty');
        }
        
        // Same category connection
        if (node1.category === node2.category) {
          connectionStrength += 0.6;
          connectionType.push('category');
        }
        
        // Period overlap (simplified)
        if (periodsOverlap(node1.period, node2.period)) {
          connectionStrength += 0.4;
          connectionType.push('period');
        }
        
        // Cultural similarity (based on tags/keywords)
        const culturalSimilarity = calculateCulturalSimilarity(node1.data, node2.data);
        if (culturalSimilarity > 0.3) {
          connectionStrength += culturalSimilarity * 0.5;
          connectionType.push('cultural');
        }
        
        // Create edge if connection is strong enough
        if (connectionStrength > 0.3) {
          newEdges.push({
            source: node1.id,
            target: node2.id,
            strength: Math.min(connectionStrength, 1),
            type: connectionType,
            sourceNode: node1,
            targetNode: node2
          });
          
          node1.connections++;
          node2.connections++;
        }
      });
    });

    // Adjust node sizes based on connections
    newNodes.forEach(node => {
      node.radius = Math.max(20, Math.min(40, 20 + node.connections * 3));
    });

    setNodes(newNodes);
    setEdges(newEdges);
  };

  const periodsOverlap = (period1, period2) => {
    if (!period1 || !period2) return false;
    
    // Extract years from periods (simplified)
    const extractYear = (period) => {
      const match = period.match(/(\d{1,4})/);
      return match ? parseInt(match[1]) : null;
    };
    
    const year1 = extractYear(period1);
    const year2 = extractYear(period2);
    
    if (!year1 || !year2) return false;
    
    // Consider periods overlapping if within 200 years
    return Math.abs(year1 - year2) < 200;
  };

  const calculateCulturalSimilarity = (loc1, loc2) => {
    const tags1 = loc1.tags || [];
    const tags2 = loc2.tags || [];
    
    if (tags1.length === 0 || tags2.length === 0) return 0;
    
    const commonTags = tags1.filter(tag => tags2.includes(tag));
    return commonTags.length / Math.max(tags1.length, tags2.length);
  };

  const startAnimation = () => {
    const animate = () => {
      updatePhysics();
      draw();
      animationRef.current = requestAnimationFrame(animate);
    };
    animate();
  };

  const stopAnimation = () => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
      animationRef.current = null;
    }
  };

  const updatePhysics = () => {
    const damping = 0.95;
    const repulsionStrength = 2000;
    const attractionStrength = 0.05;
    const centeringForce = 0.02;

    setNodes(prevNodes => {
      const newNodes = [...prevNodes];
      
      // Apply forces
      newNodes.forEach((node, i) => {
        if (node.id === draggedNode?.id) return; // Skip dragged node
        
        let fx = 0, fy = 0;
        
        // Repulsion from other nodes
        newNodes.forEach((other, j) => {
          if (i === j) return;
          const dx = node.x - other.x;
          const dy = node.y - other.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance > 0) {
            const force = repulsionStrength / (distance * distance);
            fx += (dx / distance) * force;
            fy += (dy / distance) * force;
          }
        });
        
        // Attraction along edges
        edges.forEach(edge => {
          let other = null;
          let direction = 1;
          
          if (edge.sourceNode.id === node.id) {
            other = edge.targetNode;
          } else if (edge.targetNode.id === node.id) {
            other = edge.sourceNode;
            direction = -1;
          }
          
          if (other) {
            const dx = other.x - node.x;
            const dy = other.y - node.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            const idealDistance = 150 * (1 - edge.strength * 0.5);
            
            if (distance > idealDistance) {
              const force = attractionStrength * edge.strength * (distance - idealDistance);
              fx += (dx / distance) * force * direction;
              fy += (dy / distance) * force * direction;
            }
          }
        });
        
        // Centering force
        const canvas = canvasRef.current;
        if (canvas) {
          const centerX = canvas.width / 2;
          const centerY = canvas.height / 2;
          const dx = centerX - node.x;
          const dy = centerY - node.y;
          fx += dx * centeringForce;
          fy += dy * centeringForce;
        }
        
        // Update velocity and position
        node.vx = (node.vx + fx) * damping;
        node.vy = (node.vy + fy) * damping;
        
        node.x += node.vx;
        node.y += node.vy;
        
        // Boundary constraints
        if (canvas) {
          const margin = node.radius;
          node.x = Math.max(margin, Math.min(canvas.width - margin, node.x));
          node.y = Math.max(margin, Math.min(canvas.height - margin, node.y));
        }
      });
      
      return newNodes;
    });
  };

  const draw = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Apply transform
    ctx.save();
    ctx.translate(viewTransform.x, viewTransform.y);
    ctx.scale(viewTransform.scale, viewTransform.scale);
    
    // Draw edges
    edges.forEach(edge => {
      if (shouldShowEdge(edge)) {
        drawEdge(ctx, edge);
      }
    });
    
    // Draw nodes
    nodes.forEach(node => {
      if (shouldShowNode(node)) {
        drawNode(ctx, node);
      }
    });
    
    ctx.restore();
  };

  const shouldShowNode = (node) => {
    if (filterBy === 'all') return true;
    if (filterBy === 'dynasty') return node.dynasty;
    if (filterBy === 'category') return node.category;
    if (filterBy === 'period') return node.period;
    return true;
  };

  const shouldShowEdge = (edge) => {
    return shouldShowNode(edge.sourceNode) && shouldShowNode(edge.targetNode);
  };

  const drawEdge = (ctx, edge) => {
    const { sourceNode, targetNode, strength, type } = edge;
    
    ctx.beginPath();
    ctx.moveTo(sourceNode.x, sourceNode.y);
    ctx.lineTo(targetNode.x, targetNode.y);
    
    // Edge styling based on type
    let strokeStyle = colors.edge;
    let lineWidth = 2;
    
    if (type.includes('dynasty')) {
      strokeStyle = 'rgba(255, 152, 0, 0.6)';
      lineWidth = 3;
    } else if (type.includes('category')) {
      strokeStyle = 'rgba(63, 81, 181, 0.4)';
      lineWidth = 2;
    } else if (type.includes('cultural')) {
      strokeStyle = 'rgba(233, 30, 99, 0.4)';
      lineWidth = 2;
    }
    
    ctx.strokeStyle = strokeStyle;
    ctx.lineWidth = lineWidth * strength;
    ctx.stroke();
  };

  const drawNode = (ctx, node) => {
    const isSelected = selectedLocation?.id === node.id;
    const isHovered = hoveredNode?.id === node.id;
    
    // Node color based on current filter
    let nodeColor = colors.category.default;
    if (filterBy === 'dynasty') {
      nodeColor = colors.dynasty[node.dynasty] || colors.dynasty.default;
    } else if (filterBy === 'category') {
      nodeColor = colors.category[node.category] || colors.category.default;
    } else {
      nodeColor = colors.category[node.category] || colors.category.default;
    }
    
    // Draw node circle
    ctx.beginPath();
    ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
    
    if (isSelected) {
      ctx.fillStyle = colors.selectedNode;
      ctx.shadowBlur = 20;
      ctx.shadowColor = colors.selectedNode;
    } else if (isHovered) {
      ctx.fillStyle = colors.hoveredNode;
      ctx.shadowBlur = 15;
      ctx.shadowColor = nodeColor;
    } else {
      ctx.fillStyle = nodeColor;
      ctx.shadowBlur = 10;
      ctx.shadowColor = nodeColor;
    }
    
    ctx.fill();
    ctx.shadowBlur = 0;
    
    // Draw border
    ctx.beginPath();
    ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
    ctx.strokeStyle = isSelected ? '#fff' : 'rgba(255, 255, 255, 0.8)';
    ctx.lineWidth = isSelected ? 3 : 2;
    ctx.stroke();
    
    // Draw node label
    ctx.fillStyle = colors.text;
    ctx.font = `${isHovered || isSelected ? '14px' : '12px'} Arial`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Text with shadow for readability
    ctx.shadowBlur = 3;
    ctx.shadowColor = 'rgba(0, 0, 0, 0.7)';
    ctx.fillText(node.name, node.x, node.y);
    ctx.shadowBlur = 0;
    
    // Draw connection count
    if (isHovered || isSelected) {
      ctx.font = '10px Arial';
      ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
      ctx.fillText(
        `${node.connections} connections`, 
        node.x, 
        node.y + node.radius + 15
      );
    }
  };

  // Mouse event handlers
  const handleMouseDown = useCallback((e) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left - viewTransform.x) / viewTransform.scale;
    const y = (e.clientY - rect.top - viewTransform.y) / viewTransform.scale;
    
    // Check if clicking on a node
    const clickedNode = nodes.find(node => {
      const dx = x - node.x;
      const dy = y - node.y;
      return Math.sqrt(dx * dx + dy * dy) < node.radius;
    });
    
    if (clickedNode) {
      setDraggedNode(clickedNode);
      selectLocation(clickedNode.data);
      if (onNodeClick) {
        onNodeClick(clickedNode.data);
      }
    } else {
      setIsDragging(true);
      setLastMousePos({ x: e.clientX, y: e.clientY });
    }
  }, [nodes, viewTransform, selectLocation, onNodeClick]);

  const handleMouseMove = useCallback((e) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    if (isDragging) {
      const dx = e.clientX - lastMousePos.x;
      const dy = e.clientY - lastMousePos.y;
      
      setViewTransform(prev => ({
        ...prev,
        x: prev.x + dx,
        y: prev.y + dy
      }));
      
      setLastMousePos({ x: e.clientX, y: e.clientY });
    } else if (draggedNode) {
      const rect = canvas.getBoundingClientRect();
      const x = (e.clientX - rect.left - viewTransform.x) / viewTransform.scale;
      const y = (e.clientY - rect.top - viewTransform.y) / viewTransform.scale;
      
      setNodes(prev => prev.map(node => 
        node.id === draggedNode.id 
          ? { ...node, x, y, vx: 0, vy: 0 }
          : node
      ));
    } else {
      // Check for hover
      const rect = canvas.getBoundingClientRect();
      const x = (e.clientX - rect.left - viewTransform.x) / viewTransform.scale;
      const y = (e.clientY - rect.top - viewTransform.y) / viewTransform.scale;
      
      const hoveredNode = nodes.find(node => {
        const dx = x - node.x;
        const dy = y - node.y;
        return Math.sqrt(dx * dx + dy * dy) < node.radius;
      });
      
      setHoveredNode(hoveredNode || null);
      canvas.style.cursor = hoveredNode ? 'pointer' : 'default';
    }
  }, [isDragging, draggedNode, lastMousePos, nodes, viewTransform]);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
    setDraggedNode(null);
  }, []);

  const handleWheel = useCallback((e) => {
    e.preventDefault();
    const scaleChange = e.deltaY > 0 ? 0.9 : 1.1;
    
    setViewTransform(prev => ({
      ...prev,
      scale: Math.max(0.1, Math.min(3, prev.scale * scaleChange))
    }));
  }, []);

  // Setup event listeners
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseup', handleMouseUp);
    canvas.addEventListener('wheel', handleWheel);
    
    return () => {
      canvas.removeEventListener('mousedown', handleMouseDown);
      canvas.removeEventListener('mousemove', handleMouseMove);
      canvas.removeEventListener('mouseup', handleMouseUp);
      canvas.removeEventListener('wheel', handleWheel);
    };
  }, [handleMouseDown, handleMouseMove, handleMouseUp, handleWheel]);

  // Reset view
  const resetView = () => {
    setViewTransform({ x: 0, y: 0, scale: 1 });
  };

  if (!isVisible) return null;

  return (
    <div className="graph-visualization">
      <div className="graph-header">
        <h2>Cultural Heritage Knowledge Graph</h2>
        <div className="graph-controls">
          <select 
            value={filterBy} 
            onChange={(e) => setFilterBy(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Connections</option>
            <option value="dynasty">By Dynasty</option>
            <option value="category">By Category</option>
            <option value="period">By Period</option>
          </select>
          
          <button onClick={() => setShowLegend(!showLegend)} className="legend-toggle">
            {showLegend ? 'Hide' : 'Show'} Legend
          </button>
          
          <button onClick={resetView} className="reset-view">
            Reset View
          </button>
          
          <button onClick={onClose} className="close-graph">
            ×
          </button>
        </div>
      </div>
      
      <canvas
        ref={canvasRef}
        width={800}
        height={600}
        className="graph-canvas"
      />
      
      {showLegend && (
        <div className="graph-legend">
          <h3>Legend</h3>
          <div className="legend-section">
            <h4>Node Colors ({filterBy})</h4>
            {filterBy === 'category' && (
              <div className="legend-items">
                <div className="legend-item">
                  <div className="legend-color" style={{ backgroundColor: colors.category.historical }}></div>
                  <span>Historical</span>
                </div>
                <div className="legend-item">
                  <div className="legend-color" style={{ backgroundColor: colors.category.religious }}></div>
                  <span>Religious</span>
                </div>
                <div className="legend-item">
                  <div className="legend-color" style={{ backgroundColor: colors.category.cultural }}></div>
                  <span>Cultural</span>
                </div>
              </div>
            )}
            
            {filterBy === 'dynasty' && (
              <div className="legend-items">
                {Object.entries(colors.dynasty).slice(0, -1).map(([dynasty, color]) => (
                  <div key={dynasty} className="legend-item">
                    <div className="legend-color" style={{ backgroundColor: color }}></div>
                    <span>{dynasty}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <div className="legend-section">
            <h4>Edge Types</h4>
            <div className="legend-items">
              <div className="legend-item">
                <div className="legend-line" style={{ backgroundColor: 'rgba(255, 152, 0, 0.6)' }}></div>
                <span>Dynasty</span>
              </div>
              <div className="legend-item">
                <div className="legend-line" style={{ backgroundColor: 'rgba(63, 81, 181, 0.4)' }}></div>
                <span>Category</span>
              </div>
              <div className="legend-item">
                <div className="legend-line" style={{ backgroundColor: 'rgba(233, 30, 99, 0.4)' }}></div>
                <span>Cultural</span>
              </div>
            </div>
          </div>
          
          <div className="interaction-help">
            <p><strong>Interactions:</strong></p>
            <p>• Click nodes to select locations</p>
            <p>• Drag nodes to reposition</p>
            <p>• Drag canvas to pan view</p>
            <p>• Scroll to zoom in/out</p>
          </div>
        </div>
      )}
      
      <div className="graph-stats">
        <div className="stat">
          <span className="stat-value">{nodes.length}</span>
          <span className="stat-label">Heritage Sites</span>
        </div>
        <div className="stat">
          <span className="stat-value">{edges.length}</span>
          <span className="stat-label">Connections</span>
        </div>
        {selectedLocation && (
          <div className="stat">
            <span className="stat-value">{nodes.find(n => n.id === selectedLocation.id)?.connections || 0}</span>
            <span className="stat-label">Related Sites</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default GraphVisualization;