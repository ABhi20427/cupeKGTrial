import React, { useState } from 'react';
import Map from './components/Map/Map';
import Header from './components/Header/Header';
import ChatInterface from './components/ChatInterface/ChatInterface';
import { MapProvider } from './context/MapContext';
import './components/ChatInterface/ChatInterface.css';
import './components/ChatInterface/MessageGroup.css';
import './styles/variables.css';
import './styles/animations.css';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [theme, setTheme] = useState('light');
  
  const handleSearch = (query) => {
    setSearchQuery(query);
    // This would typically trigger a search API call
    console.log('Searching for:', query);
  };
  
  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
    // Add theme class to body
    document.body.className = theme === 'light' ? 'dark-theme' : 'light-theme';
  };

  return (
    <MapProvider>
      <div className={`app ${theme}-theme`}>
        <Header 
          onSearch={handleSearch} 
          onThemeToggle={toggleTheme}
          theme={theme}
        />
        <Map searchQuery={searchQuery} />
        <ChatInterface />
      </div>
    </MapProvider>
  );
}

export default App;