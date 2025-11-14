import React, { useState, useEffect } from 'react';
import { DollarSign, Save, RefreshCw, Key, Store, Webhook, CheckCircle, XCircle, Eye, EyeOff, Copy, Check, AlertTriangle, Zap } from 'lucide-react';
import { Button } from '../ui/button';

const PaymentGatewaySettings = ({ backendUrl }) => {
  const [settings, setSettings] = useState({
    lemonsqueezy: {
      enabled: false,
      test_mode: true,
      api_key: '',
      store_id: '',
      webhook_url: '',
      webhook_secret: '',
      plans: {
        free: '',
        starter: '',
        professional: '',
        enterprise: ''
      }
    }
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showApiKey, setShowApiKey] = useState(false);
  const [showWebhookSecret, setShowWebhookSecret] = useState(false);
  const [testingConnection, setTestingConnection] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState(null);
  const [copied, setCopied] = useState('');
  const [fetchingProducts, setFetchingProducts] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${backendUrl}/api/admin/payment-settings`);
      if (response.ok) {
        const data = await response.json();
        setSettings(data || settings);
      }
    } catch (error) {
      console.error('Error fetching payment settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const saveSettings = async () => {
    try {
      setSaving(true);
      const response = await fetch(`${backendUrl}/api/admin/payment-settings`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
      });
      
      if (response.ok) {
        const data = await response.json();
        alert('✅ Payment gateway settings saved successfully!');
        setConnectionStatus(null);
      } else {
        const error = await response.json();
        alert(`❌ Failed to save settings: ${error.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error saving payment settings:', error);
      alert('❌ Failed to save payment settings');
    } finally {
      setSaving(false);
    }
  };

  const testConnection = async () => {
    try {
      setTestingConnection(true);
      setConnectionStatus(null);
      
      const response = await fetch(`${backendUrl}/api/admin/payment-settings/test`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          api_key: settings.lemonsqueezy.api_key,
          store_id: settings.lemonsqueezy.store_id,
          test_mode: settings.lemonsqueezy.test_mode
        })
      });
      
      const data = await response.json();
      
      if (response.ok && data.success) {
        setConnectionStatus({ 
          success: true, 
          message: data.message || 'Connection successful!',
          store_name: data.store_name
        });
      } else {
        setConnectionStatus({ 
          success: false, 
          message: data.detail || data.message || 'Connection failed. Please check your credentials.'
        });
      }
    } catch (error) {
      console.error('Error testing connection:', error);
      setConnectionStatus({ 
        success: false, 
        message: 'Failed to test connection. Please check your network.'
      });
    } finally {
      setTestingConnection(false);
    }
  };

  const fetchProducts = async () => {
    try {
      setFetchingProducts(true);
      
      const response = await fetch(`${backendUrl}/api/admin/payment-settings/fetch-products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          api_key: settings.lemonsqueezy.api_key,
          store_id: settings.lemonsqueezy.store_id,
          test_mode: settings.lemonsqueezy.test_mode
        })
      });
      
      const data = await response.json();
      
      if (response.ok && data.success) {
        alert(`✅ Found ${data.products.length} products!\n\nProducts will be displayed for you to map to plans.`);
        console.log('Products:', data.products);
      } else {
        alert(`❌ Failed to fetch products: ${data.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error fetching products:', error);
      alert('❌ Failed to fetch products. Please check your network.');
    } finally {
      setFetchingProducts(false);
    }
  };

  const copyToClipboard = (text, field) => {
    navigator.clipboard.writeText(text);
    setCopied(field);
    setTimeout(() => setCopied(''), 2000);
  };

  const generateWebhookUrl = () => {
    const baseUrl = backendUrl || window.location.origin;
    return `${baseUrl}/api/webhooks/lemonsqueezy`;
  };

  const updatePlanId = (planType, value) => {
    setSettings({
      ...settings,
      lemonsqueezy: {
        ...settings.lemonsqueezy,
        plans: {
          ...settings.lemonsqueezy.plans,
          [planType]: value
        }
      }
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  const webhookUrl = generateWebhookUrl();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
              <DollarSign className="w-8 h-8 text-purple-600" />
              Payment Gateway Settings
            </h2>
            <p className="text-gray-600">Configure payment gateways for subscription management</p>
          </div>
          <div className="flex gap-3">
            <Button onClick={fetchSettings} variant="outline">
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </Button>
            <Button onClick={saveSettings} disabled={saving} className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white">
              {saving ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4 mr-2" />
                  Save Settings
                </>
              )}
            </Button>
          </div>
        </div>
      </div>

      {/* LemonSqueezy Settings */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex flex-col gap-4 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold flex items-center gap-2">
                <Zap className="w-6 h-6 text-yellow-500" />
                LemonSqueezy Integration
              </h3>
              <p className="text-sm text-gray-600 mt-1">Manage subscription payments with LemonSqueezy</p>
            </div>
            <div className="flex items-center gap-3">
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.lemonsqueezy.enabled}
                  onChange={(e) => setSettings({
                    ...settings,
                    lemonsqueezy: { ...settings.lemonsqueezy, enabled: e.target.checked }
                  })}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-gradient-to-r peer-checked:from-purple-600 peer-checked:to-pink-600"></div>
              </label>
              <span className="text-sm font-medium text-gray-700">
                {settings.lemonsqueezy.enabled ? 'Enabled' : 'Disabled'}
              </span>
            </div>
          </div>

          {/* Test Mode Toggle */}
          <div className="flex items-center justify-between bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-blue-600" />
              <div>
                <p className="text-sm font-semibold text-blue-900">Test Mode</p>
                <p className="text-xs text-blue-700">Use test API keys for development and testing</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.lemonsqueezy.test_mode}
                  onChange={(e) => setSettings({
                    ...settings,
                    lemonsqueezy: { ...settings.lemonsqueezy, test_mode: e.target.checked }
                  })}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-gradient-to-r peer-checked:from-blue-600 peer-checked:to-cyan-600"></div>
              </label>
              <span className="text-sm font-medium text-blue-900">
                {settings.lemonsqueezy.test_mode ? 'Test Mode' : 'Live Mode'}
              </span>
            </div>
          </div>
        </div>

        {/* Connection Status */}
        {connectionStatus && (
          <div className={`mb-6 p-4 rounded-lg flex items-center gap-3 ${
            connectionStatus.success 
              ? 'bg-green-50 border border-green-200' 
              : 'bg-red-50 border border-red-200'
          }`}>
            {connectionStatus.success ? (
              <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
            ) : (
              <XCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
            )}
            <div className="flex-1">
              <p className={`font-semibold ${connectionStatus.success ? 'text-green-800' : 'text-red-800'}`}>
                {connectionStatus.success ? 'Connection Successful!' : 'Connection Failed'}
              </p>
              <p className={`text-sm ${connectionStatus.success ? 'text-green-700' : 'text-red-700'}`}>
                {connectionStatus.message}
              </p>
              {connectionStatus.store_name && (
                <p className="text-sm text-green-700 mt-1">
                  Store: <span className="font-semibold">{connectionStatus.store_name}</span>
                </p>
              )}
            </div>
          </div>
        )}

        {/* Test Mode Warning Banner */}
        {settings.lemonsqueezy.test_mode && settings.lemonsqueezy.enabled && (
          <div className="mb-6 p-4 bg-yellow-50 border-2 border-yellow-300 rounded-lg flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-yellow-900 mb-1">⚠️ Test Mode Active</p>
              <p className="text-sm text-yellow-800">
                You are currently using <span className="font-semibold">test API keys</span>. No real payments will be processed. 
                Make sure to switch to live mode and update your API keys before going to production.
              </p>
            </div>
          </div>
        )}

        <div className="space-y-6">
          {/* API Key */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
              <Key className="w-4 h-4 text-purple-600" />
              API Key
              <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <input
                type={showApiKey ? 'text' : 'password'}
                value={settings.lemonsqueezy.api_key}
                onChange={(e) => setSettings({
                  ...settings,
                  lemonsqueezy: { ...settings.lemonsqueezy, api_key: e.target.value }
                })}
                placeholder="Enter your LemonSqueezy API key"
                className="w-full px-4 py-3 pr-24 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
              <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-1">
                <button
                  type="button"
                  onClick={() => setShowApiKey(!showApiKey)}
                  className="p-2 hover:bg-gray-100 rounded-md transition-colors"
                >
                  {showApiKey ? (
                    <EyeOff className="w-4 h-4 text-gray-500" />
                  ) : (
                    <Eye className="w-4 h-4 text-gray-500" />
                  )}
                </button>
                {settings.lemonsqueezy.api_key && (
                  <button
                    type="button"
                    onClick={() => copyToClipboard(settings.lemonsqueezy.api_key, 'api_key')}
                    className="p-2 hover:bg-gray-100 rounded-md transition-colors"
                  >
                    {copied === 'api_key' ? (
                      <Check className="w-4 h-4 text-green-500" />
                    ) : (
                      <Copy className="w-4 h-4 text-gray-500" />
                    )}
                  </button>
                )}
              </div>
            </div>
            <div className="flex items-start gap-2">
              {settings.lemonsqueezy.test_mode && (
                <div className="flex items-center gap-1 px-2 py-1 bg-blue-100 border border-blue-300 rounded text-xs text-blue-800 font-semibold">
                  <AlertTriangle className="w-3 h-3" />
                  Test Key
                </div>
              )}
              <p className="text-xs text-gray-500">
                Get your {settings.lemonsqueezy.test_mode ? 'test' : 'live'} API key from: <a href="https://app.lemonsqueezy.com/settings/api" target="_blank" rel="noopener noreferrer" className="text-purple-600 hover:underline">LemonSqueezy Settings → API</a>
              </p>
            </div>
          </div>

          {/* Store ID */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
              <Store className="w-4 h-4 text-purple-600" />
              Store ID
              <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={settings.lemonsqueezy.store_id}
              onChange={(e) => setSettings({
                ...settings,
                lemonsqueezy: { ...settings.lemonsqueezy, store_id: e.target.value }
              })}
              placeholder="Enter your LemonSqueezy Store ID"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
            <p className="text-xs text-gray-500">
              Find your Store ID in: <a href="https://app.lemonsqueezy.com/settings/stores" target="_blank" rel="noopener noreferrer" className="text-purple-600 hover:underline">LemonSqueezy Settings → Stores</a>
            </p>
          </div>

          {/* Test Connection Button */}
          <div>
            <Button 
              onClick={testConnection} 
              disabled={!settings.lemonsqueezy.api_key || !settings.lemonsqueezy.store_id || testingConnection}
              variant="outline"
              className="w-full"
            >
              {testingConnection ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-purple-600 mr-2"></div>
                  Testing Connection...
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4 mr-2" />
                  Test Connection
                </>
              )}
            </Button>
          </div>

          {/* Webhook URL */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
              <Webhook className="w-4 h-4 text-purple-600" />
              Webhook URL
            </label>
            <div className="relative">
              <input
                type="text"
                value={webhookUrl}
                readOnly
                className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg bg-gray-50 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => copyToClipboard(webhookUrl, 'webhook_url')}
                className="absolute right-2 top-1/2 -translate-y-1/2 p-2 hover:bg-gray-200 rounded-md transition-colors"
              >
                {copied === 'webhook_url' ? (
                  <Check className="w-4 h-4 text-green-500" />
                ) : (
                  <Copy className="w-4 h-4 text-gray-500" />
                )}
              </button>
            </div>
            <div className="flex items-start gap-2 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <AlertTriangle className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" />
              <div className="text-xs text-blue-800">
                <p className="font-semibold mb-1">Configure this webhook in LemonSqueezy:</p>
                <ol className="list-decimal list-inside space-y-1">
                  <li>Go to <a href="https://app.lemonsqueezy.com/settings/webhooks" target="_blank" rel="noopener noreferrer" className="underline">LemonSqueezy Webhooks</a></li>
                  <li>Click "+" to create a new webhook</li>
                  <li>Paste the URL above</li>
                  <li>Select events: order_created, subscription_created, subscription_updated, subscription_cancelled</li>
                  <li>Copy the signing secret and paste below</li>
                </ol>
              </div>
            </div>
          </div>

          {/* Webhook Secret */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
              <Key className="w-4 h-4 text-purple-600" />
              Webhook Signing Secret
            </label>
            <div className="relative">
              <input
                type={showWebhookSecret ? 'text' : 'password'}
                value={settings.lemonsqueezy.webhook_secret}
                onChange={(e) => setSettings({
                  ...settings,
                  lemonsqueezy: { ...settings.lemonsqueezy, webhook_secret: e.target.value }
                })}
                placeholder="Enter webhook signing secret from LemonSqueezy"
                className="w-full px-4 py-3 pr-24 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
              <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-1">
                <button
                  type="button"
                  onClick={() => setShowWebhookSecret(!showWebhookSecret)}
                  className="p-2 hover:bg-gray-100 rounded-md transition-colors"
                >
                  {showWebhookSecret ? (
                    <EyeOff className="w-4 h-4 text-gray-500" />
                  ) : (
                    <Eye className="w-4 h-4 text-gray-500" />
                  )}
                </button>
              </div>
            </div>
            <p className="text-xs text-gray-500">
              Used to verify webhook requests from LemonSqueezy
            </p>
          </div>

          {/* Plan IDs Mapping */}
          <div className="space-y-4 pt-6 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                  <DollarSign className="w-5 h-5 text-purple-600" />
                  Plan ID Mapping
                </h4>
                <p className="text-sm text-gray-600">Map your LemonSqueezy product/variant IDs to subscription plans</p>
              </div>
              <Button
                onClick={fetchProducts}
                disabled={!settings.lemonsqueezy.api_key || !settings.lemonsqueezy.store_id || fetchingProducts}
                variant="outline"
                className="text-sm"
              >
                {fetchingProducts ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-purple-600 mr-2"></div>
                    Fetching...
                  </>
                ) : (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2" />
                    Auto-Fetch Products
                  </>
                )}
              </Button>
            </div>

            {/* Free Plan */}
            <div className="space-y-2">
              <label className="text-sm font-semibold text-gray-700">
                Free Plan ID
              </label>
              <input
                type="text"
                value={settings.lemonsqueezy.plans.free}
                onChange={(e) => updatePlanId('free', e.target.value)}
                placeholder="Leave empty if not applicable"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            {/* Starter Plan */}
            <div className="space-y-2">
              <label className="text-sm font-semibold text-gray-700">
                Starter Plan ID
                <span className="text-red-500 ml-1">*</span>
              </label>
              <input
                type="text"
                value={settings.lemonsqueezy.plans.starter}
                onChange={(e) => updatePlanId('starter', e.target.value)}
                placeholder="Enter LemonSqueezy variant ID for Starter plan"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            {/* Professional Plan */}
            <div className="space-y-2">
              <label className="text-sm font-semibold text-gray-700">
                Professional Plan ID
                <span className="text-red-500 ml-1">*</span>
              </label>
              <input
                type="text"
                value={settings.lemonsqueezy.plans.professional}
                onChange={(e) => updatePlanId('professional', e.target.value)}
                placeholder="Enter LemonSqueezy variant ID for Professional plan"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            {/* Enterprise Plan */}
            <div className="space-y-2">
              <label className="text-sm font-semibold text-gray-700">
                Enterprise Plan ID
                <span className="text-red-500 ml-1">*</span>
              </label>
              <input
                type="text"
                value={settings.lemonsqueezy.plans.enterprise}
                onChange={(e) => updatePlanId('enterprise', e.target.value)}
                placeholder="Enter LemonSqueezy variant ID for Enterprise plan"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            <div className="flex items-start gap-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <AlertTriangle className="w-4 h-4 text-yellow-600 flex-shrink-0 mt-0.5" />
              <div className="text-xs text-yellow-800">
                <p className="font-semibold mb-1">How to find Product/Variant IDs:</p>
                <ol className="list-decimal list-inside space-y-1">
                  <li>Go to your LemonSqueezy dashboard → Products</li>
                  <li>Click on a product to view its details</li>
                  <li>The Product ID is in the URL or product details</li>
                  <li>Variant IDs are listed under each product variant</li>
                  <li>Use Variant IDs here for subscription plans</li>
                </ol>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Save Button (Bottom) */}
      <div className="flex justify-end">
        <Button 
          onClick={saveSettings} 
          disabled={saving} 
          className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8"
        >
          {saving ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Saving...
            </>
          ) : (
            <>
              <Save className="w-4 h-4 mr-2" />
              Save All Settings
            </>
          )}
        </Button>
      </div>
    </div>
  );
};

export default PaymentGatewaySettings;
