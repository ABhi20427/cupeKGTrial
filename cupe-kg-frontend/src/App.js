import React, { useState } from 'react';
import Map from './components/Map/Map';
import Header from './components/Header/Header';
import InfoPanel from './components/InfoPanel/InfoPanel';
import ChatInterface from './components/ChatInterface/ChatInterface';
import Timeline from './components/Timeline/Timeline';
import GraphVisualization from './components/GraphVisualization/GraphVisualization';
import { MapProvider } from './context/MapContext';
import './components/ChatInterface/ChatInterface.css';
import './components/ChatInterface/MessageGroup.css';
import './styles/variables.css';
import './styles/animations.css';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [theme, setTheme] = useState('light');
  const [isPanelOpen, setIsPanelOpen] = useState(false);
  const [showTimeline, setShowTimeline] = useState(true);
  const [showGraph, setShowGraph] = useState(false);

  const handleSearch = (query) => {
    setSearchQuery(query);
    console.log('Searching for:', query);
  };

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
    document.body.className = theme === 'light' ? 'dark-theme' : 'light-theme';
  };

  const handleTimelineLocationSelect = (location) => {
    console.log('Timeline location selected:', location);
  };

  const handleGraphNodeClick = (location) => {
    console.log('Graph node clicked:', location);
  };

  const toggleGraphVisualization = () => {
    setShowGraph(!showGraph);
  };

  return (
    <MapProvider>
      <div className={`app ${theme}-theme`}>
        <Header 
          onSearch={handleSearch} 
          onThemeToggle={toggleTheme}
          theme={theme}
          onToggleGraph={toggleGraphVisualization}
          showGraph={showGraph}
        />
        
        <Map searchQuery={searchQuery} />
        
        <InfoPanel 
          onOpen={() => setIsPanelOpen(true)}
          onClose={() => setIsPanelOpen(false)}
        />
        
        <ChatInterface isPanelOpen={isPanelOpen} />
        
        <Timeline 
          isVisible={showTimeline}
          onLocationSelect={handleTimelineLocationSelect}
        />
        
        <GraphVisualization
          isVisible={showGraph}
          onNodeClick={handleGraphNodeClick}
          onClose={() => setShowGraph(false)}
        />
      </div>
    </MapProvider>
  );
}

export default App;