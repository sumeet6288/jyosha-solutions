import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../../components/ui/button';
import { Users, Bot, BarChart3, Database, LogOut, FileText, AlertTriangle, Shield } from 'lucide-react';
import AdminSidebar from '../../components/admin/AdminSidebar';
import UsersManagement from '../../components/admin/UsersManagement';
import EnhancedUsersManagement from '../../components/admin/EnhancedUsersManagement';
import ChatbotsManagement from '../../components/admin/ChatbotsManagement';
import ConversationsManagement from '../../components/admin/ConversationsManagement';
import SystemMonitoring from '../../components/admin/SystemMonitoring';
import RevenueDashboard from '../../components/admin/RevenueDashboard';
import AdvancedAnalytics from '../../components/admin/AdvancedAnalytics';
import SystemSettings from '../../components/admin/SystemSettings';
import ActivityLogs from '../../components/admin/ActivityLogs';
import ContactSalesManagement from '../../components/admin/ContactSalesManagement';
import AdvancedUserSearch from '../../components/admin/AdvancedUserSearch';
import UserSegmentation from '../../components/admin/UserSegmentation';
import EmailCampaignBuilder from '../../components/admin/EmailCampaignBuilder';
import LifecycleManagement from '../../components/admin/LifecycleManagement';
import ImpersonationPanel from '../../components/admin/ImpersonationPanel';
import LeadsManagement from '../../components/admin/LeadsManagement';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState({
    totalUsers: 0,
    activeChatbots: 0,
    totalMessages: 0,
    activeIntegrations: 0
  });
  const [sources, setSources] = useState([]);
  const [flaggedContent, setFlaggedContent] = useState([]);
  const [loading, setLoading] = useState(true);
  const backendUrl = process.env.REACT_APP_BACKEND_URL || '';

  useEffect(() => {
    // For demo purposes, set a default admin user
    setUser({
      name: 'Admin User',
      email: 'admin@botsmith.co'
    });

    // Fetch real stats from backend
    fetchAdminStats();
    fetchSources();
    fetchFlaggedContent();
  }, [navigate]);

  const fetchAdminStats = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${backendUrl}/api/admin/stats`);
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching admin stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSources = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/admin/sources`);
      const data = await response.json();
      setSources(data.sources || []);
    } catch (error) {
      console.error('Error fetching sources:', error);
    }
  };

  const fetchFlaggedContent = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/admin/moderation/flagged`);
      const data = await response.json();
      setFlaggedContent(data.flagged_conversations || []);
    } catch (error) {
      console.error('Error fetching flagged content:', error);
    }
  };

  const deleteSource = async (sourceId) => {
    if (!window.confirm('Are you sure you want to delete this source?')) {
      return;
    }

    try {
      const response = await fetch(`${backendUrl}/api/admin/sources/${sourceId}`, {
        method: 'DELETE'
      });
      const data = await response.json();
      if (data.success) {
        alert('Source deleted successfully');
        fetchSources();
      }
    } catch (error) {
      console.error('Error deleting source:', error);
      alert('Failed to delete source');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('botsmith_user');
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <AdminSidebar activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Main Content Area */}
      <div className="flex-1 ml-64 transition-all duration-300">
        {/* Header */}
        <nav className="bg-white border-b border-gray-200">
          <div className="px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-8">
              <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium">{user?.name}</p>
                <p className="text-xs text-gray-500">Administrator</p>
              </div>
              <Button variant="ghost" size="icon" onClick={handleLogout}>
                <LogOut className="w-5 h-5" />
              </Button>
            </div>
          </div>
        </nav>

        <div className="p-8">
          {/* Stats Overview */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div className="bg-white p-8 rounded-xl border border-gray-200 hover:shadow-lg transition-shadow">
              <Users className="w-8 h-8 text-blue-600 mb-3" />
              <p className="text-3xl font-bold">
                {loading ? '...' : stats.totalUsers.toLocaleString()}
              </p>
              <p className="text-gray-600 text-sm mt-1">Total Users</p>
            </div>
            <div className="bg-white p-8 rounded-xl border border-gray-200 hover:shadow-lg transition-shadow">
              <Bot className="w-8 h-8 text-green-600 mb-3" />
              <p className="text-3xl font-bold">
                {loading ? '...' : stats.activeChatbots.toLocaleString()}
              </p>
              <p className="text-gray-600 text-sm mt-1">Active Chatbots</p>
            </div>
            <div className="bg-white p-8 rounded-xl border border-gray-200 hover:shadow-lg transition-shadow">
              <BarChart3 className="w-8 h-8 text-purple-600 mb-3" />
              <p className="text-3xl font-bold">
                {loading ? '...' : stats.totalMessages.toLocaleString()}
              </p>
              <p className="text-gray-600 text-sm mt-1">Total Messages</p>
            </div>
            <div className="bg-white p-8 rounded-xl border border-gray-200 hover:shadow-lg transition-shadow">
              <Database className="w-8 h-8 text-orange-600 mb-3" />
              <p className="text-3xl font-bold">
                {loading ? '...' : stats.activeIntegrations.toLocaleString()}
              </p>
              <p className="text-gray-600 text-sm mt-1">Integrations</p>
            </div>
          </div>

          {/* Main Content */}
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Quick Stats */}
              <div className="bg-white rounded-xl border border-gray-200 p-6">
                <h3 className="text-xl font-bold mb-4">Quick Stats</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                    <span className="font-medium">Total Sources</span>
                    <span className="text-2xl font-bold text-blue-600">{sources.length}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-red-50 rounded-lg">
                    <span className="font-medium">Flagged Content</span>
                    <span className="text-2xl font-bold text-red-600">{flaggedContent.length}</span>
                  </div>
                </div>
              </div>

              {/* Recent Sources */}
              <div className="bg-white rounded-xl border border-gray-200 p-6">
                <h3 className="text-xl font-bold mb-4">Recent Sources</h3>
                <div className="space-y-2">
                  {sources.slice(0, 5).map((source) => (
                    <div key={source.id} className="flex items-center justify-between p-2 hover:bg-gray-50 rounded">
                      <div>
                        <p className="font-medium text-sm">{source.name}</p>
                        <p className="text-xs text-gray-500">{source.type}</p>
                      </div>
                      <span className="text-xs text-gray-400">
                        {new Date(source.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  ))}
                  {sources.length === 0 && (
                    <p className="text-center text-gray-500 py-4">No sources yet</p>
                  )}
                </div>
              </div>

              {/* Flagged Conversations */}
              <div className="bg-white rounded-xl border border-gray-200 p-6 lg:col-span-2">
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <AlertTriangle className="w-6 h-6 text-red-600" />
                  Flagged Conversations
                </h3>
                {flaggedContent.length === 0 ? (
                  <p className="text-center text-gray-500 py-8">No flagged content</p>
                ) : (
                  <div className="space-y-3">
                    {flaggedContent.map((conv) => (
                      <div key={conv.conversation_id} className="p-4 border border-red-200 bg-red-50 rounded-lg">
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <span className="font-medium">{conv.user_name || 'Anonymous'}</span>
                            <span className="text-sm text-gray-600 ml-2">
                              ({new Date(conv.created_at).toLocaleDateString()})
                            </span>
                          </div>
                          <span className="px-3 py-1 bg-red-600 text-white rounded-full text-xs">
                            {conv.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700">{conv.flag_reason}</p>
                        <p className="text-xs text-gray-500 mt-2">
                          {conv.messages?.length || 0} messages
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="advanced-search">
            <AdvancedUserSearch backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="segmentation">
            <UserSegmentation backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="email-campaigns">
            <EmailCampaignBuilder backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="lifecycle">
            <LifecycleManagement backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="impersonation">
            <ImpersonationPanel backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="revenue">
            <RevenueDashboard backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="users">
            <EnhancedUsersManagement backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="chatbots">
            <ChatbotsManagement backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="conversations">
            <ConversationsManagement backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="sources">
            <div className="bg-white rounded-xl border border-gray-200 p-8">
              <h2 className="text-2xl font-bold mb-6">Sources Management</h2>
              {sources.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  <FileText className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p>No sources found</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Name</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Type</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Chatbot</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Size</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Created</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {sources.map((source) => (
                        <tr key={source.id} className="border-b border-gray-100 hover:bg-gray-50">
                          <td className="py-3 px-4 font-medium">{source.name}</td>
                          <td className="py-3 px-4">
                            <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">
                              {source.type}
                            </span>
                          </td>
                          <td className="py-3 px-4 font-mono text-xs">{source.chatbot_id.substring(0, 8)}...</td>
                          <td className="py-3 px-4 text-sm">{source.file_size ? `${(source.file_size / 1024).toFixed(2)} KB` : 'N/A'}</td>
                          <td className="py-3 px-4">
                            <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
                              {source.status || 'active'}
                            </span>
                          </td>
                          <td className="py-3 px-4 text-sm text-gray-600">
                            {new Date(source.created_at).toLocaleDateString()}
                          </td>
                          <td className="py-3 px-4">
                            <Button
                              size="sm"
                              variant="ghost"
                              onClick={() => deleteSource(source.id)}
                            >
                              <LogOut className="w-4 h-4 text-red-600" />
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="monitoring">
            <SystemMonitoring backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="analytics">
            <AdvancedAnalytics backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="logs">
            <ActivityLogs backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="leads">
            <LeadsManagement />
          </TabsContent>

          <TabsContent value="contact-sales">
            <ContactSalesManagement backendUrl={backendUrl} />
          </TabsContent>

          <TabsContent value="moderation">
            <div className="bg-white rounded-xl border border-gray-200 p-8">
              <h2 className="text-2xl font-bold mb-6">Content Moderation</h2>
              {flaggedContent.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  <Shield className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p>No flagged content to review</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {flaggedContent.map((conv) => (
                    <div key={conv.conversation_id} className="p-6 border border-gray-200 rounded-lg">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h3 className="font-bold text-lg">{conv.user_name || 'Anonymous User'}</h3>
                          <p className="text-sm text-gray-600">
                            Conversation ID: {conv.conversation_id.substring(0, 16)}...
                          </p>
                        </div>
                        <span className="px-4 py-2 bg-red-100 text-red-700 rounded-full font-medium">
                          {conv.status}
                        </span>
                      </div>
                      <div className="mb-4">
                        <p className="text-sm font-medium text-gray-700 mb-2">Reason:</p>
                        <p className="text-sm text-gray-600">{conv.flag_reason}</p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-2">Messages:</p>
                        <div className="space-y-2 max-h-60 overflow-y-auto">
                          {conv.messages?.map((msg, idx) => (
                            <div key={idx} className={`p-3 rounded-lg ${
                              msg.role === 'user' ? 'bg-blue-50' : 'bg-gray-50'
                            }`}>
                              <p className="text-xs font-semibold text-gray-500 mb-1">
                                {msg.role === 'user' ? 'USER' : 'ASSISTANT'}
                              </p>
                              <p className="text-sm">{msg.content}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="settings">
            <SystemSettings backendUrl={backendUrl} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AdminDashboard;