import React from 'react';
import Chat from './Chat';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>🏙️ HDMI City Dwellers</h1>
        <p>Urban Technology Knowledge Base - Connecting Cities Through Smart Infrastructure</p>
      </header>
      <main className="app-main">
        <Chat />
      </main>
    </div>
  );
}

export default App;
