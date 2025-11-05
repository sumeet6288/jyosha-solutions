(function() {
  'use strict';
  
  // Get configuration from script tag
  const script = document.currentScript;
  const config = {
    chatbotId: script?.getAttribute('chatbot-id') || window.botsmithConfig?.chatbotId,
    domain: script?.getAttribute('domain') || window.botsmithConfig?.domain || window.location.origin,
    position: script?.getAttribute('position') || 'bottom-right',
    theme: script?.getAttribute('theme') || 'purple',
    apiUrl: script?.getAttribute('api-url') || (script?.getAttribute('domain') || window.location.origin) + '/api'
  };
  
  if (!config.chatbotId) {
    console.error('BotSmith Widget: chatbot-id is required');
    return;
  }
  
  // Theme colors
  const themes = {
    purple: { primary: '#7c3aed', secondary: '#a78bfa' },
    blue: { primary: '#3b82f6', secondary: '#06b6d4' },
    green: { primary: '#10b981', secondary: '#14b8a6' },
    orange: { primary: '#f97316', secondary: '#f59e0b' },
    pink: { primary: '#ec4899', secondary: '#f43f5e' }
  };
  
  const currentTheme = themes[config.theme] || themes.purple;
  
  // Session ID
  const sessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  
  // State
  let isOpen = false;
  let messages = [];
  let chatbot = null;
  let isLoading = false;
  let isSending = false;
  
  // Position styles
  const positions = {
    'bottom-right': { bottom: '20px', right: '20px' },
    'bottom-left': { bottom: '20px', left: '20px' },
    'top-right': { top: '20px', right: '20px' },
    'top-left': { top: '20px', left: '20px' }
  };
  
  const currentPosition = positions[config.position] || positions['bottom-right'];

  // Inject styles
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideUp {
      from { opacity: 0; transform: translateY(30px) scale(0.95); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }
    @keyframes messageSlideIn {
      from { 
        opacity: 0; 
        transform: translateY(20px) scale(0.95);
      }
      to { 
        opacity: 1; 
        transform: translateY(0) scale(1);
      }
    }
    @keyframes pulse {
      0%, 100% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.1); opacity: 0.8; }
    }
    @keyframes bounce {
      0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(-10px); }
      60% { transform: translateY(-5px); }
    }
    @keyframes dotBounce {
      0%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(-8px); }
    }
    #botsmith-container * { box-sizing: border-box; }
    .botsmith-bubble { animation: bounce 2s infinite; }
    .botsmith-message-item {
      animation: messageSlideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .botsmith-typing-dot {
      width: 8px; height: 8px; border-radius: 50%;
      background: #9ca3af; display: inline-block;
      margin: 0 2px; animation: dotBounce 1.4s infinite ease-in-out;
    }
    .botsmith-typing-dot:nth-child(1) { animation-delay: 0s; }
    .botsmith-typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .botsmith-typing-dot:nth-child(3) { animation-delay: 0.4s; }
    #botsmith-messages {
      scroll-behavior: smooth;
    }
    @media (max-width: 768px) {
      #botsmith-window {
        width: 100vw !important; height: 100vh !important;
        bottom: 0 !important; right: 0 !important; left: 0 !important; top: 0 !important;
        border-radius: 0 !important;
      }
    }
  `;
  document.head.appendChild(style);

  // Create container
  const container = document.createElement('div');
  container.id = 'botsmith-container';
  container.style.cssText = `
    position: fixed;
    ${currentPosition.bottom ? `bottom: ${currentPosition.bottom};` : ''}
    ${currentPosition.top ? `top: ${currentPosition.top};` : ''}
    ${currentPosition.left ? `left: ${currentPosition.left};` : ''}
    ${currentPosition.right ? `right: ${currentPosition.right};` : ''}
    z-index: 999999;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  `;

  // Create chat bubble
  const bubble = document.createElement('button');
  bubble.className = 'botsmith-bubble';
  bubble.innerHTML = `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.38 14.99 3.06 16.27L2 22L7.73 20.94C9.01 21.62 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" fill="white"/>
    </svg>
  `;
  bubble.style.cssText = `
    width: 60px; height: 60px; border-radius: 50%;
    background: linear-gradient(135deg, ${currentTheme.primary} 0%, ${currentTheme.secondary} 100%);
    border: none; cursor: pointer; box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
    display: flex; align-items: center; justify-content: center; transition: all 0.3s ease;
  `;
  
  bubble.onmouseenter = () => {
    bubble.style.transform = 'scale(1.1)';
    bubble.style.boxShadow = `0 8px 20px ${currentTheme.primary}80`;
  };
  bubble.onmouseleave = () => {
    bubble.style.transform = 'scale(1)';
    bubble.style.boxShadow = `0 4px 12px ${currentTheme.primary}66`;
  };

  // Create chat window
  const chatWindow = document.createElement('div');
  chatWindow.id = 'botsmith-window';
  const windowPosition = config.position.includes('bottom') ? 'bottom: 90px;' : 'top: 90px;';
  const windowAlign = config.position.includes('right') ? 'right: 0;' : 'left: 0;';
  
  chatWindow.style.cssText = `
    position: fixed; ${windowPosition} ${windowAlign}
    width: 400px; height: 600px; max-width: calc(100vw - 40px); max-height: calc(100vh - 120px);
    background: white; border-radius: 20px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    display: none; flex-direction: column; overflow: hidden; animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  `;

  // Header
  const header = document.createElement('div');
  header.style.cssText = `
    background: linear-gradient(135deg, ${currentTheme.primary} 0%, ${currentTheme.secondary} 100%);
    color: white; padding: 20px; display: flex; align-items: center; justify-content: space-between;
  `;
  header.innerHTML = `
    <div style="display: flex; align-items: center; gap: 12px; flex: 1;">
      <div style="width: 44px; height: 44px; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.38 14.99 3.06 16.27L2 22L7.73 20.94C9.01 21.62 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" fill="${currentTheme.primary}"/>
        </svg>
      </div>
      <div style="flex: 1;">
        <div style="font-weight: 600; font-size: 16px;" id="botsmith-header-title">Chat Support</div>
        <div style="font-size: 12px; opacity: 0.95;">Usually replies instantly</div>
      </div>
    </div>
    <button id="botsmith-close" style="background: rgba(255,255,255,0.15); border: none; color: white; cursor: pointer; padding: 8px; display: flex; border-radius: 8px; transition: all 0.2s;">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
        <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </button>
  `;

  // Messages container
  const messagesContainer = document.createElement('div');
  messagesContainer.id = 'botsmith-messages';
  messagesContainer.style.cssText = `
    flex: 1; overflow-y: auto; padding: 20px; background: #f9fafb;
    display: flex; flex-direction: column; gap: 12px;
  `;

  // Input area
  const inputArea = document.createElement('div');
  inputArea.style.cssText = 'border-top: 1px solid #e5e7eb; padding: 12px 16px; background: white;';
  inputArea.innerHTML = `
    <form id="botsmith-form" style="display: flex; gap: 8px; margin: 0;">
      <input type="text" id="botsmith-input" placeholder="Type your message..."
        style="flex: 1; padding: 10px 16px; border: 1px solid #e5e7eb; border-radius: 24px; outline: none; font-size: 14px;"
      />
      <button type="submit" id="botsmith-send" style="width: 40px; height: 40px; border-radius: 50%; border: none; background: ${currentTheme.primary}; color: white; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
          <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </form>
  `;

  // Branding footer
  const brandingFooter = document.createElement('div');
  brandingFooter.style.cssText = 'padding: 8px 16px; background: #f9fafb; text-align: center; border-top: 1px solid #f3f4f6;';
  brandingFooter.innerHTML = `
    <a href="https://botsmith.ai" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: #9ca3af; font-size: 10px; display: flex; align-items: center; justify-content: center; gap: 4px; transition: color 0.2s;">
      <span>Powered by</span>
      <span style="font-weight: 600; color: ${currentTheme.primary};">BotSmith</span>
    </a>
  `;
  
  // Add hover effect
  const brandingLink = brandingFooter.querySelector('a');
  brandingLink.addEventListener('mouseenter', () => {
    brandingLink.style.color = currentTheme.primary;
  });
  brandingLink.addEventListener('mouseleave', () => {
    brandingLink.style.color = '#9ca3af';
  });

  // Assemble window
  chatWindow.appendChild(header);
  chatWindow.appendChild(messagesContainer);
  chatWindow.appendChild(inputArea);
  chatWindow.appendChild(brandingFooter);

  // Assemble container
  container.appendChild(bubble);
  container.appendChild(chatWindow);

  // Add to DOM
  document.body.appendChild(container);

  // Functions
  function addMessage(role, content) {
    messages.push({ role, content, timestamp: new Date() });
    renderMessages();
  }

  function renderMessages() {
    messagesContainer.innerHTML = '';
    messages.forEach((msg, index) => {
      const msgDiv = document.createElement('div');
      msgDiv.className = 'botsmith-message-item';
      msgDiv.style.cssText = `
        display: flex; gap: 8px; align-items: flex-start;
        ${msg.role === 'user' ? 'justify-content: flex-end;' : ''}
        animation-delay: ${index === messages.length - 1 ? '0s' : '0s'};
      `;
      
      if (msg.role === 'assistant') {
        const avatarContent = chatbot?.avatar_url 
          ? `<img src="${chatbot.avatar_url}" alt="Bot" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;">`
          : `<svg width="18" height="18" viewBox="0 0 24 24" fill="white">
              <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.38 14.99 3.06 16.27L2 22L7.73 20.94C9.01 21.62 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z"/>
            </svg>`;
            
        msgDiv.innerHTML = `
          <div style="width: 32px; height: 32px; border-radius: 50%; background: ${currentTheme.secondary}; display: flex; align-items: center; justify-content: center; flex-shrink: 0; overflow: hidden;">
            ${avatarContent}
          </div>
          <div style="max-width: 70%; padding: 12px 16px; border-radius: 18px; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); word-wrap: break-word; font-size: 13px; line-height: 1.5;">
            ${msg.content}
          </div>
        `;
      } else {
        msgDiv.innerHTML = `
          <div style="max-width: 70%; padding: 12px 16px; border-radius: 18px; background: ${currentTheme.primary}; color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); word-wrap: break-word; font-size: 13px; line-height: 1.5;">
            ${msg.content}
          </div>
        `;
      }
      
      messagesContainer.appendChild(msgDiv);
    });
    
    // Smooth scroll to bottom to show newest message
    requestAnimationFrame(() => {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });
  }

  function showTyping() {
    const typingDiv = document.createElement('div');
    typingDiv.id = 'botsmith-typing-indicator';
    typingDiv.className = 'botsmith-message-item';
    typingDiv.style.cssText = 'display: flex; gap: 8px; align-items: center;';
    
    const avatarContent = chatbot?.avatar_url 
      ? `<img src="${chatbot.avatar_url}" alt="Bot" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;">`
      : `<svg width="18" height="18" viewBox="0 0 24 24" fill="white">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.38 14.99 3.06 16.27L2 22L7.73 20.94C9.01 21.62 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z"/>
        </svg>`;
    
    typingDiv.innerHTML = `
      <div style="width: 32px; height: 32px; border-radius: 50%; background: ${currentTheme.secondary}; display: flex; align-items: center; justify-content: center; overflow: hidden;">
        ${avatarContent}
      </div>
      <div style="padding: 12px 16px; border-radius: 18px; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <span class="botsmith-typing-dot"></span>
        <span class="botsmith-typing-dot"></span>
        <span class="botsmith-typing-dot"></span>
      </div>
    `;
    messagesContainer.appendChild(typingDiv);
    
    // Smooth scroll to bottom to show typing indicator
    requestAnimationFrame(() => {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });
  }

  function hideTyping() {
    const typing = document.getElementById('botsmith-typing-indicator');
    if (typing) typing.remove();
  }

  async function loadChatbot() {
    try {
      isLoading = true;
      const response = await fetch(`${config.apiUrl}/public/chatbot/${config.chatbotId}`);
      if (!response.ok) throw new Error('Failed to load chatbot');
      
      chatbot = await response.json();
      
      // Update header title
      document.getElementById('botsmith-header-title').textContent = chatbot.name || 'Chat Support';
      
      // Apply custom colors if available
      if (chatbot.primary_color) {
        currentTheme.primary = chatbot.primary_color;
        currentTheme.secondary = chatbot.secondary_color || chatbot.primary_color;
        
        // Update bubble colors
        bubble.style.background = `linear-gradient(135deg, ${currentTheme.primary} 0%, ${currentTheme.secondary} 100%)`;
        
        // Update header colors
        header.style.background = `linear-gradient(135deg, ${currentTheme.primary} 0%, ${currentTheme.secondary} 100%)`;
        
        // Update send button color
        const sendBtn = document.getElementById('botsmith-send');
        if (sendBtn) sendBtn.style.background = currentTheme.primary;
        
        // Update all bot avatar colors
        updateBotAvatarColors();
        
        // Update branding color
        const brandingBotSmith = brandingFooter.querySelector('span[style*="font-weight: 600"]');
        if (brandingBotSmith) {
          brandingBotSmith.style.color = currentTheme.primary;
        }
      }
      
      // Update logo if available
      if (chatbot.logo_url) {
        // Find the logo container more specifically - it's the first div inside the flex container
        const flexContainer = header.querySelector('div[style*="display: flex"]');
        const logoContainer = flexContainer?.querySelector('div');
        if (logoContainer) {
          // Update logo while maintaining container styles to prevent layout issues
          logoContainer.style.cssText = 'width: 44px; height: 44px; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center; flex-shrink: 0; overflow: hidden;';
          logoContainer.innerHTML = `<img src="${chatbot.logo_url}" alt="Logo" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;">`;
        }
      }
      
      // Apply widget settings from chatbot configuration
      if (chatbot.widget_position) {
        const newPosition = positions[chatbot.widget_position] || positions['bottom-right'];
        // Reset all positions first, then set the appropriate ones
        container.style.bottom = '';
        container.style.top = '';
        container.style.left = '';
        container.style.right = '';
        
        // Update container position
        if (newPosition.bottom) container.style.bottom = newPosition.bottom;
        if (newPosition.top) container.style.top = newPosition.top;
        if (newPosition.left) container.style.left = newPosition.left;
        if (newPosition.right) container.style.right = newPosition.right;
        
        // Update chat window position
        const windowPosition = chatbot.widget_position.includes('bottom') ? 'bottom: 90px;' : 'top: 90px;';
        const windowAlign = chatbot.widget_position.includes('right') ? 'right: 0;' : 'left: 0;';
        
        // Rebuild window style with new position
        chatWindow.style.cssText = `
          position: fixed; ${windowPosition} ${windowAlign}
          width: ${chatWindow.style.width || '420px'}; height: ${chatWindow.style.height || '600px'}; 
          max-width: calc(100vw - 40px); max-height: calc(100vh - 120px);
          background: white; border-radius: 20px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
          display: ${chatWindow.style.display || 'none'}; flex-direction: column; overflow: hidden; 
          animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        `;
      }
      
      // Apply widget size
      if (chatbot.widget_size) {
        const sizes = {
          'small': { width: '360px', height: '550px' },
          'medium': { width: '420px', height: '600px' },
          'large': { width: '500px', height: '700px' }
        };
        const size = sizes[chatbot.widget_size] || sizes['medium'];
        chatWindow.style.width = size.width;
        chatWindow.style.height = size.height;
      }
      
      // Apply widget theme (background color of messages area)
      if (chatbot.widget_theme) {
        const themeColors = {
          'light': '#f9fafb',
          'dark': '#1f2937',
          'auto': window.matchMedia('(prefers-color-scheme: dark)').matches ? '#1f2937' : '#f9fafb'
        };
        messagesContainer.style.background = themeColors[chatbot.widget_theme] || themeColors['light'];
      }
      
      // Auto-expand widget if enabled
      if (chatbot.auto_expand && !isOpen) {
        setTimeout(() => {
          toggleChat();
        }, 1000); // Open after 1 second
      }
      
      // Add welcome message
      if (chatbot.welcome_message) {
        addMessage('assistant', chatbot.welcome_message);
      }
    } catch (error) {
      console.error('Error loading chatbot:', error);
      addMessage('assistant', 'Hello! How can I help you today?');
    } finally {
      isLoading = false;
    }
  }
  
  function updateBotAvatarColors() {
    // Update all existing bot avatars
    const avatars = messagesContainer.querySelectorAll('div[style*="background"]');
    avatars.forEach(avatar => {
      if (avatar.querySelector('svg')) {
        avatar.style.background = currentTheme.secondary;
      }
    });
  }

  async function sendMessage(message) {
    if (!message.trim() || isSending) return;
    
    isSending = true;
    const input = document.getElementById('botsmith-input');
    input.disabled = true;
    
    // Add user message
    addMessage('user', message);
    input.value = '';
    
    // Show typing
    showTyping();
    
    try {
      const response = await fetch(`${config.apiUrl}/public/chat/${config.chatbotId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, session_id: sessionId })
      });
      
      if (!response.ok) throw new Error('Failed to send message');
      
      const data = await response.json();
      hideTyping();
      addMessage('assistant', data.message);
    } catch (error) {
      console.error('Error sending message:', error);
      hideTyping();
      addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
    } finally {
      isSending = false;
      input.disabled = false;
      input.focus();
    }
  }

  function toggleChat() {
    isOpen = !isOpen;
    if (isOpen) {
      chatWindow.style.display = 'flex';
      bubble.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18M6 6L18 18" stroke="white" stroke-width="2.5" stroke-linecap="round"/></svg>`;
      bubble.className = '';
      document.getElementById('botsmith-input').focus();
      
      if (!chatbot) loadChatbot();
    } else {
      chatWindow.style.display = 'none';
      bubble.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.38 14.99 3.06 16.27L2 22L7.73 20.94C9.01 21.62 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" fill="white"/></svg>`;
      bubble.className = 'botsmith-bubble';
    }
  }

  // Event listeners
  bubble.onclick = toggleChat;
  document.getElementById('botsmith-close').onclick = (e) => {
    e.stopPropagation();
    toggleChat();
  };
  
  document.getElementById('botsmith-form').onsubmit = (e) => {
    e.preventDefault();
    const input = document.getElementById('botsmith-input');
    sendMessage(input.value);
  };

  // API
  window.BotSmith = {
    open: () => { if (!isOpen) toggleChat(); },
    close: () => { if (isOpen) toggleChat(); },
    toggle: toggleChat,
    isOpen: () => isOpen
  };
  
  // Load chatbot configuration immediately to apply widget settings
  loadChatbot();
})();
