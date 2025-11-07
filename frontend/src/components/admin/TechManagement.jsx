import React, { useState, useEffect } from 'react';
import { Key, Webhook, FileText, AlertTriangle, Copy, Eye, EyeOff, Plus, Trash2, RefreshCw, Download, Check, X } from 'lucide-react';
import { Button } from '../ui/button';
import axios from 'axios';

const TechManagement = ({ backendUrl }) => {
  const [apiKeys, setApiKeys] = useState([]);
  const [webhooks, setWebhooks] = useState([]);
  const [systemLogs, setSystemLogs] = useState([]);
  const [errors, setErrors] = useState([]);
  const [showNewKeyModal, setShowNewKeyModal] = useState(false);
  const [showNewWebhookModal, setShowNewWebhookModal] = useState(false);
  const [visibleKeys, setVisibleKeys] = useState({});
  const [loading, setLoading] = useState(true);
  const [newKeyName, setNewKeyName] = useState('');
  const [newKeyDescription, setNewKeyDescription] = useState('');
  const [newKeyExpiry, setNewKeyExpiry] = useState('');
  const [newWebhookUrl, setNewWebhookUrl] = useState('');
  const [newWebhookEvents, setNewWebhookEvents] = useState([]);
  const [newWebhookDescription, setNewWebhookDescription] = useState('');
  const [techStats, setTechStats] = useState(null);
  const [copiedKey, setCopiedKey] = useState(null);
  const [newlyCreatedKey, setNewlyCreatedKey] = useState(null);

  const availableEvents = [
    'user.created', 'user.updated', 'user.deleted',
    'chatbot.created', 'chatbot.updated', 'chatbot.deleted',
    'conversation.started', 'conversation.completed',
    'message.sent', 'message.received',
    'source.uploaded', 'source.processed',
    'error.occurred'
  ];

  useEffect(() => {
    fetchAllData();
  }, [backendUrl]);

  const fetchAllData = async () => {
    setLoading(true);
    try {
      await Promise.all([
        fetchApiKeys(),
        fetchWebhooks(),
        fetchSystemLogs(),
        fetchErrors(),
        fetchTechStats()
      ]);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchApiKeys = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/tech/api-keys`);
      setApiKeys(response.data);
    } catch (error) {
      console.error('Error fetching API keys:', error);
    }
  };

  const fetchWebhooks = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/tech/webhooks`);
      setWebhooks(response.data);
    } catch (error) {
      console.error('Error fetching webhooks:', error);
    }
  };

  const fetchSystemLogs = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/tech/system-logs?limit=50`);
      setSystemLogs(response.data);
    } catch (error) {
      console.error('Error fetching system logs:', error);
    }
  };

  const fetchErrors = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/tech/errors?resolved=false&limit=50`);
      setErrors(response.data);
    } catch (error) {
      console.error('Error fetching errors:', error);
    }
  };

  const fetchTechStats = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/tech/tech-stats`);
      setTechStats(response.data);
    } catch (error) {
      console.error('Error fetching tech stats:', error);
    }
  };

  const toggleKeyVisibility = (keyId) => {
    setVisibleKeys(prev => ({
      ...prev,
      [keyId]: !prev[keyId]
    }));
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    // TODO: Show toast notification
  };

  const maskApiKey = (key) => {
    const visible = key.substring(0, 12);
    const masked = '•'.repeat(20);
    return visible + masked;
  };

  const getLevelColor = (level) => {
    switch(level) {
      case 'error': return 'text-red-600 bg-red-50';
      case 'warning': return 'text-yellow-600 bg-yellow-50';
      case 'info': return 'text-blue-600 bg-blue-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="space-y-8">
      {/* API Keys Section */}
      <div className="bg-white rounded-xl border border-gray-200 p-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Key className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">API Keys</h2>
              <p className="text-sm text-gray-600">Manage your API keys and access tokens</p>
            </div>
          </div>
          <Button 
            onClick={() => setShowNewKeyModal(true)}
            className="bg-gradient-to-r from-blue-600 to-blue-700 text-white"
          >
            <Plus className="w-4 h-4 mr-2" />
            Generate New Key
          </Button>
        </div>

        <div className="space-y-4">
          {apiKeys.map((apiKey) => (
            <div key={apiKey.id} className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="font-semibold text-lg">{apiKey.name}</h3>
                    <span className="px-2 py-1 bg-green-100 text-green-700 rounded text-xs font-medium">
                      Active
                    </span>
                  </div>
                  <div className="flex items-center gap-2 mb-2">
                    <code className="px-3 py-1 bg-gray-100 rounded font-mono text-sm">
                      {visibleKeys[apiKey.id] ? apiKey.key : maskApiKey(apiKey.key)}
                    </code>
                    <button
                      onClick={() => toggleKeyVisibility(apiKey.id)}
                      className="p-1 hover:bg-gray-100 rounded"
                    >
                      {visibleKeys[apiKey.id] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                    <button
                      onClick={() => copyToClipboard(apiKey.key)}
                      className="p-1 hover:bg-gray-100 rounded"
                    >
                      <Copy className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="flex gap-4 text-sm text-gray-600">
                    <span>Created: {new Date(apiKey.created_at).toLocaleDateString()}</span>
                    <span>•</span>
                    <span>Last used: {new Date(apiKey.last_used).toLocaleDateString()}</span>
                    <span>•</span>
                    <span>Usage: {apiKey.usage_count.toLocaleString()} calls</span>
                  </div>
                </div>
                <button className="p-2 hover:bg-red-50 rounded text-red-600">
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Webhooks Section */}
      <div className="bg-white rounded-xl border border-gray-200 p-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <Webhook className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Webhooks</h2>
              <p className="text-sm text-gray-600">Configure webhook endpoints for real-time events</p>
            </div>
          </div>
          <Button 
            onClick={() => setShowNewWebhookModal(true)}
            className="bg-gradient-to-r from-purple-600 to-purple-700 text-white"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Webhook
          </Button>
        </div>

        <div className="space-y-4">
          {webhooks.map((webhook) => (
            <div key={webhook.id} className="p-4 border border-gray-200 rounded-lg hover:border-purple-300 transition-colors">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <h3 className="font-semibold">{webhook.url}</h3>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    webhook.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                  }`}>
                    {webhook.status}
                  </span>
                </div>
                <div className="flex gap-2">
                  <button className="p-2 hover:bg-gray-100 rounded">
                    <RefreshCw className="w-4 h-4" />
                  </button>
                  <button className="p-2 hover:bg-red-50 rounded text-red-600">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
              <div className="flex items-center gap-4 text-sm text-gray-600">
                <span>Events: {webhook.events.join(', ')}</span>
                <span>•</span>
                <span className="text-green-600 font-medium">Success Rate: {webhook.success_rate}%</span>
                <span>•</span>
                <span>Created: {new Date(webhook.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* System Logs Section */}
      <div className="bg-white rounded-xl border border-gray-200 p-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <FileText className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">System Logs</h2>
              <p className="text-sm text-gray-600">View real-time system activity and events</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline">
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </Button>
            <Button variant="outline">
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
          </div>
        </div>

        <div className="space-y-2 max-h-96 overflow-y-auto">
          {systemLogs.map((log) => (
            <div key={log.id} className="p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <div className="flex items-start gap-3">
                <span className={`px-2 py-1 rounded text-xs font-medium ${getLevelColor(log.level)}`}>
                  {log.level.toUpperCase()}
                </span>
                <div className="flex-1">
                  <p className="text-sm font-medium">{log.message}</p>
                  {log.details && <p className="text-xs text-gray-600 mt-1">{log.details}</p>}
                  {log.user && <p className="text-xs text-gray-500 mt-1">User: {log.user}</p>}
                </div>
                <span className="text-xs text-gray-500">
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Error Tracking Section */}
      <div className="bg-white rounded-xl border border-gray-200 p-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-red-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Error Tracking</h2>
              <p className="text-sm text-gray-600">Monitor and debug application errors</p>
            </div>
          </div>
          <Button variant="outline" className="text-red-600 border-red-600 hover:bg-red-50">
            Clear All Errors
          </Button>
        </div>

        <div className="space-y-4">
          {errors.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <AlertTriangle className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p>No errors tracked</p>
            </div>
          ) : (
            errors.map((error) => (
              <div key={error.id} className="p-4 border border-red-200 bg-red-50 rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="px-2 py-1 bg-red-600 text-white rounded text-xs font-medium">
                        {error.type}
                      </span>
                      <span className="px-2 py-1 bg-red-200 text-red-800 rounded text-xs font-medium">
                        Count: {error.count}
                      </span>
                    </div>
                    <h3 className="font-semibold text-red-900">{error.message}</h3>
                  </div>
                  <span className="text-xs text-gray-600">
                    {new Date(error.timestamp).toLocaleString()}
                  </span>
                </div>
                <details className="mt-2">
                  <summary className="cursor-pointer text-sm text-red-700 font-medium hover:text-red-800">
                    View Stack Trace
                  </summary>
                  <pre className="mt-2 p-3 bg-white rounded text-xs overflow-x-auto border border-red-200">
                    {error.stack}
                  </pre>
                </details>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default TechManagement;
