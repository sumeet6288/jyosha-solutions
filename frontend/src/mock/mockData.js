// Mock data for Chatbase replica

export const mockChatbots = [
  {
    id: '1',
    name: 'Customer Support Bot',
    status: 'active',
    conversations: 1247,
    sources: 5,
    lastTrained: '2025-01-10',
    model: 'gpt-4',
    createdAt: '2024-12-01'
  },
  {
    id: '2',
    name: 'Sales Assistant',
    status: 'active',
    conversations: 856,
    sources: 3,
    lastTrained: '2025-01-09',
    model: 'gpt-4',
    createdAt: '2024-12-15'
  },
  {
    id: '3',
    name: 'Product FAQ Bot',
    status: 'inactive',
    conversations: 423,
    sources: 8,
    lastTrained: '2025-01-05',
    model: 'gpt-3.5-turbo',
    createdAt: '2024-11-20'
  }
];

export const mockAnalytics = {
  totalConversations: 2526,
  activeChats: 47,
  avgResponseTime: '2.3s',
  satisfaction: 94,
  topicsDiscussed: [
    { topic: 'Pricing', count: 423 },
    { topic: 'Integration', count: 387 },
    { topic: 'Features', count: 312 },
    { topic: 'Support', count: 289 },
    { topic: 'Account', count: 234 }
  ],
  conversationTrend: [
    { date: '2025-01-04', count: 156 },
    { date: '2025-01-05', count: 178 },
    { date: '2025-01-06', count: 145 },
    { date: '2025-01-07', count: 192 },
    { date: '2025-01-08', count: 201 },
    { date: '2025-01-09', count: 187 },
    { date: '2025-01-10', count: 213 }
  ]
};

export const mockSources = [
  {
    id: '1',
    type: 'file',
    name: 'Product Documentation.pdf',
    size: '2.4 MB',
    status: 'processed',
    addedAt: '2025-01-08'
  },
  {
    id: '2',
    type: 'website',
    name: 'https://example.com/help',
    status: 'processed',
    addedAt: '2025-01-07'
  },
  {
    id: '3',
    type: 'text',
    name: 'FAQ Content',
    status: 'processing',
    addedAt: '2025-01-10'
  }
];

export const mockConversations = [
  {
    id: '1',
    user: 'John Doe',
    lastMessage: 'How do I integrate this with my website?',
    timestamp: '2025-01-10T14:32:00',
    status: 'resolved'
  },
  {
    id: '2',
    user: 'Jane Smith',
    lastMessage: 'What pricing plans do you offer?',
    timestamp: '2025-01-10T14:28:00',
    status: 'active'
  },
  {
    id: '3',
    user: 'Mike Johnson',
    lastMessage: 'I need help with API integration',
    timestamp: '2025-01-10T14:15:00',
    status: 'escalated'
  }
];

export const mockChatMessages = [
  {
    id: '1',
    role: 'assistant',
    content: 'Hello! How can I help you today?',
    timestamp: '2025-01-10T14:30:00'
  },
  {
    id: '2',
    role: 'user',
    content: 'How do I integrate this with my website?',
    timestamp: '2025-01-10T14:32:00'
  },
  {
    id: '3',
    role: 'assistant',
    content: 'To integrate the chatbot with your website, you can use our embed code. Simply copy the script tag from your dashboard and paste it before the closing </body> tag in your HTML.',
    timestamp: '2025-01-10T14:32:15'
  }
];
