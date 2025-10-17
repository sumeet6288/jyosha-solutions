import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { LogOut, TrendingUp, MessageSquare, Users, Clock, BarChart3, Settings } from 'lucide-react';
import { mockAnalytics } from '../mock/mockData';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '../components/ui/dropdown-menu';

const Analytics = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    const userData = localStorage.getItem('chatbase_user');
    if (!userData) {
      navigate('/signin');
      return;
    }
    setUser(JSON.parse(userData));
    setAnalytics(mockAnalytics);
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('chatbase_user');
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
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
              <button onClick={() => navigate('/dashboard')} className="text-gray-600 hover:text-black transition-colors">Chatbots</button>
              <button className="text-black font-medium">Analytics</button>
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
        <h1 className="text-3xl font-bold mb-8">Analytics Overview</h1>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <MessageSquare className="w-8 h-8 text-gray-600 mb-3" />
            <p className="text-3xl font-bold">{analytics?.totalConversations.toLocaleString() || 0}</p>
            <p className="text-gray-600 text-sm mt-1">Total Conversations</p>
          </div>
          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <Users className="w-8 h-8 text-gray-600 mb-3" />
            <p className="text-3xl font-bold">{analytics?.activeChats || 0}</p>
            <p className="text-gray-600 text-sm mt-1">Active Users</p>
          </div>
          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <TrendingUp className="w-8 h-8 text-gray-600 mb-3" />
            <p className="text-3xl font-bold">{analytics?.satisfaction || 0}%</p>
            <p className="text-gray-600 text-sm mt-1">Satisfaction Rate</p>
          </div>
          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <Clock className="w-8 h-8 text-gray-600 mb-3" />
            <p className="text-3xl font-bold">{analytics?.avgResponseTime || '0s'}</p>
            <p className="text-gray-600 text-sm mt-1">Avg Response Time</p>
          </div>
        </div>

        {analytics && analytics.totalConversations === 0 && (
          <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
            <BarChart3 className="w-16 h-16 mx-auto mb-4 text-gray-400" />
            <h3 className="text-xl font-semibold mb-2">No analytics data yet</h3>
            <p className="text-gray-600 mb-6">Create a chatbot and start conversations to see analytics here</p>
            <Button 
              className="bg-black hover:bg-gray-800 text-white"
              onClick={() => navigate('/dashboard')}
            >
              Go to Dashboard
            </Button>
          </div>
        )}

        {analytics && analytics.conversationTrend && analytics.conversationTrend.length > 0 && (
          <>
            {/* Conversation Trend */}
            <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
              <h2 className="text-xl font-bold mb-6">Conversation Trend</h2>
              <div className="h-64 flex items-end gap-4">
                {analytics?.conversationTrend.map((item, index) => (
                  <div key={index} className="flex-1 flex flex-col items-center">
                    <div
                      className="w-full bg-black rounded-t-lg transition-all hover:bg-gray-700"
                      style={{ height: `${(item.count / 250) * 100}%` }}
                    ></div>
                    <p className="text-xs text-gray-500 mt-2">{item.date.split('-')[2]}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Top Topics */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-xl font-bold mb-6">Top Discussion Topics</h2>
              <div className="space-y-4">
                {analytics?.topicsDiscussed.map((topic, index) => (
                  <div key={index} className="flex items-center gap-4">
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">{topic.topic}</span>
                        <span className="text-sm text-gray-500">{topic.count} mentions</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-black h-2 rounded-full transition-all"
                          style={{ width: `${(topic.count / 500) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Analytics;