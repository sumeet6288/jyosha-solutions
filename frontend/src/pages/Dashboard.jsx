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
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="group bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-purple-200/50 hover:border-purple-400 hover:shadow-2xl hover:shadow-purple-500/20 transition-all duration-500 transform hover:-translate-y-2 animate-fade-in-up overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-600 to-pink-600 opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
            <div className="flex items-center justify-between mb-2 relative z-10">
              <div className="p-3 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg shadow-purple-500/30 transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <MessageSquare className="w-6 h-6 text-white" />
              </div>
            </div>
            <p className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">{analytics?.total_conversations?.toLocaleString() || 0}</p>
            <p className="text-gray-600 text-sm mt-2 font-medium">Total Conversations</p>
          </div>
          
          <div className="group bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-blue-200/50 hover:border-blue-400 hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 transform hover:-translate-y-2 animate-fade-in-up animation-delay-300 overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-600 to-cyan-600 opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
            <div className="flex items-center justify-between mb-2 relative z-10">
              <div className="p-3 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl shadow-lg shadow-blue-500/30 transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <Activity className="w-6 h-6 text-white" />
              </div>
            </div>
            <p className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">{analytics?.total_messages?.toLocaleString() || 0}</p>
            <p className="text-gray-600 text-sm mt-2 font-medium">Total Messages</p>
          </div>
          
          <div className="group bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-green-200/50 hover:border-green-400 hover:shadow-2xl hover:shadow-green-500/20 transition-all duration-500 transform hover:-translate-y-2 animate-fade-in-up animation-delay-500 overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-br from-green-600 to-emerald-600 opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
            <div className="flex items-center justify-between mb-2 relative z-10">
              <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl shadow-lg shadow-green-500/30 transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
            </div>
            <p className="text-4xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">{analytics?.active_chatbots || 0}</p>
            <p className="text-gray-600 text-sm mt-2 font-medium">Active Chatbots</p>
          </div>
          
          <div className="group bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-orange-200/50 hover:border-orange-400 hover:shadow-2xl hover:shadow-orange-500/20 transition-all duration-500 transform hover:-translate-y-2 animate-fade-in-up animation-delay-700 overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-br from-orange-600 to-pink-600 opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
            <div className="flex items-center justify-between mb-2 relative z-10">
              <div className="p-3 bg-gradient-to-br from-orange-500 to-pink-600 rounded-xl shadow-lg shadow-orange-500/30 transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
            </div>
            <p className="text-4xl font-bold bg-gradient-to-r from-orange-600 to-pink-600 bg-clip-text text-transparent">{analytics?.total_chatbots || 0}</p>
            <p className="text-gray-600 text-sm mt-2 font-medium">Total Chatbots</p>
          </div>
        </div>

        {/* Plan Usage Widget */}
        {usageStats && (
          <div className="bg-gradient-to-br from-purple-600 via-pink-600 to-orange-500 rounded-2xl border-2 border-white/50 p-1 mb-8 animate-fade-in-up shadow-2xl">
            <div className="bg-white/95 backdrop-blur-sm rounded-xl p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <Sparkles className="w-5 h-5 text-purple-600" />
                    <h3 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">{usageStats.plan?.name} Plan</h3>
                  </div>
                  <p className="text-sm text-gray-600">Current usage overview</p>
                </div>
                <Button
                  onClick={() => navigate('/subscription')}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg shadow-purple-500/30 transform hover:scale-105 transition-all duration-300"
                >
                  View Details
                </Button>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                {[
                  { label: 'Chatbots', current: usageStats.usage?.chatbots?.current, limit: usageStats.usage?.chatbots?.limit, percentage: usageStats.usage?.chatbots?.percentage },
                  { label: 'Messages', current: usageStats.usage?.messages?.current, limit: usageStats.usage?.messages?.limit, percentage: usageStats.usage?.messages?.percentage },
                  { label: 'Files', current: usageStats.usage?.file_uploads?.current, limit: usageStats.usage?.file_uploads?.limit, percentage: usageStats.usage?.file_uploads?.percentage },
                  { label: 'Websites', current: usageStats.usage?.website_sources?.current, limit: usageStats.usage?.website_sources?.limit, percentage: usageStats.usage?.website_sources?.percentage },
                  { label: 'Text Sources', current: usageStats.usage?.text_sources?.current, limit: usageStats.usage?.text_sources?.limit, percentage: usageStats.usage?.text_sources?.percentage }
                ].map((item, index) => (
                  <div key={index} className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-4 border border-purple-200/50 hover:border-purple-400 hover:shadow-lg transition-all duration-300 transform hover:scale-105">
                    <p className="text-xs text-gray-600 mb-1 font-medium">{item.label}</p>
                    <p className="text-xl font-bold text-gray-900">
                      {item.current}/{item.limit === 999999 || item.limit === 999999999 ? '∞' : item.limit?.toLocaleString()}
                    </p>
                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                      <div 
                        className={`h-2 rounded-full transition-all duration-500 ${
                          item.percentage >= 90 ? 'bg-gradient-to-r from-red-500 to-red-600' : 
                          item.percentage >= 75 ? 'bg-gradient-to-r from-orange-500 to-orange-600' : 
                          'bg-gradient-to-r from-green-500 to-emerald-600'
                        }`}
                        style={{ width: `${Math.min(item.percentage || 0, 100)}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Chatbots Section */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-purple-200/50 p-8 shadow-xl animate-fade-in-up">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-purple-600 bg-clip-text text-transparent">Your Chatbots</h2>
            <Button 
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg shadow-purple-500/30 transform hover:scale-105 transition-all duration-300 group"
              onClick={handleCreateChatbot}
            >
              <Plus className="w-4 h-4 mr-2 group-hover:rotate-90 transition-transform duration-300" />
              New Chatbot
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
