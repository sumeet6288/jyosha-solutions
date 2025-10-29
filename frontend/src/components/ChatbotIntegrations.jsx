import React, { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { useToast } from '../hooks/use-toast';
import WhatsAppQRModal from './WhatsAppQRModal';
import { 
  MessageCircle, 
  Send, 
  CheckCircle, 
  Copy, 
  ExternalLink,
  AlertCircle,
  Zap,
  Globe,
  Phone
} from 'lucide-react';

const ChatbotIntegrations = ({ chatbot }) => {
  const { toast } = useToast();
  const [activeIntegration, setActiveIntegration] = useState(null);
  const [showWhatsAppQR, setShowWhatsAppQR] = useState(false);

  const integrations = [
    {
      id: 'whatsapp',
      name: 'WhatsApp',
      description: 'Connect your chatbot to WhatsApp Business API',
      icon: <MessageCircle className="w-6 h-6" />,
      gradient: 'from-green-500 to-green-600',
      status: 'available',
      setupRequired: ['Phone Number', 'API Key', 'Webhook URL'],
      instructions: 'Connect your WhatsApp Business API account to enable chatbot responses on WhatsApp.'
    },
    {
      id: 'slack',
      name: 'Slack',
      description: 'Deploy chatbot to your Slack workspace',
      icon: <Send className="w-6 h-6" />,
      gradient: 'from-purple-500 to-purple-600',
      status: 'available',
      setupRequired: ['Workspace URL', 'Bot Token', 'Signing Secret'],
      instructions: 'Add the chatbot to your Slack workspace to assist your team members.'
    },
    {
      id: 'telegram',
      name: 'Telegram',
      description: 'Create a Telegram bot for your chatbot',
      icon: <Send className="w-6 h-6" />,
      gradient: 'from-blue-500 to-blue-600',
      status: 'available',
      setupRequired: ['Bot Token', 'Username'],
      instructions: 'Create a Telegram bot using BotFather and connect it to your chatbot.'
    },
    {
      id: 'discord',
      name: 'Discord',
      description: 'Add chatbot to your Discord server',
      icon: <MessageCircle className="w-6 h-6" />,
      gradient: 'from-indigo-500 to-indigo-600',
      status: 'available',
      setupRequired: ['Bot Token', 'Client ID', 'Server ID'],
      instructions: 'Deploy your chatbot to Discord servers for community support.'
    },
    {
      id: 'webchat',
      name: 'Web Chat Widget',
      description: 'Embed chat widget on any website',
      icon: <Globe className="w-6 h-6" />,
      gradient: 'from-cyan-500 to-cyan-600',
      status: 'active',
      setupRequired: ['Domain', 'Widget Code'],
      instructions: 'Already configured! Your widget is ready to embed.'
    },
    {
      id: 'api',
      name: 'REST API',
      description: 'Integrate via REST API for custom applications',
      icon: <Zap className="w-6 h-6" />,
      gradient: 'from-orange-500 to-orange-600',
      status: 'available',
      setupRequired: ['API Key', 'Endpoint URL'],
      instructions: 'Use our REST API to integrate the chatbot into your custom applications.'
    },
    {
      id: 'twilio',
      name: 'Twilio SMS',
      description: 'Enable chatbot responses via SMS',
      icon: <Phone className="w-6 h-6" />,
      gradient: 'from-red-500 to-red-600',
      status: 'available',
      setupRequired: ['Account SID', 'Auth Token', 'Phone Number'],
      instructions: 'Connect Twilio to enable SMS-based chatbot conversations.'
    },
    {
      id: 'messenger',
      name: 'Facebook Messenger',
      description: 'Connect to Facebook Messenger',
      icon: <MessageCircle className="w-6 h-6" />,
      gradient: 'from-blue-600 to-blue-700',
      status: 'coming_soon',
      setupRequired: ['Page Access Token', 'App Secret', 'Verify Token'],
      instructions: 'Coming soon! Connect your Facebook page to enable Messenger chatbot.'
    }
  ];

  const copyWebhookURL = () => {
    const webhookURL = `${window.location.origin}/api/webhook/${chatbot.id}`;
    navigator.clipboard.writeText(webhookURL);
    toast({
      title: 'Copied!',
      description: 'Webhook URL copied to clipboard'
    });
  };

  const copyAPIKey = () => {
    const apiKey = chatbot.id; // In production, this would be a separate API key
    navigator.clipboard.writeText(apiKey);
    toast({
      title: 'Copied!',
      description: 'API key copied to clipboard'
    });
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'active':
        return (
          <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold flex items-center gap-1">
            <CheckCircle className="w-3 h-3" />
            Active
          </span>
        );
      case 'available':
        return (
          <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-semibold">
            Available
          </span>
        );
      case 'coming_soon':
        return (
          <span className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-xs font-semibold">
            Coming Soon
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold mb-2 bg-gradient-to-r from-gray-900 to-purple-600 bg-clip-text text-transparent">
          Platform Integrations
        </h2>
        <p className="text-gray-600">
          Connect your chatbot to various platforms and channels
        </p>
      </div>

      {/* Global Webhook & API Info */}
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-200 rounded-xl p-6">
        <div className="flex items-start gap-3 mb-4">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg flex items-center justify-center flex-shrink-0">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 mb-1">Integration Credentials</h3>
            <p className="text-sm text-gray-600">Use these credentials to connect your chatbot to external platforms</p>
          </div>
        </div>

        <div className="space-y-3">
          <div>
            <label className="text-xs font-semibold text-gray-700 mb-1 block">Webhook URL</label>
            <div className="flex gap-2">
              <Input
                value={`${window.location.origin}/api/webhook/${chatbot.id}`}
                readOnly
                className="font-mono text-xs bg-white"
              />
              <Button
                onClick={copyWebhookURL}
                variant="outline"
                size="sm"
                className="flex-shrink-0"
              >
                <Copy className="w-4 h-4" />
              </Button>
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-gray-700 mb-1 block">Chatbot ID (API Key)</label>
            <div className="flex gap-2">
              <Input
                value={chatbot.id}
                readOnly
                className="font-mono text-xs bg-white"
              />
              <Button
                onClick={copyAPIKey}
                variant="outline"
                size="sm"
                className="flex-shrink-0"
              >
                <Copy className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Integrations Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {integrations.map((integration) => (
          <Card
            key={integration.id}
            className={`p-6 hover:shadow-xl transition-all duration-300 border-2 ${
              integration.status === 'active' 
                ? 'border-green-200 bg-green-50/30' 
                : integration.status === 'coming_soon'
                ? 'border-gray-200 opacity-75'
                : 'border-purple-200/50 hover:border-purple-400'
            }`}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-start gap-3">
                <div className={`w-12 h-12 bg-gradient-to-br ${integration.gradient} rounded-xl flex items-center justify-center text-white shadow-lg transform hover:scale-110 transition-transform`}>
                  {integration.icon}
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-1">
                    {integration.name}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {integration.description}
                  </p>
                </div>
              </div>
              {getStatusBadge(integration.status)}
            </div>

            <div className="space-y-3">
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs font-semibold text-gray-700 mb-2">Setup Requirements:</p>
                <ul className="space-y-1">
                  {integration.setupRequired.map((req, idx) => (
                    <li key={idx} className="text-xs text-gray-600 flex items-center gap-2">
                      <div className="w-1.5 h-1.5 bg-purple-400 rounded-full"></div>
                      {req}
                    </li>
                  ))}
                </ul>
              </div>

              <Button
                className={`w-full ${
                  integration.status === 'active'
                    ? 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800'
                    : integration.status === 'coming_soon'
                    ? 'bg-gray-300 cursor-not-allowed'
                    : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700'
                } text-white`}
                onClick={() => {
                  if (integration.status === 'coming_soon') return;
                  setActiveIntegration(integration);
                  toast({
                    title: integration.status === 'active' ? 'Already Active' : 'Setup Guide',
                    description: integration.instructions
                  });
                }}
                disabled={integration.status === 'coming_soon'}
              >
                {integration.status === 'active' ? (
                  <>
                    <CheckCircle className="w-4 h-4 mr-2" />
                    Connected
                  </>
                ) : integration.status === 'coming_soon' ? (
                  'Coming Soon'
                ) : (
                  <>
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Setup Integration
                  </>
                )}
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* API Documentation Link */}
      <div className="bg-white border-2 border-purple-200 rounded-xl p-6">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-lg flex items-center justify-center flex-shrink-0">
            <AlertCircle className="w-5 h-5 text-white" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 mb-2">Need Help with Integration?</h3>
            <p className="text-sm text-gray-600 mb-3">
              Check out our comprehensive API documentation and integration guides to get started quickly.
            </p>
            <Button
              variant="outline"
              className="border-2 border-purple-600 text-purple-600 hover:bg-purple-50"
              onClick={() => {
                toast({
                  title: 'Documentation',
                  description: 'API documentation is available in your dashboard'
                });
              }}
            >
              <ExternalLink className="w-4 h-4 mr-2" />
              View API Documentation
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatbotIntegrations;
