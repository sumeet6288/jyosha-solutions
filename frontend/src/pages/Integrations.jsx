import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Check, X, CreditCard, Zap, MessageCircle, Headphones, Phone, Database } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '../components/ui/dialog';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { useToast } from '../hooks/use-toast';
import UserProfileDropdown from '../components/UserProfileDropdown';
import ResponsiveNav from '../components/ResponsiveNav';
import { useAuth } from '../contexts/AuthContext';
import Footer from '../components/Footer';
import { DashboardSkeleton } from '../components/LoadingSkeleton';
import api from '../services/api';

const Integrations = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { user, logout } = useAuth();
  const [selectedIntegration, setSelectedIntegration] = useState(null);
  const [isConnectModalOpen, setIsConnectModalOpen] = useState(false);
  const [isManageModalOpen, setIsManageModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [connectionData, setConnectionData] = useState({
    apiKey: '',
    webhookUrl: '',
    workspaceId: '',
    phoneNumber: ''
  });

  const integrationIcons = {
    'Stripe': CreditCard,
    'Calendly': Zap,
    'Slack': MessageCircle,
    'Zendesk': Headphones,
    'WhatsApp': Phone,
    'Salesforce': Database
  };

  const integrationGradients = {
    'Stripe': 'from-purple-500 to-indigo-600',
    'Calendly': 'from-blue-500 to-cyan-600',
    'Slack': 'from-pink-500 to-rose-600',
    'Zendesk': 'from-green-500 to-emerald-600',
    'WhatsApp': 'from-teal-500 to-green-600',
    'Salesforce': 'from-orange-500 to-red-600'
  };

  const integrationDescriptions = {
    'Stripe': 'Accept payments directly in chat',
    'Calendly': 'Schedule appointments seamlessly',
    'Slack': 'Deploy chatbot to Slack workspace',
    'Zendesk': 'Sync conversations to Zendesk',
    'WhatsApp': 'Deploy on WhatsApp Business',
    'Salesforce': 'Integrate with Salesforce CRM'
  };

  const [integrations, setIntegrations] = useState([]);

  useEffect(() => {
    fetchIntegrations();
  }, []);

  const fetchIntegrations = async () => {
    try {
      setLoading(true);
      const response = await api.get('/integrations/');
      const integrationsData = response.data.map(int => ({
        id: int.id || int.name,
        name: int.name,
        description: integrationDescriptions[int.name],
        connected: int.connected,
        connected_at: int.connected_at,
        config: int.config
      }));
      setIntegrations(integrationsData);
    } catch (error) {
      console.error('Error fetching integrations:', error);
      toast({
        title: 'Error',
        description: 'Failed to load integrations',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleConnect = (integration) => {
    setSelectedIntegration(integration);
    setIsConnectModalOpen(true);
    setConnectionData({ apiKey: '', webhookUrl: '', workspaceId: '', phoneNumber: '' });
  };

  const handleManage = (integration) => {
    setSelectedIntegration(integration);
    setIsManageModalOpen(true);
  };

  const handleConfirmConnect = async () => {
    if (!connectionData.apiKey) {
      toast({
        title: 'Error',
        description: 'API Key is required',
        variant: 'destructive'
      });
      return;
    }

    try {
      await api.post('/integrations/connect', {
        name: selectedIntegration.name,
        api_key: connectionData.apiKey,
        webhook_url: connectionData.webhookUrl,
        workspace_id: connectionData.workspaceId,
        phone_number: connectionData.phoneNumber
      });

      toast({
        title: 'Connected!',
        description: `${selectedIntegration.name} has been connected successfully`
      });

      setIsConnectModalOpen(false);
      fetchIntegrations();
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.detail || 'Failed to connect integration',
        variant: 'destructive'
      });
    }
  };

  const handleDisconnect = async () => {
    try {
      await api.delete(`/integrations/${selectedIntegration.name}`);

      toast({
        title: 'Disconnected',
        description: `${selectedIntegration.name} has been disconnected`
      });

      setIsManageModalOpen(false);
      fetchIntegrations();
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.detail || 'Failed to disconnect integration',
        variant: 'destructive'
      });
    }
  };

  if (loading) {
    return <DashboardSkeleton />;
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
      <nav className="bg-white/80 backdrop-blur-lg border-b border-purple-200/50 sticky top-0 z-50 shadow-sm">
        <div className="px-8 py-4 flex items-center justify-between max-w-[95%] mx-auto">
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-2 cursor-pointer group" onClick={() => navigate('/dashboard')}>
              <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300 shadow-lg shadow-purple-500/30">
                <span className="text-white font-bold text-lg">B</span>
              </div>
              <span className="text-xl font-semibold bg-gradient-to-r from-gray-900 to-purple-600 bg-clip-text text-transparent">BotSmith</span>
            </div>
            <div className="flex items-center gap-6">
              <button onClick={() => navigate('/dashboard')} className="text-gray-600 hover:text-purple-600 transition-colors font-medium relative group">
                Chatbots
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-purple-600 to-pink-600 transform scale-x-0 group-hover:scale-x-100 transition-transform"></span>
              </button>
              <button onClick={() => navigate('/analytics')} className="text-gray-600 hover:text-purple-600 transition-colors font-medium relative group">
                Analytics
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-purple-600 to-pink-600 transform scale-x-0 group-hover:scale-x-100 transition-transform"></span>
              </button>
              <button onClick={() => navigate('/subscription')} className="text-gray-600 hover:text-purple-600 transition-colors font-medium relative group flex items-center gap-2">
                <CreditCard className="w-4 h-4" />
                Subscription
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-purple-600 to-pink-600 transform scale-x-0 group-hover:scale-x-100 transition-transform"></span>
              </button>
              <button className="text-purple-600 font-semibold relative group">
                Integrations
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-purple-600 to-pink-600 transform scale-x-100 transition-transform"></span>
              </button>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <UserProfileDropdown user={user} onLogout={handleLogout} />
          </div>
        </div>
      </nav>

      <div className="p-8 max-w-[95%] mx-auto relative z-10">
        <div className="mb-8 animate-fade-in-up">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-gray-900 via-purple-900 to-pink-900 bg-clip-text text-transparent">Integrations</h1>
          <p className="text-gray-600">Connect your favorite tools and services</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {integrations.map((integration, index) => {
            const Icon = integrationIcons[integration.name];
            const gradient = integrationGradients[integration.name];
            
            return (
              <div 
                key={index} 
                className="group bg-white/80 backdrop-blur-sm rounded-2xl border-2 border-purple-200/50 p-6 hover:border-purple-400 hover:shadow-2xl hover:shadow-purple-500/20 transition-all duration-500 transform hover:-translate-y-2 animate-fade-in-up"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className={`w-14 h-14 bg-gradient-to-br ${gradient} rounded-xl flex items-center justify-center shadow-lg transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300`}>
                    <Icon className="w-7 h-7 text-white" />
                  </div>
                  {integration.connected && (
                    <div className="flex items-center gap-1 bg-gradient-to-r from-green-500 to-emerald-600 text-white text-xs font-semibold px-3 py-1 rounded-full shadow-lg shadow-green-500/30 animate-bounce-subtle">
                      <Check className="w-3 h-3" />
                      Connected
                    </div>
                  )}
                </div>
                <h3 className="text-xl font-bold mb-2 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-pink-600 group-hover:bg-clip-text transition-all duration-300">{integration.name}</h3>
                <p className="text-sm text-gray-600 mb-4 line-clamp-2">{integration.description}</p>
                <Button
                  variant={integration.connected ? 'outline' : 'default'}
                  className={integration.connected ? 
                    'w-full border-2 border-purple-300 hover:bg-purple-50 hover:text-purple-600 transition-all duration-300' : 
                    'w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg shadow-purple-500/30 transform hover:scale-105 transition-all duration-300'
                  }
                  onClick={() => {
                    if (integration.connected) {
                      handleManage(integration);
                    } else {
                      handleConnect(integration);
                    }
                  }}
                >
                  {integration.connected ? 'Manage' : 'Connect'}
                </Button>
              </div>
            );
          })}
        </div>
      </div>

      {/* Connect Modal */}
      <Dialog open={isConnectModalOpen} onOpenChange={setIsConnectModalOpen}>
        <DialogContent className="bg-white/95 backdrop-blur-sm">
          <DialogHeader>
            <DialogTitle className="text-2xl bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Connect {selectedIntegration?.name}</DialogTitle>
            <DialogDescription>
              Enter your {selectedIntegration?.name} credentials to connect
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 py-4">
            <div>
              <Label htmlFor="apiKey" className="font-medium text-gray-700">API Key *</Label>
              <Input
                id="apiKey"
                placeholder="Enter your API key"
                value={connectionData.apiKey}
                onChange={(e) => setConnectionData({...connectionData, apiKey: e.target.value})}
                className="mt-2 border-2 border-purple-200 focus:border-purple-600 transition-colors"
              />
            </div>
            
            {selectedIntegration?.name === 'Slack' && (
              <div>
                <Label htmlFor="workspaceId" className="font-medium text-gray-700">Workspace ID</Label>
                <Input
                  id="workspaceId"
                  placeholder="Enter workspace ID"
                  value={connectionData.workspaceId}
                  onChange={(e) => setConnectionData({...connectionData, workspaceId: e.target.value})}
                  className="mt-2 border-2 border-purple-200 focus:border-purple-600 transition-colors"
                />
              </div>
            )}
            
            <div>
              <Label htmlFor="webhookUrl" className="font-medium text-gray-700">Webhook URL (Optional)</Label>
              <Input
                id="webhookUrl"
                placeholder="https://your-domain.com/webhook"
                value={connectionData.webhookUrl}
                onChange={(e) => setConnectionData({...connectionData, webhookUrl: e.target.value})}
                className="mt-2 border-2 border-purple-200 focus:border-purple-600 transition-colors"
              />
            </div>
          </div>
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsConnectModalOpen(false)} className="border-2 border-gray-300 hover:bg-gray-50">
              Cancel
            </Button>
            <Button 
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg shadow-purple-500/30 transform hover:scale-105 transition-all duration-300"
              onClick={handleConfirmConnect}
            >
              Connect
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Manage Modal */}
      <Dialog open={isManageModalOpen} onOpenChange={setIsManageModalOpen}>
        <DialogContent className="bg-white/95 backdrop-blur-sm">
          <DialogHeader>
            <DialogTitle className="text-2xl bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Manage {selectedIntegration?.name}</DialogTitle>
            <DialogDescription>
              Configure your {selectedIntegration?.name} integration
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 py-4">
            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border-2 border-green-300">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center shadow-lg shadow-green-500/30">
                  <Check className="w-5 h-5 text-white" />
                </div>
                <div>
                  <p className="font-semibold text-green-900">Connected</p>
                  <p className="text-sm text-green-700">Integration is active</p>
                </div>
              </div>
            </div>
            
            <div>
              <Label className="font-medium text-gray-700">API Key</Label>
              <Input
                value="••••••••••••••••"
                disabled
                className="mt-2 border-2 border-gray-200"
              />
            </div>
            
            <div>
              <Label className="font-medium text-gray-700">Status</Label>
              <div className="mt-2 flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-gray-600 font-medium">Active and syncing</span>
              </div>
            </div>
          </div>
          
          <DialogFooter className="gap-2">
            <Button variant="outline" onClick={() => setIsManageModalOpen(false)} className="border-2 border-gray-300 hover:bg-gray-50">
              Close
            </Button>
            <Button 
              variant="destructive"
              onClick={handleDisconnect}
              className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 shadow-lg shadow-red-500/30 transform hover:scale-105 transition-all duration-300"
            >
              Disconnect
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Footer */}
      <Footer variant="dashboard" />
    </div>
  );
};

export default Integrations;