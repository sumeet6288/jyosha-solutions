import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { LogOut, Check, X } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '../components/ui/dialog';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { useToast } from '../hooks/use-toast';

const Integrations = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [user, setUser] = useState(null);
  const [selectedIntegration, setSelectedIntegration] = useState(null);
  const [isConnectModalOpen, setIsConnectModalOpen] = useState(false);
  const [isManageModalOpen, setIsManageModalOpen] = useState(false);
  const [connectionData, setConnectionData] = useState({
    apiKey: '',
    webhookUrl: '',
    workspaceId: ''
  });

  const [integrations, setIntegrations] = useState([
    { id: 1, name: 'Stripe', description: 'Accept payments directly in chat', connected: false },
    { id: 2, name: 'Calendly', description: 'Schedule appointments seamlessly', connected: false },
    { id: 3, name: 'Slack', description: 'Deploy chatbot to Slack workspace', connected: false },
    { id: 4, name: 'Zendesk', description: 'Sync conversations to Zendesk', connected: false },
    { id: 5, name: 'WhatsApp', description: 'Deploy on WhatsApp Business', connected: false },
    { id: 6, name: 'Salesforce', description: 'Integrate with Salesforce CRM', connected: false },
  ]);

  useEffect(() => {
    const userData = localStorage.getItem('chatbase_user');
    if (!userData) {
      navigate('/signin');
      return;
    }
    setUser(JSON.parse(userData));
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('chatbase_user');
    navigate('/');
  };

  const handleConnect = (integration) => {
    setSelectedIntegration(integration);
    setIsConnectModalOpen(true);
    setConnectionData({ apiKey: '', webhookUrl: '', workspaceId: '' });
  };

  const handleManage = (integration) => {
    setSelectedIntegration(integration);
    setIsManageModalOpen(true);
  };

  const handleConfirmConnect = () => {
    if (!connectionData.apiKey) {
      toast({
        title: 'Error',
        description: 'API Key is required',
        variant: 'destructive'
      });
      return;
    }

    setIntegrations(integrations.map(int => 
      int.id === selectedIntegration.id 
        ? { ...int, connected: true }
        : int
    ));

    toast({
      title: 'Connected!',
      description: `${selectedIntegration.name} has been connected successfully`
    });

    setIsConnectModalOpen(false);
  };

  const handleDisconnect = () => {
    setIntegrations(integrations.map(int => 
      int.id === selectedIntegration.id 
        ? { ...int, connected: false }
        : int
    ));

    toast({
      title: 'Disconnected',
      description: `${selectedIntegration.name} has been disconnected`
    });

    setIsManageModalOpen(false);
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
              <button onClick={() => navigate('/analytics')} className="text-gray-600 hover:text-black transition-colors">Analytics</button>
              <button className="text-black font-medium">Integrations</button>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium">{user?.name}</p>
              <p className="text-xs text-gray-500">{user?.email}</p>
            </div>
            <Button variant="ghost" size="icon" onClick={handleLogout}>
              <LogOut className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </nav>

      <div className="p-6 max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">Integrations</h1>
        <p className="text-gray-600 mb-8">Connect your favorite tools and services</p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {integrations.map((integration, index) => (
            <div key={index} className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg transition-all">
              <div className="flex items-start justify-between mb-4">
                <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                  <span className="text-2xl font-bold">{integration.name[0]}</span>
                </div>
                {integration.connected && (
                  <div className="flex items-center gap-1 text-green-600 text-sm">
                    <Check className="w-4 h-4" />
                    Connected
                  </div>
                )}
              </div>
              <h3 className="text-lg font-semibold mb-2">{integration.name}</h3>
              <p className="text-sm text-gray-600 mb-4">{integration.description}</p>
              <Button
                variant={integration.connected ? 'outline' : 'default'}
                className={integration.connected ? '' : 'bg-black hover:bg-gray-800 text-white'}
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
          ))}
        </div>
      </div>

      {/* Connect Modal */}
      <Dialog open={isConnectModalOpen} onOpenChange={setIsConnectModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Connect {selectedIntegration?.name}</DialogTitle>
            <DialogDescription>
              Enter your {selectedIntegration?.name} credentials to connect
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 py-4">
            <div>
              <Label htmlFor="apiKey">API Key *</Label>
              <Input
                id="apiKey"
                placeholder="Enter your API key"
                value={connectionData.apiKey}
                onChange={(e) => setConnectionData({...connectionData, apiKey: e.target.value})}
                className="mt-2"
              />
            </div>
            
            {selectedIntegration?.name === 'Slack' && (
              <div>
                <Label htmlFor="workspaceId">Workspace ID</Label>
                <Input
                  id="workspaceId"
                  placeholder="Enter workspace ID"
                  value={connectionData.workspaceId}
                  onChange={(e) => setConnectionData({...connectionData, workspaceId: e.target.value})}
                  className="mt-2"
                />
              </div>
            )}
            
            <div>
              <Label htmlFor="webhookUrl">Webhook URL (Optional)</Label>
              <Input
                id="webhookUrl"
                placeholder="https://your-domain.com/webhook"
                value={connectionData.webhookUrl}
                onChange={(e) => setConnectionData({...connectionData, webhookUrl: e.target.value})}
                className="mt-2"
              />
            </div>
          </div>
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsConnectModalOpen(false)}>
              Cancel
            </Button>
            <Button 
              className="bg-black hover:bg-gray-800 text-white"
              onClick={handleConfirmConnect}
            >
              Connect
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Manage Modal */}
      <Dialog open={isManageModalOpen} onOpenChange={setIsManageModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Manage {selectedIntegration?.name}</DialogTitle>
            <DialogDescription>
              Configure your {selectedIntegration?.name} integration
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 py-4">
            <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg border border-green-200">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                  <Check className="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <p className="font-medium text-green-900">Connected</p>
                  <p className="text-sm text-green-700">Integration is active</p>
                </div>
              </div>
            </div>
            
            <div>
              <Label>API Key</Label>
              <Input
                value="••••••••••••••••"
                disabled
                className="mt-2"
              />
            </div>
            
            <div>
              <Label>Status</Label>
              <div className="mt-2 flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-600">Active and syncing</span>
              </div>
            </div>
          </div>
          
          <DialogFooter className="gap-2">
            <Button variant="outline" onClick={() => setIsManageModalOpen(false)}>
              Close
            </Button>
            <Button 
              variant="destructive"
              onClick={handleDisconnect}
            >
              Disconnect
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Integrations;