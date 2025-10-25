import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Users, Bot, BarChart3, Settings, Activity, Database, Shield, LogOut, MessageSquare, FileText, AlertTriangle, HardDrive } from 'lucide-react';
import UsersManagement from '../../components/admin/UsersManagement';
import ChatbotsManagement from '../../components/admin/ChatbotsManagement';
import ConversationsManagement from '../../components/admin/ConversationsManagement';
import SystemMonitoring from '../../components/admin/SystemMonitoring';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
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
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <nav className="bg-white border-b border-gray-200">
        <div className="px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-red-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">A</span>
              </div>
              <span className="text-xl font-semibold">Admin Dashboard</span>
            </div>
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

      <div className="p-8 max-w-[95%] mx-auto">
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
        <Tabs defaultValue="users" className="w-full">
          <TabsList className="mb-6">
            <TabsTrigger value="users">Users</TabsTrigger>
            <TabsTrigger value="chatbots">Chatbots</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="integrations">Integrations</TabsTrigger>
            <TabsTrigger value="activity">Activity Logs</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          <TabsContent value="users">
            <div className="bg-white rounded-xl border border-gray-200 p-8">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold">User Management</h2>
                <Button className="bg-black hover:bg-gray-800 text-white">
                  Add User
                </Button>
              </div>
              <div className="text-center py-12 text-gray-500">
                <Users className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p>User management interface</p>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="chatbots">
            <div className="bg-white rounded-xl border border-gray-200 p-8">
              <h2 className="text-2xl font-bold mb-6">Chatbot Overview</h2>
              <div className="text-center py-12 text-gray-500">
                <Bot className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p>Chatbot management interface</p>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="analytics">
            <div className="bg-white rounded-xl border border-gray-200 p-8">
              <h2 className="text-2xl font-bold mb-6">System Analytics</h2>
              <div className="text-center py-12 text-gray-500">
                <BarChart3 className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p>Analytics dashboard</p>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="integrations">
            <div className="bg-white rounded-xl border border-gray-200 p-8">
              <h2 className="text-2xl font-bold mb-6">Integration Management</h2>
              <div className="text-center py-12 text-gray-500">
                <Database className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p>Integration settings</p>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="activity">
            <div className="bg-white rounded-xl border border-gray-200 p-8">
              <h2 className="text-2xl font-bold mb-6">Activity Logs</h2>
              <div className="text-center py-12 text-gray-500">
                <Activity className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p>System activity logs</p>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="settings">
            <div className="bg-white rounded-xl border border-gray-200 p-8">
              <h2 className="text-2xl font-bold mb-6">System Settings</h2>
              <div className="text-center py-12 text-gray-500">
                <Settings className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p>System configuration</p>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AdminDashboard;