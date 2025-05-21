// components/GraphVisualization/GraphVisualization.jsx

import React, { useEffect, useRef, useState } from 'react';
import { useMapContext } from '../../context/MapContext';
import './GraphVisualization.css';

const GraphVisualization = ({ isVisible, onNodeClick }) => {
  const canvasRef = useRef(null);
  const { locations } = useMapContext();
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [hoveredNode, setHoveredNode] = useState(null);
  const [activeNode, setActiveNode] = useState(null);
  const animationRef = useRef(null);
  
  const colors = {
    historical: '#E91E63', // Pink
    cultural: '#4CAF50',   // Green
    religious: '#FFC107',  // Amber
    node: '#3f51b5',       // Default node
    edge: 'rgba(255, 255, 255, 0.2)',
    text: '#ffffff'
  };

  // Generate nodes and edges from location data
  useEffect(() => {
    if (!locations.length) return;
    
    // Create nodes from locations
    const newNodes = locations.map((location, index) => {
      // Generate a position based on category (cluster similar types)
      const angle = (index / locations.length) * Math.PI * 2;
      const radius = 150 + (Math.random() * 100);
      
      return {
        id: location.id,
        name: location.name,
        category: location.category,
        x: Math.cos(angle) * radius + 400, // center x
        y: Math.sin(angle) * radius + 300, // center y
        radius: 20,
        color: colors[location.category] || colors.node,
        adjacentNodes: [],
        vx: 0,  // Added velocity for force simulation
        vy: 0   // Added velocity for force simulation
      };
    });
    
    // Generate edges between nodes based on relationships (category, proximity)
    const newEdges = [];
    
    // Connect nodes of same category
    for (let i = 0; i < newNodes.length; i++) {
      for (let j = i + 1; j < newNodes.length; j++) {
        const sourceNode = newNodes[i];
        const targetNode = newNodes[j];
        
        // Connect nodes of same category with stronger links
        if (sourceNode.category === targetNode.category) {
          const edge = {
            source: sourceNode.id,
            target: targetNode.id,
            strength: 0.8,
            width: 2,
            color: sourceNode.color,
            alpha: 0.6
          };
          newEdges.push(edge);
          sourceNode.adjacentNodes.push(targetNode.id);
          targetNode.adjacentNodes.push(sourceNode.id);
        } 
        // Connect some nodes with weaker links for network effect
        else if (Math.random() > 0.7) {
          const edge = {
            source: sourceNode.id,
            target: targetNode.id,
            strength: 0.3,
            width: 1,
            color: 'rgba(255, 255, 255, 0.3)',
            alpha: 0.3
          };
          newEdges.push(edge);
          sourceNode.adjacentNodes.push(targetNode.id);
          targetNode.adjacentNodes.push(sourceNode.id);
        }
      }
    }
    
    setNodes(newNodes);
    setEdges(newEdges);

    // Debug: Log the graph data
    console.log(`Created graph with ${newNodes.length} nodes and ${newEdges.length} edges`);
  }, [locations]);

  // Center the graph in the canvas when it becomes visible
  useEffect(() => {
    if (isVisible && canvasRef.current && nodes.length > 0) {
      const canvas = canvasRef.current;
      const centerX = canvas.offsetWidth / 2;
      const centerY = canvas.offsetHeight / 2;
      
      // Calculate current center of graph
      let avgX = 0, avgY = 0;
      nodes.forEach(node => {
        avgX += node.x;
        avgY += node.y;
      });
      avgX /= nodes.length;
      avgY /= nodes.length;
      
      // Calculate offset to center
      const offsetX = centerX - avgX;
      const offsetY = centerY - avgY;
      
      // Update node positions
      setNodes(prevNodes => prevNodes.map(node => ({
        ...node,
        x: node.x + offsetX,
        y: node.y + offsetY
      })));
      
      console.log("Centered graph in viewport");
    }
  }, [isVisible, canvasRef.current?.offsetWidth, canvasRef.current?.offsetHeight, nodes.length]);

  // Handle animation and rendering
  useEffect(() => {
    if (!isVisible || !canvasRef.current || !nodes.length) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const pixelRatio = window.devicePixelRatio || 1;
    
    // Set canvas dimensions
    const updateCanvasSize = () => {
      canvas.width = canvas.offsetWidth * pixelRatio;
      canvas.height = canvas.offsetHeight * pixelRatio;
      ctx.scale(pixelRatio, pixelRatio);
    };
    
    updateCanvasSize();
    window.addEventListener('resize', updateCanvasSize);
    
    // Animation state
    let animationActive = true;
    
    // Perform physics simulation with improved force-directed layout
    const updatePositions = () => {
      // Constants for force simulation
      const attraction = 0.005;   // Attraction to connected nodes
      const repulsion = 500;      // Repulsion between all nodes
      const damping = 0.9;        // Damping factor for movement
      const centerGravity = 0.03; // Attraction to center
      
      // Apply forces
      for (let i = 0; i < nodes.length; i++) {
        // Center gravity
        const centerX = canvas.offsetWidth / 2;
        const centerY = canvas.offsetHeight / 2;
        nodes[i].vx += (centerX - nodes[i].x) * centerGravity;
        nodes[i].vy += (centerY - nodes[i].y) * centerGravity;
        
        // Node repulsion (between all nodes)
        for (let j = 0; j < nodes.length; j++) {
          if (i !== j) {
            const dx = nodes[i].x - nodes[j].x;
            const dy = nodes[i].y - nodes[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy) || 1;
            const force = repulsion / (distance * distance);
            nodes[i].vx += dx * force / distance;
            nodes[i].vy += dy * force / distance;
          }
        }
        
        // Edge attraction (between connected nodes)
        for (const edge of edges) {
          if (edge.source === nodes[i].id || edge.target === nodes[i].id) {
            const other = nodes.find(n => 
              n.id === (edge.source === nodes[i].id ? edge.target : edge.source)
            );
            if (other) {
              const dx = nodes[i].x - other.x;
              const dy = nodes[i].y - other.y;
              nodes[i].vx -= dx * attraction * edge.strength;
              nodes[i].vy -= dy * attraction * edge.strength;
            }
          }
        }
        
        // Apply velocity with damping
        nodes[i].vx *= damping;
        nodes[i].vy *= damping;
        nodes[i].x += nodes[i].vx;
        nodes[i].y += nodes[i].vy;
        
        // Keep nodes within bounds with some padding
        const padding = 50;
        nodes[i].x = Math.max(padding, Math.min(canvas.offsetWidth - padding, nodes[i].x));
        nodes[i].y = Math.max(padding, Math.min(canvas.offsetHeight - padding, nodes[i].y));
      }
    };
    
    // Draw the graph
    const drawGraph = () => {
      if (!animationActive) return;
      
      // Clear canvas
      ctx.clearRect(0, 0, canvas.offsetWidth, canvas.offsetHeight);
      
      // Draw background gradient
      const gradient = ctx.createRadialGradient(
        canvas.offsetWidth/2, canvas.offsetHeight/2, 10,
        canvas.offsetWidth/2, canvas.offsetHeight/2, canvas.offsetWidth/2
      );
      gradient.addColorStop(0, 'rgba(25, 25, 35, 0.9)');
      gradient.addColorStop(1, 'rgba(10, 10, 20, 0.95)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.offsetWidth, canvas.offsetHeight);
      
      // Draw edges first (so they appear under nodes)
      edges.forEach(edge => {
        const source = nodes.find(n => n.id === edge.source);
        const target = nodes.find(n => n.id === edge.target);
        if (!source || !target) return;
        
        // Highlight edges connected to hovered node
        let alpha = edge.alpha;
        if (hoveredNode && (hoveredNode.id === source.id || hoveredNode.id === target.id)) {
          alpha = 0.8; // Increase opacity for connected edges
        }
        
        ctx.beginPath();
        ctx.moveTo(source.x, source.y);
        ctx.lineTo(target.x, target.y);
        
        // Use gradient for edges
        const edgeGradient = ctx.createLinearGradient(source.x, source.y, target.x, target.y);
        edgeGradient.addColorStop(0, source.color.replace(')', ', ' + alpha + ')').replace('rgb', 'rgba'));
        edgeGradient.addColorStop(1, target.color.replace(')', ', ' + alpha + ')').replace('rgb', 'rgba'));
        
        ctx.strokeStyle = edgeGradient;
        ctx.lineWidth = edge.width;
        ctx.stroke();
      });
      
      // Draw nodes
      nodes.forEach(node => {
        // Node fill with glow effect
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
        
        // Add glow effect for hovered/active nodes
        if (hoveredNode === node || activeNode === node) {
          ctx.shadowColor = node.color;
          ctx.shadowBlur = 15;
          ctx.fillStyle = node.color;
        } else {
          ctx.shadowBlur = 0;
          // Semi-transparent fill
          ctx.fillStyle = node.color.replace(')', ', 0.7)').replace('rgb', 'rgba');
        }
        ctx.fill();
        
        // Node border
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Draw node label
        ctx.font = '14px Arial';
        ctx.fillStyle = colors.text;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(node.name, node.x, node.y + node.radius + 15);
        
        // Reset shadow for next elements
        ctx.shadowBlur = 0;
      });
      
      // Update positions for next frame
      updatePositions();
      
      // Continue animation loop
      animationRef.current = requestAnimationFrame(drawGraph);
    };
    
    drawGraph();
    
    // Handle mousemove for hover effects
    const handleMouseMove = (e) => {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Check if mouse is over any node
      let foundNode = null;
      for (const node of nodes) {
        const distance = Math.hypot(node.x - x, node.y - y);
        if (distance <= node.radius) {
          foundNode = node;
          break;
        }
      }
      
      setHoveredNode(foundNode);
      document.body.style.cursor = foundNode ? 'pointer' : 'default';
    };
    
    // Handle click to select a node/location
    const handleClick = (e) => {
      if (hoveredNode) {
        setActiveNode(hoveredNode);
        const location = locations.find(loc => loc.id === hoveredNode.id);
        if (location && onNodeClick) {
          onNodeClick(location);
        }
      }
    };
    
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('click', handleClick);
    
    return () => {
      animationActive = false;
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      window.removeEventListener('resize', updateCanvasSize);
      canvas.removeEventListener('mousemove', handleMouseMove);
      canvas.removeEventListener('click', handleClick);
    };
  }, [isVisible, nodes, edges, hoveredNode, activeNode, locations, onNodeClick]);

  return (
    <div className={`graph-container ${isVisible ? 'visible' : 'hidden'}`}>
      <canvas 
        ref={canvasRef} 
        className="graph-canvas"
      />
      
      <div className="graph-legend">
        <div className="legend-title">CuPe-KG Knowledge Graph</div>
        <div className="legend-items">
          <div className="legend-item">
            <span className="legend-color" style={{backgroundColor: colors.historical}}></span>
            <span className="legend-label">Historical Sites</span>
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{backgroundColor: colors.cultural}}></span>
            <span className="legend-label">Cultural Sites</span>
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{backgroundColor: colors.religious}}></span>
            <span className="legend-label">Religious Sites</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GraphVisualization;