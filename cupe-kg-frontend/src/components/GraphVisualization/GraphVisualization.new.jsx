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

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw edges
    edges.forEach(edge => {
      drawEdge(ctx, edge);
    });

    // Draw nodes
    nodes.forEach(node => {
      drawNode(ctx, node);
    });
  }, [edges, nodes]);

  const updatePhysics = useCallback(() => {
    const damping = 0.95;
    const repulsionStrength = 2000;
    const attractionStrength = 0.05;
    const centeringForce = 0.02;

    // Apply forces
    nodes.forEach(node1 => {
      node1.vx = (node1.vx || 0) * damping;
      node1.vy = (node1.vy || 0) * damping;

      // Repulsion between nodes
      nodes.forEach(node2 => {
        if (node1 === node2) return;

        const dx = node2.x - node1.x;
        const dy = node2.y - node1.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance === 0) return;

        const force = repulsionStrength / (distance * distance);
        const fx = (dx / distance) * force;
        const fy = (dy / distance) * force;

        node1.vx -= fx;
        node1.vy -= fy;
      });

      // Attraction along edges
      edges.forEach(edge => {
        if (edge.source === node1.id || edge.target === node1.id) {
          const otherNode = edge.source === node1.id 
            ? nodes.find(n => n.id === edge.target)
            : nodes.find(n => n.id === edge.source);

          if (!otherNode) return;

          const dx = otherNode.x - node1.x;
          const dy = otherNode.y - node1.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          node1.vx += dx * attractionStrength * edge.strength;
          node1.vy += dy * attractionStrength * edge.strength;
        }
      });

      // Centering force
      node1.vx += (canvas.width / 2 - node1.x) * centeringForce;
      node1.vy += (canvas.height / 2 - node1.y) * centeringForce;

      // Update position
      if (!node1.isFixed) {
        node1.x += node1.vx;
        node1.y += node1.vy;
      }
    });
  }, [nodes, edges]);

  const startAnimation = useCallback(() => {
    const animate = () => {
      updatePhysics();
      draw();
      animationRef.current = requestAnimationFrame(animate);
    };
    animate();
  }, [updatePhysics, draw]);

  const stopAnimation = useCallback(() => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
      animationRef.current = null;
    }
  }, []);

  const initializeGraph = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(canvas.width, canvas.height) * 0.3;

    // Create nodes
    const newNodes = locations.map((location, index) => {
      const angle = (index / locations.length) * 2 * Math.PI;
      return {
        id: location.id,
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
        radius: 20,
        color: location.category ? colors.category[location.category] : colors.category.default,
        data: location,
        connections: 0
      };
    });

    // Create edges
    const newEdges = [];
    newNodes.forEach((node1, i) => {
      newNodes.slice(i + 1).forEach(node2 => {
        const connectionStrength = calculateConnectionStrength(node1.data, node2.data);
        if (connectionStrength > 0.3) {
          newEdges.push({
            source: node1.id,
            target: node2.id,
            strength: connectionStrength
          });
          node1.connections++;
          node2.connections++;
        }
      });
    });

    // Update node sizes based on connections
    newNodes.forEach(node => {
      node.radius = Math.max(20, Math.min(40, 20 + node.connections * 3));
    });

    setNodes(newNodes);
    setEdges(newEdges);
  }, [locations, colors]);

  const calculateConnectionStrength = useCallback((loc1, loc2) => {
    let strength = 0;
    
    // Same dynasty
    if (loc1.dynasty && loc2.dynasty && loc1.dynasty === loc2.dynasty) {
      strength += 0.4;
    }
    
    // Same category
    if (loc1.category === loc2.category) {
      strength += 0.3;
    }
    
    // Period overlap
    if (loc1.period && loc2.period) {
      const overlap = calculatePeriodOverlap(loc1.period, loc2.period);
      strength += overlap * 0.3;
    }
    
    return Math.min(1, strength);
  }, []);

  const calculatePeriodOverlap = useCallback((period1, period2) => {
    // Simplified period overlap calculation
    // In a real application, you would parse and compare actual dates
    return period1 === period2 ? 1 : 0;
  }, []);

  const drawNode = useCallback((ctx, node) => {
    ctx.beginPath();
    ctx.arc(node.x, node.y, node.radius, 0, 2 * Math.PI);
    ctx.fillStyle = node.color;
    ctx.fill();
    ctx.strokeStyle = node === hoveredNode ? colors.hoveredNode : 'rgba(255,255,255,0.3)';
    ctx.lineWidth = 2;
    ctx.stroke();

    if (node.data.name) {
      ctx.fillStyle = colors.text;
      ctx.font = '12px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(node.data.name, node.x, node.y + node.radius + 15);
    }
  }, [hoveredNode, colors]);

  const drawEdge = useCallback((ctx, edge) => {
    const sourceNode = nodes.find(n => n.id === edge.source);
    const targetNode = nodes.find(n => n.id === edge.target);
    
    if (!sourceNode || !targetNode) return;

    ctx.beginPath();
    ctx.moveTo(sourceNode.x, sourceNode.y);
    ctx.lineTo(targetNode.x, targetNode.y);
    ctx.strokeStyle = colors.edge;
    ctx.lineWidth = edge.strength * 3;
    ctx.stroke();
  }, [nodes, colors]);

  useEffect(() => {
    if (locations.length > 0) {
      initializeGraph();
    }
  }, [locations, initializeGraph]);

  useEffect(() => {
    if (isVisible && nodes.length > 0) {
      startAnimation();
    } else {
      stopAnimation();
    }
    return () => stopAnimation();
  }, [isVisible, nodes.length, startAnimation, stopAnimation]);

  const handleMouseMove = useCallback((event) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Update hover state
    const hoveredNode = nodes.find(node => {
      const dx = x - node.x;
      const dy = y - node.y;
      return dx * dx + dy * dy < node.radius * node.radius;
    });

    setHoveredNode(hoveredNode || null);

    // Handle dragging
    if (isDragging && draggedNode) {
      draggedNode.x = x;
      draggedNode.y = y;
      draggedNode.isFixed = true;
    }
  }, [nodes, isDragging, draggedNode]);

  const handleMouseDown = useCallback((event) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const clickedNode = nodes.find(node => {
      const dx = x - node.x;
      const dy = y - node.y;
      return dx * dx + dy * dy < node.radius * node.radius;
    });

    if (clickedNode) {
      setDraggedNode(clickedNode);
      setIsDragging(true);
      if (onNodeClick) {
        onNodeClick(clickedNode.data);
      }
    }
  }, [nodes, onNodeClick]);

  const handleMouseUp = useCallback(() => {
    if (draggedNode) {
      draggedNode.isFixed = false;
    }
    setIsDragging(false);
    setDraggedNode(null);
  }, [draggedNode]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Set canvas size
    const updateSize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };

    updateSize();
    window.addEventListener('resize', updateSize);

    // Add event listeners
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mouseup', handleMouseUp);
    canvas.addEventListener('mouseleave', handleMouseUp);

    return () => {
      window.removeEventListener('resize', updateSize);
      canvas.removeEventListener('mousemove', handleMouseMove);
      canvas.removeEventListener('mousedown', handleMouseDown);
      canvas.removeEventListener('mouseup', handleMouseUp);
      canvas.removeEventListener('mouseleave', handleMouseUp);
    };
  }, [handleMouseMove, handleMouseDown, handleMouseUp]);

  return (
    <div className={`graph-visualization ${isVisible ? 'visible' : ''}`}>
      <canvas ref={canvasRef} className="graph-canvas" />
      {showLegend && (
        <div className="graph-legend">
          <h3>Legend</h3>
          <div className="legend-categories">
            {Object.entries(colors.category).map(([category, color]) => (
              category !== 'default' && (
                <div key={category} className="legend-item">
                  <span className="legend-color" style={{ backgroundColor: color }} />
                  <span className="legend-label">{category}</span>
                </div>
              )
            ))}
          </div>
        </div>
      )}
      <button className="close-button" onClick={onClose}>×</button>
    </div>
  );
};

export default GraphVisualization;
