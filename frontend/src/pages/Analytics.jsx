import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { TrendingUp, MessageSquare, Users, Clock, BarChart3, CreditCard } from 'lucide-react';
import UserProfileDropdown from '../components/UserProfileDropdown';
import ResponsiveNav from '../components/ResponsiveNav';
import { useAuth } from '../contexts/AuthContext';
import { AnalyticsSkeleton } from '../components/LoadingSkeleton';
import Footer from '../components/Footer';
import toast from 'react-hot-toast';
import { analyticsAPI } from '../utils/api';

const Analytics = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadDashboardAnalytics = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await analyticsAPI.getDashboard();
      // Convert backend data to expected format
      const data = response.data;
      setAnalytics({
        totalConversations: data.total_conversations || 0,
        activeChats: data.active_chatbots || 0,
        satisfaction: 0, // This would need additional API call if needed
        avgResponseTime: '0s', // This would need additional API call if needed
        conversationTrend: [],
        topicsDiscussed: []
      });
    } catch (error) {
      console.error('Error loading analytics:', error);
      setError(error.message);
      toast.error('Failed to load analytics data');
      // Set default empty data on error
      setAnalytics({
        totalConversations: 0,
        activeChats: 0,
        satisfaction: 0,
        avgResponseTime: '0s',
        conversationTrend: [],
        topicsDiscussed: []
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardAnalytics();
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  if (loading) {
    return <AnalyticsSkeleton />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-pink-50 relative overflow-hidden animate-fade-in">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-blob"></div>
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-1/4 right-1/3 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-blob animation-delay-4000"></div>
      </div>

      {/* Navigation */}
      <ResponsiveNav currentPage="analytics" user={user} onLogout={handleLogout} />

      <div className="p-6 max-w-[95%] mx-auto relative z-10">
        <div className="mb-8 animate-fade-in-up">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-gray-900 via-purple-900 to-pink-900 bg-clip-text text-transparent">Analytics Overview</h1>
          <p className="text-gray-600">Track your chatbot performance and user engagement</p>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="group bg-white/80 backdrop-blur-sm p-6 rounded-2xl border-2 border-purple-200/50 hover:border-purple-400 hover:shadow-2xl hover:shadow-purple-500/20 transition-all duration-500 transform hover:-translate-y-2 animate-fade-in-up overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-600 to-pink-600 opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
            <div className="relative z-10">
              <div className="p-3 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg shadow-purple-500/30 mb-3 inline-block transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <MessageSquare className="w-6 h-6 text-white" />
              </div>
              <p className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">{analytics?.totalConversations.toLocaleString() || 0}</p>
              <p className="text-gray-600 text-sm mt-2 font-medium">Total Conversations</p>
            </div>
          </div>
          
          <div className="group bg-white/80 backdrop-blur-sm p-6 rounded-2xl border-2 border-blue-200/50 hover:border-blue-400 hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 transform hover:-translate-y-2 animate-fade-in-up animation-delay-300 overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-600 to-cyan-600 opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
            <div className="relative z-10">
              <div className="p-3 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl shadow-lg shadow-blue-500/30 mb-3 inline-block transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <Users className="w-6 h-6 text-white" />
              </div>
              <p className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">{analytics?.activeChats || 0}</p>
              <p className="text-gray-600 text-sm mt-2 font-medium">Active Users</p>
            </div>
          </div>
          
          <div className="group bg-white/80 backdrop-blur-sm p-6 rounded-2xl border-2 border-green-200/50 hover:border-green-400 hover:shadow-2xl hover:shadow-green-500/20 transition-all duration-500 transform hover:-translate-y-2 animate-fade-in-up animation-delay-500 overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-br from-green-600 to-emerald-600 opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
            <div className="relative z-10">
              <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl shadow-lg shadow-green-500/30 mb-3 inline-block transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <p className="text-4xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">{analytics?.satisfaction || 0}%</p>
              <p className="text-gray-600 text-sm mt-2 font-medium">Satisfaction Rate</p>
            </div>
          </div>
          
          <div className="group bg-white/80 backdrop-blur-sm p-6 rounded-2xl border-2 border-orange-200/50 hover:border-orange-400 hover:shadow-2xl hover:shadow-orange-500/20 transition-all duration-500 transform hover:-translate-y-2 animate-fade-in-up animation-delay-700 overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-br from-orange-600 to-red-600 opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
            <div className="relative z-10">
              <div className="p-3 bg-gradient-to-br from-orange-500 to-red-600 rounded-xl shadow-lg shadow-orange-500/30 mb-3 inline-block transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <Clock className="w-6 h-6 text-white" />
              </div>
              <p className="text-4xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">{analytics?.avgResponseTime || '0s'}</p>
              <p className="text-gray-600 text-sm mt-2 font-medium">Avg Response Time</p>
            </div>
          </div>
        </div>

        {analytics && analytics.totalConversations === 0 && (
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl border-2 border-purple-200/50 p-16 text-center shadow-xl animate-fade-in">
            <div className="w-20 h-20 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-4 transform hover:scale-110 transition-transform duration-300">
              <BarChart3 className="w-10 h-10 text-purple-600" />
            </div>
            <h3 className="text-2xl font-bold mb-2 text-gray-900">No analytics data yet</h3>
            <p className="text-gray-600 mb-6">Create a chatbot and start conversations to see analytics here</p>
            <Button 
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg shadow-purple-500/30 transform hover:scale-105 transition-all duration-300"
              onClick={() => navigate('/dashboard')}
            >
              Go to Dashboard
            </Button>
          </div>
        )}

        {analytics && analytics.conversationTrend && analytics.conversationTrend.length > 0 && (
          <>
            {/* Conversation Trend */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl border-2 border-purple-200/50 p-8 mb-8 shadow-xl animate-fade-in-up">
              <h2 className="text-2xl font-bold mb-6 bg-gradient-to-r from-gray-900 to-purple-600 bg-clip-text text-transparent">Conversation Trend</h2>
              <div className="h-64 flex items-end gap-3">
                {analytics?.conversationTrend.map((item, index) => (
                  <div key={index} className="flex-1 flex flex-col items-center group">
                    <div
                      className="w-full bg-gradient-to-t from-purple-600 to-pink-600 rounded-t-xl transition-all hover:from-purple-700 hover:to-pink-700 shadow-lg hover:shadow-purple-500/50 transform hover:scale-105"
                      style={{ height: `${(item.count / 250) * 100}%` }}
                    ></div>
                    <p className="text-xs text-gray-500 mt-2 font-medium group-hover:text-purple-600 transition-colors">{item.date.split('-')[2]}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Top Topics */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl border-2 border-purple-200/50 p-8 shadow-xl animate-fade-in-up">
              <h2 className="text-2xl font-bold mb-6 bg-gradient-to-r from-gray-900 to-purple-600 bg-clip-text text-transparent">Top Discussion Topics</h2>
              <div className="space-y-4">
                {analytics?.topicsDiscussed.map((topic, index) => (
                  <div key={index} className="group p-4 rounded-xl hover:bg-purple-50 transition-all duration-300">
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-3">
                        <span className="font-semibold text-gray-900 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-pink-600 group-hover:bg-clip-text transition-all">{topic.topic}</span>
                        <span className="text-sm text-gray-500 font-medium">{topic.count} mentions</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
                        <div
                          className="bg-gradient-to-r from-purple-600 to-pink-600 h-2.5 rounded-full transition-all duration-1000 ease-out shadow-sm"
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

      {/* Footer */}
      <Footer variant="dashboard" />
    </div>
  );
};

export default Analytics;