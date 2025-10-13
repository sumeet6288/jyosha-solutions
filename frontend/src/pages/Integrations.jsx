import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { LogOut, Check } from 'lucide-react';

const Integrations = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

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

  const integrations = [
    { name: 'Stripe', description: 'Accept payments directly in chat', connected: false },
    { name: 'Calendly', description: 'Schedule appointments seamlessly', connected: true },
    { name: 'Slack', description: 'Deploy chatbot to Slack workspace', connected: false },
    { name: 'Zendesk', description: 'Sync conversations to Zendesk', connected: false },
    { name: 'WhatsApp', description: 'Deploy on WhatsApp Business', connected: false },
    { name: 'Salesforce', description: 'Integrate with Salesforce CRM', connected: false },
  ];

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
                  // Integration logic would go here
                }}
              >
                {integration.connected ? 'Manage' : 'Connect'}
              </Button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Integrations;