import React, { useState, useRef, useEffect } from 'react';
import './ChatbotPage.css';

const ChatbotPage = () => {
  const [messages, setMessages] = useState([
    { 
      id: 1, 
      text: "👋 Hello! I'm your AI assistant. I'm here to help you with any questions or tasks you might have.", 
      sender: 'bot', 
      timestamp: "10:30 AM" 
    },
    { 
      id: 2, 
      text: "Feel free to ask me anything - from general information to specific assistance. How can I help you today?", 
      sender: 'bot', 
      timestamp: "10:30 AM" 
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Auto-resize textarea
  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
    }
  };

  useEffect(() => {
    adjustTextareaHeight();
  }, [inputMessage]);

  const generateBotResponses = () => {
    const responses = [
      "That's a great question! Let me help you with that. 🤔",
      "I understand what you're asking. Here's what I can tell you about that topic.",
      "Thanks for reaching out! I'd be happy to assist you with this.",
      "That's an interesting point. Let me provide you with some helpful information.",
      "I'm here to help! Based on your question, I can offer some guidance.",
      "Great question! I can definitely help you understand this better.",
      "I appreciate you asking! Here's my take on what you're looking for."
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const handleSendMessage = async () => {
    if (inputMessage.trim() === '') return;

    const newUserMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prevMessages => [...prevMessages, newUserMessage]);
    setInputMessage('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      const response = await fetch('http://localhost:5000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: newUserMessage.text })
      });
      const data = await response.json();
      setIsTyping(false);
      setMessages(prevMessages => [
        ...prevMessages,
        {
          id: Date.now() + 1,
          text: data.text,
          sql: data.sql || null,
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } catch (error) {
      setIsTyping(false);
      setMessages(prevMessages => [
        ...prevMessages,
        {
          id: Date.now() + 1,
          text: 'Sorry, there was an error connecting to the server.',
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    }
    setIsLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleInputChange = (e) => {
    setInputMessage(e.target.value);
    adjustTextareaHeight();
  };

  // Format timestamp to show only when needed
  const shouldShowTimestamp = (index) => {
    if (index === 0) return true;
    
    const prevMessage = messages[index - 1];
    const currentMessage = messages[index];
    
    return prevMessage.sender !== currentMessage.sender;
  };

  const quickActions = [
    { icon: "💡", text: "Get suggestions" },
    { icon: "📊", text: "Show analytics" },
    { icon: "❓", text: "Help & Support" },
    { icon: "⚙️", text: "Settings" }
  ];

  const handleQuickAction = (action) => {
    setInputMessage(action.text);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="modern-chatbot-container">
      <div className="chatbot-header">
        <div className="chatbot-header-info">
          <div className="chatbot-avatar">
            <div className="avatar-inner">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z"/>
                <path d="M12 22V12"/>
                <path d="M22 7L12 12L2 7"/>
              </svg>
            </div>
          </div>
          <div className="chatbot-header-text">
            <h2>AI Assistant</h2>
            <p className="chatbot-status">
              <span className="status-indicator"></span>
              Online • Ready to help
            </p>
          </div>
        </div>
        <div className="chatbot-actions">
          <button className="action-button" title="Search">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
          </button>
          <button className="action-button" title="More options">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="1"/>
              <circle cx="19" cy="12" r="1"/>
              <circle cx="5" cy="12" r="1"/>
            </svg>
          </button>
        </div>
      </div>
      
      <div className="chat-messages">
        {messages.length === 2 && (
          <div className="welcome-section">
            <div className="welcome-message">
              <h3>Welcome to AI Assistant! 🚀</h3>
              <p>Try these quick actions to get started:</p>
              <div className="quick-actions">
                {quickActions.map((action, index) => (
                  <button 
                    key={index}
                    className="quick-action-btn"
                    onClick={() => handleQuickAction(action)}
                  >
                    <span className="action-icon">{action.icon}</span>
                    <span className="action-text">{action.text}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div key={message.id} className={`message-wrapper ${message.sender === 'user' ? 'user-message-wrapper' : 'bot-message-wrapper'}`}>
            {message.sender === 'bot' && (
              <div className="message-avatar">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z"/>
                  <path d="M12 22V12"/>
                  <path d="M22 7L12 12L2 7"/>
                </svg>
              </div>
            )}
            <div className="message-container">
              {shouldShowTimestamp(index) && (
                <div className="message-timestamp">{message.timestamp}</div>
              )}
              <div className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}>
                <div className="message-bubble">
                  <div className="message-text">{message.text}</div>
                  {message.sender === 'bot' && message.sql && (
                    <div className="sql-container">
                      <div className="sql-header">
                        <div className="sql-title">
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <polyline points="16 18 22 12 16 6"/>
                            <polyline points="8 6 2 12 8 18"/>
                          </svg>
                          SQL Query
                        </div>
                        <button 
                          className="copy-btn"
                          onClick={() => copyToClipboard(message.sql)}
                          title="Copy SQL"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                          </svg>
                        </button>
                      </div>
                      <pre className="sql-block">{message.sql}</pre>
                    </div>
                  )}
                </div>
                <div className="message-info">
                  <span className="message-time">{message.timestamp}</span>
                  {message.sender === 'user' && (
                    <span className="message-status">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="20 6 9 17 4 12"/>
                      </svg>
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="message-wrapper bot-message-wrapper">
            <div className="message-avatar">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z"/>
                <path d="M12 22V12"/>
                <path d="M22 7L12 12L2 7"/>
              </svg>
            </div>
            <div className="message-container">
              <div className="message bot-message">
                <div className="message-bubble typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="chat-input-area">
        <button className="input-action-button" title="Add emoji">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
            <line x1="9" y1="9" x2="9.01" y2="9"/>
            <line x1="15" y1="9" x2="15.01" y2="9"/>
          </svg>
        </button>
        <button className="input-action-button" title="Attach file">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21.44 11.05L12.25 20.24C11.12 21.37 9.31 21.37 8.18 20.24C7.05 19.11 7.05 17.3 8.18 16.17L15.84 8.51C16.48 7.87 17.52 7.87 18.16 8.51C18.8 9.15 18.8 10.19 18.16 10.83L11.19 17.8"/>
          </svg>
        </button>
        <div className="message-input-container">
          <textarea
            ref={textareaRef}
            placeholder="Type your message here..."
            value={inputMessage}
            onChange={handleInputChange}
            onKeyDown={handleKeyPress}
            disabled={isLoading}
            rows="1"
          />
          {inputMessage && (
            <button 
              className="clear-input-btn"
              onClick={() => setInputMessage('')}
              title="Clear input"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          )}
        </div>
        <button 
          className={`send-button ${inputMessage.trim() ? 'active' : ''}`}
          onClick={handleSendMessage} 
          disabled={isLoading || inputMessage.trim() === ''}
          title="Send message"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"/>
            <polygon points="22 2 15 22 11 13 2 9 22 2"/>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default ChatbotPage;