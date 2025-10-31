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

  // Create chat window
  const chatWindow = document.createElement('div');
  chatWindow.id = 'botsmith-window';
  chatWindow.style.cssText = `
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 400px;
    height: 600px;
    max-width: calc(100vw - 40px);
    max-height: calc(100vh - 120px);
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    display: none;
    flex-direction: column;
    overflow: hidden;
    z-index: 999998;
    animation: slideUp 0.3s ease-out;
  `;

  // Add animation keyframes
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    @media (max-width: 768px) {
      #botsmith-window {
        width: calc(100vw - 20px) !important;
        height: calc(100vh - 100px) !important;
        bottom: 10px !important;
        right: 10px !important;
      }
      #botsmith-widget-container {
        bottom: 10px !important;
        right: 10px !important;
      }
    }
  `;
  document.head.appendChild(style);

  // Create header
  const header = document.createElement('div');
  header.style.cssText = `
    background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%);
    color: white;
    padding: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  `;
  header.innerHTML = `
    <div style="display: flex; align-items: center; gap: 12px;">
      <div style="width: 40px; height: 40px; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.38 14.99 3.06 16.27L2 22L7.73 20.94C9.01 21.62 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C10.69 20 9.45 19.69 8.35 19.14L8 18.96L4.21 19.79L5.04 16.05L4.84 15.68C4.26 14.55 3.94 13.31 3.94 12C3.94 7.59 7.59 3.94 12 3.94C16.41 3.94 20.06 7.59 20.06 12C20.06 16.41 16.41 20 12 20Z" fill="#7c3aed"/>
        </svg>
      </div>
      <div>
        <div style="font-weight: 600; font-size: 16px;">Chat Support</div>
        <div style="font-size: 12px; opacity: 0.9;">Online now</div>
      </div>
    </div>
    <button id="botsmith-close" style="background: transparent; border: none; color: white; cursor: pointer; padding: 4px; display: flex; align-items: center; justify-content: center; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='transparent'">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  `;

  // Create iframe
  const iframe = document.createElement('iframe');
  iframe.src = `${domain}/embed/${chatbotId}`;
  iframe.style.cssText = `
    width: 100%;
    height: 100%;
    border: none;
    flex: 1;
  `;
  iframe.setAttribute('allow', 'clipboard-read; clipboard-write');

  // Assemble chat window
  chatWindow.appendChild(header);
  chatWindow.appendChild(iframe);

  // Assemble widget
  widgetContainer.appendChild(chatBubble);
  widgetContainer.appendChild(chatWindow);

  // Toggle chat window
  let isOpen = false;
  function toggleChat() {
    isOpen = !isOpen;
    if (isOpen) {
      chatWindow.style.display = 'flex';
      chatBubble.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M18 6L6 18M6 6L18 18" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      `;
    } else {
      chatWindow.style.display = 'none';
      chatBubble.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.38 14.99 3.06 16.27L2 22L7.73 20.94C9.01 21.62 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C10.69 20 9.45 19.69 8.35 19.14L8 18.96L4.21 19.79L5.04 16.05L4.84 15.68C4.26 14.55 3.94 13.31 3.94 12C3.94 7.59 7.59 3.94 12 3.94C16.41 3.94 20.06 7.59 20.06 12C20.06 16.41 16.41 20 12 20Z" fill="white"/>
        </svg>
      `;
    }
  }

  chatBubble.addEventListener('click', toggleChat);
  header.querySelector('#botsmith-close').addEventListener('click', (e) => {
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
