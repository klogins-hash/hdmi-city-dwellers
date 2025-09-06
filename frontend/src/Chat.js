import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Load initial stats
    loadStats();
    
    // Add welcome message
    setMessages([{
      id: 1,
      type: 'bot',
      content: `🤖 **Welcome to HDMI City Dwellers Knowledge Base!**

I'm your urban technology assistant, here to help you explore and manage knowledge about smart cities, connectivity, and urban infrastructure.

**🔍 Search:** Ask me anything about urban technology, HDMI, smart cities, or infrastructure
**➕ Add:** \`add: title | content | category\`
**✏️ Update:** \`update: search term | new content\`
**🗑️ Delete:** \`delete: search term\`
**📋 List:** \`list\` or \`list category_name\`
**📊 Stats:** \`stats\` or \`database info\`
**❓ Help:** \`help\`

**Popular Categories:** technology, urban-planning, connectivity, infrastructure, smart-city

Try asking me about "smart city infrastructure" or "HDMI connectivity"!`,
      timestamp: new Date(),
      action_performed: 'welcome'
    }]);
  }, []);

  const loadStats = async () => {
    try {
      const response = await axios.get('/api/database/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await axios.post('/api/chat', {
        message: inputMessage,
        session_id: 'default'
      });

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.response,
        timestamp: new Date(),
        processing_time: response.data.processing_time,
        action_performed: response.data.action_performed,
        data_modified: response.data.data_modified
      };

      setMessages(prev => [...prev, botMessage]);
      
      // Reload stats if data was modified
      if (response.data.data_modified) {
        loadStats();
      }

    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: '❌ Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setInputMessage('');
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getActionIcon = (action) => {
    const icons = {
      'add': '➕',
      'delete': '🗑️',
      'update': '✏️',
      'list': '📋',
      'search': '🔍',
      'stats': '📊',
      'help': '❓',
      'welcome': '🏙️'
    };
    return icons[action] || '💬';
  };

  return (
    <div className="chat-container">
      <div className="chat-sidebar">
        <div className="stats-panel">
          <h3>📊 Database Stats</h3>
          {stats ? (
            <div className="stats-content">
              <div className="stat-item">
                <span className="stat-label">Total Entries:</span>
                <span className="stat-value">{stats.total_entries}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Schema Classes:</span>
                <span className="stat-value">{stats.schema_classes}</span>
              </div>
            </div>
          ) : (
            <div className="stats-loading">Loading...</div>
          )}
        </div>

        <div className="quick-commands">
          <h3>⚡ Quick Commands</h3>
          <button 
            onClick={() => setInputMessage('list all')}
            className="quick-btn"
          >
            📋 List All
          </button>
          <button 
            onClick={() => setInputMessage('list technology')}
            className="quick-btn"
          >
            🔧 Technology
          </button>
          <button 
            onClick={() => setInputMessage('list smart-city')}
            className="quick-btn"
          >
            🏙️ Smart Cities
          </button>
          <button 
            onClick={() => setInputMessage('stats')}
            className="quick-btn"
          >
            📊 Show Stats
          </button>
          <button 
            onClick={() => setInputMessage('help')}
            className="quick-btn"
          >
            ❓ Help
          </button>
        </div>
      </div>

      <div className="chat-main">
        <div className="chat-messages">
          {messages.map((message) => (
            <div 
              key={message.id} 
              className={`message ${message.type}-message ${message.error ? 'error' : ''}`}
            >
              <div className="message-content">
                {message.content.split('\n').map((line, index) => (
                  <div key={index}>
                    {line.includes('**') ? (
                      <span dangerouslySetInnerHTML={{
                        __html: line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                      }} />
                    ) : (
                      line
                    )}
                  </div>
                ))}
              </div>
              <div className="message-meta">
                <span className="message-time">
                  {formatTime(message.timestamp)}
                </span>
                {message.action_performed && (
                  <span className="message-action">
                    {getActionIcon(message.action_performed)} {message.action_performed}
                  </span>
                )}
                {message.processing_time && (
                  <span className="processing-time">
                    ({(message.processing_time * 1000).toFixed(0)}ms)
                  </span>
                )}
                {message.data_modified && (
                  <span className="data-modified">📝 DB Updated</span>
                )}
              </div>
            </div>
          ))}
          
          {loading && (
            <div className="message bot-message">
              <div className="message-content typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={sendMessage} className="chat-input-form">
          <div className="input-group">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask about urban technology or enter a command..."
              disabled={loading}
              className="message-input"
            />
            <button 
              type="submit" 
              disabled={loading || !inputMessage.trim()}
              className="send-button"
            >
              Send
            </button>
          </div>
          <div className="input-hint">
            Try: "add: HDMI 2.1 | Latest HDMI standard for 8K displays | technology" or ask about smart cities
          </div>
        </form>
      </div>
    </div>
  );
};

export default Chat;
