(function() {
  'use strict';
  
  // Get configuration from script tag or window object
  const script = document.currentScript;
  const config = {
    chatbotId: script?.getAttribute('chatbot-id') || window.botsmithConfig?.chatbotId,
    domain: script?.getAttribute('domain') || window.botsmithConfig?.domain || window.location.origin,
    position: script?.getAttribute('position') || window.botsmithConfig?.position || 'bottom-right',
    theme: script?.getAttribute('theme') || window.botsmithConfig?.theme || 'purple',
    welcomeMessage: script?.getAttribute('welcome-message') || window.botsmithConfig?.welcomeMessage,
    showNotification: script?.getAttribute('show-notification') !== 'false',
    autoOpen: script?.getAttribute('auto-open') === 'true',
    autoOpenDelay: parseInt(script?.getAttribute('auto-open-delay') || '3000')
  };
  
  if (!config.chatbotId) {
    console.error('BotSmith Widget: chatbot-id is required');
    return;
  }
  
  // Theme colors
  const themes = {
    purple: { primary: '#7c3aed', secondary: '#db2777', gradient: 'linear-gradient(135deg, #7c3aed 0%, #db2777 100%)' },
    blue: { primary: '#3b82f6', secondary: '#06b6d4', gradient: 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)' },
    green: { primary: '#10b981', secondary: '#14b8a6', gradient: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)' },
    orange: { primary: '#f97316', secondary: '#f59e0b', gradient: 'linear-gradient(135deg, #f97316 0%, #f59e0b 100%)' },
    pink: { primary: '#ec4899', secondary: '#f43f5e', gradient: 'linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)' }
  };
  
  const currentTheme = themes[config.theme] || themes.purple;
  
  // Position styles
  const positions = {
    'bottom-right': { bottom: '20px', right: '20px', left: 'auto', top: 'auto' },
    'bottom-left': { bottom: '20px', left: '20px', right: 'auto', top: 'auto' },
    'top-right': { top: '20px', right: '20px', left: 'auto', bottom: 'auto' },
    'top-left': { top: '20px', left: '20px', right: 'auto', bottom: 'auto' }
  };
  
  const currentPosition = positions[config.position] || positions['bottom-right'];

  // Create chat widget container
  const widgetContainer = document.createElement('div');
  widgetContainer.id = 'botsmith-widget-container';
  widgetContainer.style.cssText = `
    position: fixed;
    ${currentPosition.bottom ? `bottom: ${currentPosition.bottom};` : ''}
    ${currentPosition.top ? `top: ${currentPosition.top};` : ''}
    ${currentPosition.left ? `left: ${currentPosition.left};` : ''}
    ${currentPosition.right ? `right: ${currentPosition.right};` : ''}
    z-index: 999999;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  `;

  // Create notification badge
  const notificationBadge = document.createElement('div');
  notificationBadge.id = 'botsmith-notification';
  notificationBadge.style.cssText = `
    position: absolute;
    top: -8px;
    right: -8px;
    width: 24px;
    height: 24px;
    background: #ef4444;
    border-radius: 50%;
    color: white;
    font-size: 12px;
    font-weight: bold;
    display: none;
    align-items: center;
    justify-content: center;
    animation: pulse 2s infinite;
    border: 2px solid white;
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
  `;
  notificationBadge.textContent = '1';

  // Create chat bubble button with ripple effect
  const chatBubble = document.createElement('button');
  chatBubble.id = 'botsmith-bubble';
  chatBubble.setAttribute('aria-label', 'Open chat');
  chatBubble.innerHTML = `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.38 14.99 3.06 16.27L2 22L7.73 20.94C9.01 21.62 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C10.69 20 9.45 19.69 8.35 19.14L8 18.96L4.21 19.79L5.04 16.05L4.84 15.68C4.26 14.55 3.94 13.31 3.94 12C3.94 7.59 7.59 3.94 12 3.94C16.41 3.94 20.06 7.59 20.06 12C20.06 16.41 16.41 20 12 20Z" fill="white"/>
    </svg>
  `;
  chatBubble.style.cssText = `
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: ${currentTheme.gradient};
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  `;
  
  // Add ripple effect container
  const rippleContainer = document.createElement('div');
  rippleContainer.style.cssText = `
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 50%;
    overflow: hidden;
    pointer-events: none;
  `;
  chatBubble.appendChild(rippleContainer);

  // Ripple effect on click
  chatBubble.addEventListener('click', function(e) {
    const ripple = document.createElement('span');
    ripple.style.cssText = `
      position: absolute;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.6);
      width: 100px;
      height: 100px;
      margin-top: -50px;
      margin-left: -50px;
      animation: ripple 0.6s;
      top: ${e.offsetY}px;
      left: ${e.offsetX}px;
    `;
    rippleContainer.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });

  // Enhanced hover effect
  chatBubble.addEventListener('mouseenter', () => {
    chatBubble.style.transform = 'scale(1.1) rotate(5deg)';
    chatBubble.style.boxShadow = `0 8px 20px ${currentTheme.primary}80`;
  });
  chatBubble.addEventListener('mouseleave', () => {
    chatBubble.style.transform = 'scale(1) rotate(0deg)';
    chatBubble.style.boxShadow = `0 4px 12px ${currentTheme.primary}66`;
  });

  // Create chat window with enhanced styling
  const chatWindow = document.createElement('div');
  chatWindow.id = 'botsmith-window';
  const windowPosition = config.position.includes('bottom') ? 'bottom: 90px;' : 'top: 90px;';
  const windowAlign = config.position.includes('right') ? 'right: 20px;' : 'left: 20px;';
  
  chatWindow.style.cssText = `
    position: fixed;
    ${windowPosition}
    ${windowAlign}
    width: 400px;
    height: 600px;
    max-width: calc(100vw - 40px);
    max-height: calc(100vh - 120px);
    background: white;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    display: none;
    flex-direction: column;
    overflow: hidden;
    z-index: 999998;
    animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    border: 1px solid rgba(0, 0, 0, 0.08);
  `;

  // Enhanced animation keyframes
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideUp {
      from {
        opacity: 0;
        transform: translateY(30px) scale(0.95);
      }
      to {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }
    
    @keyframes pulse {
      0%, 100% {
        transform: scale(1);
        opacity: 1;
      }
      50% {
        transform: scale(1.1);
        opacity: 0.8;
      }
    }
    
    @keyframes ripple {
      to {
        transform: scale(4);
        opacity: 0;
      }
    }
    
    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(10px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    
    @keyframes bounce {
      0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
      }
      40% {
        transform: translateY(-10px);
      }
      60% {
        transform: translateY(-5px);
      }
    }
    
    #botsmith-bubble {
      animation: bounce 2s infinite;
    }
    
    @media (max-width: 768px) {
      #botsmith-window {
        width: calc(100vw - 20px) !important;
        height: calc(100vh - 100px) !important;
        bottom: 10px !important;
        top: auto !important;
        left: 10px !important;
        right: 10px !important;
        border-radius: 16px !important;
      }
      #botsmith-widget-container {
        bottom: 10px !important;
        right: 10px !important;
      }
    }
    
    /* Smooth scrollbar */
    #botsmith-window ::-webkit-scrollbar {
      width: 6px;
    }
    #botsmith-window ::-webkit-scrollbar-track {
      background: #f1f1f1;
    }
    #botsmith-window ::-webkit-scrollbar-thumb {
      background: ${currentTheme.primary};
      border-radius: 3px;
    }
    #botsmith-window ::-webkit-scrollbar-thumb:hover {
      background: ${currentTheme.secondary};
    }
  `;
  document.head.appendChild(style);

  // Create enhanced header with typing indicator
  const header = document.createElement('div');
  header.style.cssText = `
    background: ${currentTheme.gradient};
    color: white;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  `;
  
  const typingIndicator = `
    <div id="botsmith-typing" style="display: none; margin-top: 4px; font-size: 11px; opacity: 0.9;">
      <span style="animation: fadeIn 0.5s;">AI is typing</span>
      <span style="animation: pulse 1.4s infinite;">...</span>
    </div>
  `;
  
  header.innerHTML = `
    <div style="display: flex; align-items: center; gap: 12px; flex: 1;">
      <div style="width: 44px; height: 44px; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.38 14.99 3.06 16.27L2 22L7.73 20.94C9.01 21.62 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C10.69 20 9.45 19.69 8.35 19.14L8 18.96L4.21 19.79L5.04 16.05L4.84 15.68C4.26 14.55 3.94 13.31 3.94 12C3.94 7.59 7.59 3.94 12 3.94C16.41 3.94 20.06 7.59 20.06 12C20.06 16.41 16.41 20 12 20Z" fill="${currentTheme.primary}"/>
        </svg>
      </div>
      <div style="flex: 1;">
        <div style="font-weight: 600; font-size: 16px; display: flex; align-items: center; gap: 6px;">
          Chat Support
          <span style="width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block; animation: pulse 2s infinite;"></span>
        </div>
        <div style="font-size: 12px; opacity: 0.95;">Usually replies instantly</div>
        ${typingIndicator}
      </div>
    </div>
    <div style="display: flex; gap: 8px;">
      <button id="botsmith-minimize" style="background: rgba(255,255,255,0.15); border: none; color: white; cursor: pointer; padding: 8px; display: flex; align-items: center; justify-content: center; border-radius: 8px; transition: all 0.2s; backdrop-filter: blur(10px);" onmouseover="this.style.background='rgba(255,255,255,0.25)'" onmouseout="this.style.background='rgba(255,255,255,0.15)'">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
      <button id="botsmith-close" style="background: rgba(255,255,255,0.15); border: none; color: white; cursor: pointer; padding: 8px; display: flex; align-items: center; justify-content: center; border-radius: 8px; transition: all 0.2s; backdrop-filter: blur(10px);" onmouseover="this.style.background='rgba(255,255,255,0.25)'; this.style.transform='rotate(90deg)'" onmouseout="this.style.background='rgba(255,255,255,0.15)'; this.style.transform='rotate(0deg)'">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
  `;

  // Create iframe with loading state
  const iframeContainer = document.createElement('div');
  iframeContainer.style.cssText = `
    width: 100%;
    height: 100%;
    flex: 1;
    position: relative;
    background: #f9fafb;
  `;
  
  const loadingIndicator = document.createElement('div');
  loadingIndicator.id = 'botsmith-loading';
  loadingIndicator.style.cssText = `
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: ${currentTheme.primary};
  `;
  loadingIndicator.innerHTML = `
    <div style="width: 40px; height: 40px; border: 3px solid #e5e7eb; border-top: 3px solid ${currentTheme.primary}; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 12px;"></div>
    <div style="font-size: 14px; color: #6b7280;">Loading chat...</div>
  `;
  
  const spinAnimation = document.createElement('style');
  spinAnimation.textContent = `
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  `;
  document.head.appendChild(spinAnimation);
  
  const iframe = document.createElement('iframe');
  iframe.src = `${config.domain}/public-chat/${config.chatbotId}`;
  iframe.style.cssText = `
    width: 100%;
    height: 100%;
    border: none;
    display: none;
  `;
  iframe.setAttribute('allow', 'clipboard-read; clipboard-write');
  iframe.setAttribute('loading', 'lazy');
  
  iframe.onload = () => {
    loadingIndicator.style.display = 'none';
    iframe.style.display = 'block';
  };
  
  iframeContainer.appendChild(loadingIndicator);
  iframeContainer.appendChild(iframe);

  // Assemble chat window
  chatWindow.appendChild(header);
  chatWindow.appendChild(iframeContainer);

  // Add notification badge to bubble
  chatBubble.appendChild(notificationBadge);
  
  // Assemble widget
  widgetContainer.appendChild(chatBubble);
  widgetContainer.appendChild(chatWindow);

  // Toggle chat window with enhanced animations
  let isOpen = false;
  let hasBeenOpened = false;
  
  function toggleChat() {
    isOpen = !isOpen;
    if (isOpen) {
      chatWindow.style.display = 'flex';
      chatBubble.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M18 6L6 18M6 6L18 18" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      `;
      chatBubble.style.animation = 'none';
      notificationBadge.style.display = 'none';
      hasBeenOpened = true;
      
      // Load iframe content if not loaded yet
      if (!iframe.src) {
        iframe.src = `${config.domain}/public-chat/${config.chatbotId}`;
      }
    } else {
      chatWindow.style.display = 'none';
      chatBubble.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.38 14.99 3.06 16.27L2 22L7.73 20.94C9.01 21.62 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C10.69 20 9.45 19.69 8.35 19.14L8 18.96L4.21 19.79L5.04 16.05L4.84 15.68C4.26 14.55 3.94 13.31 3.94 12C3.94 7.59 7.59 3.94 12 3.94C16.41 3.94 20.06 7.59 20.06 12C20.06 16.41 16.41 20 12 20Z" fill="white"/>
        </svg>
      `;
      if (!hasBeenOpened) {
        chatBubble.style.animation = 'bounce 2s infinite';
      }
    }
  }
  
  // Show welcome notification
  function showNotification() {
    if (config.showNotification && !hasBeenOpened) {
      setTimeout(() => {
        notificationBadge.style.display = 'flex';
      }, 2000);
    }
  }

  chatBubble.addEventListener('click', toggleChat);
  
  header.querySelector('#botsmith-close').addEventListener('click', (e) => {
    e.stopPropagation();
    toggleChat();
  });
  
  header.querySelector('#botsmith-minimize').addEventListener('click', (e) => {
    e.stopPropagation();
    toggleChat();
  });

  // Add to DOM when ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      document.body.appendChild(widgetContainer);
    });
  } else {
    document.body.appendChild(widgetContainer);
  }

  // Expose API for programmatic control
  window.BotSmith = {
    open: () => {
      if (!isOpen) toggleChat();
    },
    close: () => {
      if (isOpen) toggleChat();
    },
    toggle: toggleChat
  };
})();
