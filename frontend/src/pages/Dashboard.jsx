import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Plus, MessageSquare, Activity, TrendingUp, BarChart3, CreditCard, Sparkles, FileText, Globe, BookOpen } from 'lucide-react';
import { useToast } from '../hooks/use-toast';
import UserProfileDropdown from '../components/UserProfileDropdown';
import ResponsiveNav from '../components/ResponsiveNav';
import { useAuth } from '../contexts/AuthContext';
import { chatbotAPI, analyticsAPI, plansAPI } from '../utils/api';
import UpgradeModal from '../components/UpgradeModal';
import Footer from '../components/Footer';

const Dashboard = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { user, logout } = useAuth();
  const [chatbots, setChatbots] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [usageStats, setUsageStats] = useState(null);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [upgradeContext, setUpgradeContext] = useState({});

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [chatbotsResponse, analyticsResponse, usageResponse] = await Promise.all([
        chatbotAPI.list(),
        analyticsAPI.getDashboard(),
        plansAPI.getUsageStats()
      ]);
      
      setChatbots(chatbotsResponse.data);
      setAnalytics(analyticsResponse.data);
      setUsageStats(usageResponse.data);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      toast({
        title: 'Error',
        description: 'Failed to load dashboard data',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    toast({
      title: 'Signed out',
      description: 'You have been signed out successfully'
    });
    navigate('/');
  };

  const handleCreateChatbot = async () => {
    try {
      // Check chatbot limit first
      const limitCheck = await plansAPI.checkLimit('chatbots');
      if (limitCheck.data.reached) {
        setUpgradeContext({
          limitType: 'chatbots',
          currentUsage: limitCheck.data.current,
          maxUsage: limitCheck.data.max
        });
        setShowUpgradeModal(true);
        return;
      }

      const newChatbot = await chatbotAPI.create({
        name: 'New Chatbot',
        model: 'gpt-4o-mini',
        provider: 'openai',
        temperature: 0.7,
        instructions: 'You are a helpful assistant.',
        welcome_message: 'Hello! How can I help you today?'
      });
      
      toast({
        title: 'Success',
        description: 'Chatbot created successfully'
      });
      
      navigate(`/chatbot/${newChatbot.data.id}`);
    } catch (error) {
      console.error('Error creating chatbot:', error);
      toast({
        title: 'Error',
        description: 'Failed to create chatbot',
        variant: 'destructive'
      });
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="relative">
          <div className="w-20 h-20 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin"></div>
          <div className="absolute inset-0 w-20 h-20 border-4 border-transparent border-t-pink-600 rounded-full animate-spin animation-delay-300"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-pink-50 relative overflow-hidden">
      {/* Rich Animated background with multiple layers */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Layer 1: Large slow-moving gradient blobs */}
        <div className="absolute -top-40 -right-40 w-[800px] h-[800px] bg-gradient-to-br from-purple-400 via-pink-400 to-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-1/4 -left-40 w-[700px] h-[700px] bg-gradient-to-br from-pink-400 via-rose-400 to-orange-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-40 right-1/4 w-[750px] h-[750px] bg-gradient-to-br from-blue-400 via-purple-400 to-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
        
        {/* Layer 2: Medium floating orbs */}
        <div className="absolute top-1/3 right-1/3 w-96 h-96 bg-gradient-to-br from-indigo-300 to-purple-300 rounded-full mix-blend-multiply filter blur-2xl opacity-15 animate-float"></div>
        <div className="absolute bottom-1/3 left-1/4 w-80 h-80 bg-gradient-to-br from-pink-300 to-rose-300 rounded-full mix-blend-multiply filter blur-2xl opacity-15 animate-float animation-delay-3000"></div>
        
        {/* Layer 3: Smaller accent orbs */}
        <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-gradient-to-br from-yellow-200 to-orange-200 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse-slow"></div>
        <div className="absolute top-3/4 right-1/2 w-72 h-72 bg-gradient-to-br from-cyan-200 to-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse-slow animation-delay-2000"></div>
      </div>

      {/* Top Navigation */}
      <ResponsiveNav user={user} onLogout={handleLogout} />

      <div className="p-6 sm:p-8 max-w-[95%] mx-auto relative z-10">
        {/* Welcome Header */}
        <div className="mb-8 animate-fade-in">
          <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center gap-3">
            Welcome back, {user?.name || 'Demo User'} 
            <span className="text-4xl">👋</span>
          </h1>
          <p className="text-lg text-gray-600">Here's what's happening with your AI chatbots today</p>
        </div>

        {/* Stats Cards - Matching uploaded UI design */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {/* Total Conversations Card */}
          <div className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 animate-fade-in-up">
            <div className="flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-b from-pink-500 to-purple-600 mb-4 shadow-lg">
              <MessageSquare className="w-8 h-8 text-white" />
            </div>
            <p className="text-5xl font-bold text-purple-600 mb-2">{analytics?.total_conversations?.toLocaleString() || 0}</p>
            <p className="text-gray-600 text-base font-medium">Total Conversations</p>
          </div>
          
          {/* Total Messages Card */}
          <div className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 animate-fade-in-up animation-delay-100">
            <div className="flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-b from-cyan-400 to-blue-500 mb-4 shadow-lg">
              <Activity className="w-8 h-8 text-white" />
            </div>
            <p className="text-5xl font-bold text-cyan-500 mb-2">{analytics?.total_messages?.toLocaleString() || 0}</p>
            <p className="text-gray-600 text-base font-medium">Total Messages</p>
          </div>
          
          {/* Active Chatbots Card */}
          <div className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 animate-fade-in-up animation-delay-200">
            <div className="flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-b from-red-400 to-pink-500 mb-4 shadow-lg">
              <TrendingUp className="w-8 h-8 text-white" />
            </div>
            <p className="text-5xl font-bold text-pink-500 mb-2">{analytics?.active_chatbots || 0}</p>
            <p className="text-gray-600 text-base font-medium">Active Chatbots</p>
          </div>
          
          {/* Total Chatbots Card */}
          <div className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 animate-fade-in-up animation-delay-300">
            <div className="flex items-center justify-center w-16 h-16 rounded-2xl bg-purple-600 mb-4 shadow-lg">
              <BarChart3 className="w-8 h-8 text-white" />
            </div>
            <p className="text-5xl font-bold text-purple-600 mb-2">{analytics?.total_chatbots || 0}</p>
            <p className="text-gray-600 text-base font-medium">Total Chatbots</p>
          </div>
        </div>

        {/* Free Plan Section - Matching uploaded UI design */}
        {usageStats && (
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 mb-8 animate-fade-in-up">
            <div className="flex items-center justify-between mb-6">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-600 to-purple-700 flex items-center justify-center">
                    <Sparkles className="w-5 h-5 text-white" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900">{usageStats.plan?.name} Plan</h2>
                </div>
                <p className="text-sm text-gray-600">Monitor your resource usage and limits</p>
              </div>
              <Button
                onClick={() => navigate('/subscription')}
                className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-6 py-2 rounded-xl font-semibold shadow-lg"
              >
                Upgrade Plan
              </Button>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {/* Chatbots */}
              <div className="bg-white rounded-xl p-5 border border-gray-200 hover:shadow-md transition-all duration-300">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center">
                    <MessageSquare className="w-5 h-5 text-white" />
                  </div>
                  <p className="text-sm font-semibold text-gray-700">Chatbots</p>
                </div>
                <p className="text-3xl font-bold text-gray-900 mb-2">
                  {usageStats.usage?.chatbots?.current}/{usageStats.usage?.chatbots?.limit}
                </p>
                <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden mb-1">
                  <div 
                    className={`h-2 rounded-full transition-all duration-500 ${
                      usageStats.usage?.chatbots?.percentage >= 90 ? 'bg-red-500' : 
                      usageStats.usage?.chatbots?.percentage >= 75 ? 'bg-orange-500' : 
                      'bg-gray-300'
                    }`}
                    style={{ width: `${Math.min(usageStats.usage?.chatbots?.percentage || 0, 100)}%` }}
                  />
                </div>
                <p className="text-xs text-gray-600">{usageStats.usage?.chatbots?.percentage}% used</p>
              </div>

              {/* Messages */}
              <div className="bg-white rounded-xl p-5 border border-gray-200 hover:shadow-md transition-all duration-300">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center">
                    <Activity className="w-5 h-5 text-white" />
                  </div>
                  <p className="text-sm font-semibold text-gray-700">Messages</p>
                </div>
                <p className="text-3xl font-bold text-gray-900 mb-2">
                  {usageStats.usage?.messages?.current}/{usageStats.usage?.messages?.limit === 999999 || usageStats.usage?.messages?.limit === 999999999 ? '∞' : usageStats.usage?.messages?.limit?.toLocaleString()}
                </p>
                <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden mb-1">
                  <div 
                    className="h-2 rounded-full bg-gray-300 transition-all duration-500"
                    style={{ width: `${Math.min(usageStats.usage?.messages?.percentage || 0, 100)}%` }}
                  />
                </div>
                <p className="text-xs text-gray-600">{usageStats.usage?.messages?.percentage}% used</p>
              </div>

              {/* Files */}
              <div className="bg-white rounded-xl p-5 border border-gray-200 hover:shadow-md transition-all duration-300">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-red-400 to-pink-500 flex items-center justify-center">
                    <FileText className="w-5 h-5 text-white" />
                  </div>
                  <p className="text-sm font-semibold text-gray-700">Files</p>
                </div>
                <p className="text-3xl font-bold text-gray-900 mb-2">
                  {usageStats.usage?.file_uploads?.current}/{usageStats.usage?.file_uploads?.limit}
                </p>
                <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden mb-1">
                  <div 
                    className="h-2 rounded-full bg-gray-300 transition-all duration-500"
                    style={{ width: `${Math.min(usageStats.usage?.file_uploads?.percentage || 0, 100)}%` }}
                  />
                </div>
                <p className="text-xs text-gray-600">{usageStats.usage?.file_uploads?.percentage}% used</p>
              </div>

              {/* Websites */}
              <div className="bg-white rounded-xl p-5 border border-gray-200 hover:shadow-md transition-all duration-300">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center">
                    <Globe className="w-5 h-5 text-white" />
                  </div>
                  <p className="text-sm font-semibold text-gray-700">Websites</p>
                </div>
                <p className="text-3xl font-bold text-gray-900 mb-2">
                  {usageStats.usage?.website_sources?.current}/{usageStats.usage?.website_sources?.limit}
                </p>
                <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden mb-1">
                  <div 
                    className="h-2 rounded-full bg-gray-300 transition-all duration-500"
                    style={{ width: `${Math.min(usageStats.usage?.website_sources?.percentage || 0, 100)}%` }}
                  />
                </div>
                <p className="text-xs text-gray-600">{usageStats.usage?.website_sources?.percentage}% used</p>
              </div>

              {/* Text Sources */}
              <div className="bg-white rounded-xl p-5 border border-gray-200 hover:shadow-md transition-all duration-300">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-purple-700 flex items-center justify-center">
                    <BookOpen className="w-5 h-5 text-white" />
                  </div>
                  <p className="text-sm font-semibold text-gray-700">Text Sources</p>
                </div>
                <p className="text-3xl font-bold text-gray-900 mb-2">
                  {usageStats.usage?.text_sources?.current}/{usageStats.usage?.text_sources?.limit}
                </p>
                <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden mb-1">
                  <div 
                    className="h-2 rounded-full bg-gray-300 transition-all duration-500"
                    style={{ width: `${Math.min(usageStats.usage?.text_sources?.percentage || 0, 100)}%` }}
                  />
                </div>
                <p className="text-xs text-gray-600">{usageStats.usage?.text_sources?.percentage}% used</p>
              </div>
            </div>
          </div>
        )}

        {/* Your Chatbots Section - Matching uploaded UI design */}
        <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 animate-fade-in-up">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-1">Your Chatbots</h2>
              <p className="text-sm text-gray-600">Manage and monitor your AI agents</p>
            </div>
            <Button 
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-6 py-2 rounded-xl font-semibold shadow-lg flex items-center gap-2"
              onClick={handleCreateChatbot}
            >
              <Plus className="w-5 h-5" />
              Create New
            </Button>
          </div>
          
          {chatbots.length === 0 ? (
            <div className="text-center py-16 animate-fade-in">
              <div className="w-20 h-20 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-4 transform hover:scale-110 transition-transform duration-300">
                <MessageSquare className="w-10 h-10 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">No chatbots yet</h3>
              <p className="text-gray-600 mb-6">Create your first AI chatbot to get started</p>
              <Button 
                className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg shadow-purple-500/30 transform hover:scale-105 transition-all duration-300"
                onClick={handleCreateChatbot}
              >
                <Plus className="w-4 h-4 mr-2" />
                Create Chatbot
              </Button>
            </div>
          ) : (
            <div className="grid gap-4">
              {chatbots.map((bot, index) => (
                <div 
                  key={bot.id} 
                  className="group p-6 border-2 border-purple-200/50 rounded-2xl hover:border-purple-400 hover:shadow-2xl hover:shadow-purple-500/20 transition-all duration-500 cursor-pointer bg-gradient-to-r from-white to-purple-50/30 transform hover:-translate-y-1 animate-fade-in-up"
                  style={{ animationDelay: `${index * 100}ms` }}
                  onClick={() => navigate(`/chatbot/${bot.id}`)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <h3 className="text-xl font-bold text-gray-900 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-pink-600 group-hover:bg-clip-text transition-all duration-300">{bot.name}</h3>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          bot.status === 'active' ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-lg shadow-green-500/30' : 'bg-gray-200 text-gray-700'
                        }`}>
                          {bot.status}
                        </span>
                      </div>
                      <div className="flex items-center gap-6 text-sm text-gray-600">
                        <span className="flex items-center gap-1">
                          <MessageSquare className="w-4 h-4" />
                          <strong>{bot.conversations_count?.toLocaleString() || 0}</strong> conversations
                        </span>
                        <span className="flex items-center gap-1">
                          <Activity className="w-4 h-4" />
                          <strong>{bot.messages_count?.toLocaleString() || 0}</strong> messages
                        </span>
                        <span className="font-medium">Model: <strong className="text-purple-600">{bot.model}</strong></span>
                        {bot.last_trained && (
                          <span>Last trained: {new Date(bot.last_trained).toLocaleDateString()}</span>
                        )}
                      </div>
                    </div>
                    <Button 
                      variant="outline" 
                      onClick={(e) => { e.stopPropagation(); navigate(`/chatbot/${bot.id}`); }}
                      className="border-2 border-purple-300 hover:bg-gradient-to-r hover:from-purple-600 hover:to-pink-600 hover:text-white hover:border-transparent transition-all duration-300 transform group-hover:scale-105"
                    >
                      Manage
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Upgrade Modal */}
      <UpgradeModal 
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        limitType={upgradeContext.limitType}
        currentUsage={upgradeContext.currentUsage}
        maxUsage={upgradeContext.maxUsage}
      />

      {/* Footer */}
      <Footer variant="dashboard" />
    </div>
  );
};

export default Dashboard;
