import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Plus, MessageSquare, Activity, TrendingUp, BarChart3, LogOut, Settings, Users } from 'lucide-react';
import { mockChatbots, mockAnalytics } from '../mock/mockData';
import { useToast } from '../hooks/use-toast';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '../components/ui/dropdown-menu';

const Dashboard = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [chatbots, setChatbots] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const userData = localStorage.getItem('chatbase_user');
    if (!userData) {
      navigate('/signin');
      return;
    }
    setUser(JSON.parse(userData));
    setChatbots(mockChatbots);
    setAnalytics(mockAnalytics);
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('chatbase_user');
    toast({
      title: 'Signed out',
      description: 'You have been signed out successfully'
    });
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate('/dashboard')}>
              <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">C</span>
              </div>
              <span className="text-xl font-semibold">Chatbase</span>
            </div>
            <div className="flex items-center gap-6">
              <button className="text-black font-medium">Chatbots</button>
              <button onClick={() => navigate('/analytics')} className="text-gray-600 hover:text-black transition-colors">Analytics</button>
              <button onClick={() => navigate('/integrations')} className="text-gray-600 hover:text-black transition-colors">Integrations</button>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className="flex items-center gap-3 hover:bg-gray-50 rounded-lg px-3 py-2 transition-colors cursor-pointer">
                  <div className="text-right">
                    <p className="text-sm font-medium">{user?.name}</p>
                    <p className="text-xs text-gray-500">{user?.email}</p>
                  </div>
                  <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-500 rounded-full flex items-center justify-center text-white font-semibold">
                    {user?.name?.charAt(0).toUpperCase()}
                  </div>
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-64">
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">{user?.name}</p>
                    <p className="text-xs leading-none text-muted-foreground">{user?.email}</p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => navigate('/dashboard')} className="cursor-pointer">
                  <MessageSquare className="mr-2 h-4 w-4" />
                  Dashboard
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => navigate('/account-settings')} className="cursor-pointer">
                  <Settings className="mr-2 h-4 w-4" />
                  Account settings
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => navigate('/workspace')} className="cursor-pointer">
                  <Users className="mr-2 h-4 w-4" />
                  Create or join workspace
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout} className="cursor-pointer text-red-600 focus:text-red-600">
                  <LogOut className="mr-2 h-4 w-4" />
                  Sign out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </nav>

      <div className="p-6 max-w-7xl mx-auto">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl border border-gray-200 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <MessageSquare className="w-8 h-8 text-gray-600" />
              <span className="text-green-500 text-sm font-medium">+12%</span>
            </div>
            <p className="text-3xl font-bold">{analytics?.totalConversations.toLocaleString()}</p>
            <p className="text-gray-600 text-sm mt-1">Total Conversations</p>
          </div>
          
          <div className="bg-white p-6 rounded-xl border border-gray-200 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <Activity className="w-8 h-8 text-gray-600" />
              <span className="text-green-500 text-sm font-medium">Live</span>
            </div>
            <p className="text-3xl font-bold">{analytics?.activeChats}</p>
            <p className="text-gray-600 text-sm mt-1">Active Chats</p>
          </div>
          
          <div className="bg-white p-6 rounded-xl border border-gray-200 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="w-8 h-8 text-gray-600" />
              <span className="text-green-500 text-sm font-medium">+8%</span>
            </div>
            <p className="text-3xl font-bold">{analytics?.satisfaction}%</p>
            <p className="text-gray-600 text-sm mt-1">Satisfaction Rate</p>
          </div>
          
          <div className="bg-white p-6 rounded-xl border border-gray-200 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <BarChart3 className="w-8 h-8 text-gray-600" />
            </div>
            <p className="text-3xl font-bold">{analytics?.avgResponseTime}</p>
            <p className="text-gray-600 text-sm mt-1">Avg Response Time</p>
          </div>
        </div>

        {/* Chatbots Section */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">Your Chatbots</h2>
            <Button 
              className="bg-black hover:bg-gray-800 text-white"
              onClick={() => navigate('/chatbot/new')}
            >
              <Plus className="w-4 h-4 mr-2" />
              New Chatbot
            </Button>
          </div>
          
          {chatbots.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <MessageSquare className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-semibold mb-2">No chatbots yet</h3>
              <p className="text-gray-600 mb-6">Create your first AI chatbot to get started</p>
              <Button 
                className="bg-black hover:bg-gray-800 text-white"
                onClick={() => navigate('/chatbot/new')}
              >
                <Plus className="w-4 h-4 mr-2" />
                Create Chatbot
              </Button>
            </div>
          ) : (
            <div className="grid gap-4">
              {chatbots.map((bot) => (
                <div 
                  key={bot.id} 
                  className="p-6 border border-gray-200 rounded-xl hover:border-gray-300 hover:shadow-md transition-all cursor-pointer"
                  onClick={() => navigate(`/chatbot/${bot.id}`)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold">{bot.name}</h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          bot.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                        }`}>
                          {bot.status}
                        </span>
                      </div>
                      <div className="flex items-center gap-6 text-sm text-gray-600">
                        <span>{bot.conversations.toLocaleString()} conversations</span>
                        <span>{bot.sources} sources</span>
                        <span>Model: {bot.model}</span>
                        <span>Last trained: {bot.lastTrained}</span>
                      </div>
                    </div>
                    <Button variant="outline" onClick={(e) => { e.stopPropagation(); navigate(`/chatbot/${bot.id}`); }}>
                      Manage
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
