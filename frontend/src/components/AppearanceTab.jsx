import React, { useState, useEffect } from 'react';
import { Palette, Image, Type, Layout, Eye } from 'lucide-react';
import { chatbotAPI } from '../utils/api';
import { toast } from 'sonner';

const AppearanceTab = ({ chatbot, onUpdate }) => {
  const [customization, setCustomization] = useState({
    primary_color: chatbot?.primary_color || '#7c3aed',
    secondary_color: chatbot?.secondary_color || '#a78bfa',
    accent_color: chatbot?.accent_color || '#ec4899',
    logo_url: chatbot?.logo_url || '',
    avatar_url: chatbot?.avatar_url || '',
    welcome_message: chatbot?.welcome_message || 'Hello! How can I help you today?',
    widget_position: chatbot?.widget_position || 'bottom-right',
    widget_theme: chatbot?.widget_theme || 'light',
    font_family: chatbot?.font_family || 'Inter, system-ui, sans-serif',
    font_size: chatbot?.font_size || 'medium',
    bubble_style: chatbot?.bubble_style || 'rounded',
    widget_size: chatbot?.widget_size || 'medium',
    auto_expand: chatbot?.auto_expand || false,
  });

  const [saving, setSaving] = useState(false);

  const handleChange = (field, value) => {
    setCustomization(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await chatbotAPI.update(chatbot.id, customization);
      toast.success('Appearance updated successfully! Open the live preview to see changes.');
      if (onUpdate) {
        await onUpdate();
      }
    } catch (error) {
      console.error('Error updating appearance:', error);
      toast.error('Failed to update appearance');
    } finally {
      setSaving(false);
    }
  };

  const handleViewLivePreview = () => {
    // Add timestamp to force reload and bypass cache
    const previewUrl = `/public-chat/${chatbot.id}?t=${Date.now()}`;
    window.open(previewUrl, '_blank');
  };

  return (
    <div className="space-y-6">
      {/* Color Customization */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center space-x-2 mb-4">
          <Palette className="w-5 h-5 text-purple-600" />
          <h3 className="text-lg font-semibold">Color Theme</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Primary Color
            </label>
            <div className="flex items-center space-x-3">
              <input
                type="color"
                value={customization.primary_color}
                onChange={(e) => handleChange('primary_color', e.target.value)}
                className="h-10 w-20 rounded border border-gray-300 cursor-pointer"
              />
              <input
                type="text"
                value={customization.primary_color}
                onChange={(e) => handleChange('primary_color', e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="#7c3aed"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Secondary Color
            </label>
            <div className="flex items-center space-x-3">
              <input
                type="color"
                value={customization.secondary_color}
                onChange={(e) => handleChange('secondary_color', e.target.value)}
                className="h-10 w-20 rounded border border-gray-300 cursor-pointer"
              />
              <input
                type="text"
                value={customization.secondary_color}
                onChange={(e) => handleChange('secondary_color', e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="#a78bfa"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Accent Color
            </label>
            <div className="flex items-center space-x-3">
              <input
                type="color"
                value={customization.accent_color}
                onChange={(e) => handleChange('accent_color', e.target.value)}
                className="h-10 w-20 rounded border border-gray-300 cursor-pointer"
              />
              <input
                type="text"
                value={customization.accent_color}
                onChange={(e) => handleChange('accent_color', e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="#ec4899"
              />
            </div>
          </div>
        </div>

        {/* Color Preview */}
        <div className="mt-4 p-4 rounded-lg border-2 border-gray-200">
          <p className="text-sm text-gray-600 mb-2">Preview:</p>
          <div className="flex space-x-2">
            <div 
              className="w-20 h-20 rounded-lg shadow-md"
              style={{ backgroundColor: customization.primary_color }}
            />
            <div 
              className="w-20 h-20 rounded-lg shadow-md"
              style={{ backgroundColor: customization.secondary_color }}
            />
            <div 
              className="w-20 h-20 rounded-lg shadow-md"
              style={{ backgroundColor: customization.accent_color }}
            />
          </div>
        </div>
      </div>

      {/* Font Customization */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center space-x-2 mb-4">
          <Type className="w-5 h-5 text-purple-600" />
          <h3 className="text-lg font-semibold">Font Customization</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Font Family
            </label>
            <select
              value={customization.font_family}
              onChange={(e) => handleChange('font_family', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="Inter, system-ui, sans-serif">Inter (Default)</option>
              <option value="Arial, sans-serif">Arial</option>
              <option value="Helvetica, sans-serif">Helvetica</option>
              <option value="Georgia, serif">Georgia</option>
              <option value="'Times New Roman', serif">Times New Roman</option>
              <option value="'Courier New', monospace">Courier New</option>
              <option value="Verdana, sans-serif">Verdana</option>
              <option value="'Trebuchet MS', sans-serif">Trebuchet MS</option>
              <option value="Roboto, sans-serif">Roboto</option>
              <option value="'Open Sans', sans-serif">Open Sans</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Font Size
            </label>
            <select
              value={customization.font_size}
              onChange={(e) => handleChange('font_size', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="small">Small (14px)</option>
              <option value="medium">Medium (16px)</option>
              <option value="large">Large (18px)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Chat Bubble Style */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center space-x-2 mb-4">
          <Layout className="w-5 h-5 text-purple-600" />
          <h3 className="text-lg font-semibold">Chat Bubble Style</h3>
        </div>
        
        <div className="grid grid-cols-3 gap-4">
          <button
            onClick={() => handleChange('bubble_style', 'rounded')}
            className={`p-4 border-2 rounded-lg transition-all ${
              customization.bubble_style === 'rounded'
                ? 'border-purple-500 bg-purple-50'
                : 'border-gray-200 hover:border-purple-300'
            }`}
          >
            <div className="w-full h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl mb-2"></div>
            <p className="text-sm font-medium text-center">Rounded</p>
          </button>
          
          <button
            onClick={() => handleChange('bubble_style', 'smooth')}
            className={`p-4 border-2 rounded-lg transition-all ${
              customization.bubble_style === 'smooth'
                ? 'border-purple-500 bg-purple-50'
                : 'border-gray-200 hover:border-purple-300'
            }`}
          >
            <div className="w-full h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg mb-2"></div>
            <p className="text-sm font-medium text-center">Smooth</p>
          </button>
          
          <button
            onClick={() => handleChange('bubble_style', 'square')}
            className={`p-4 border-2 rounded-lg transition-all ${
              customization.bubble_style === 'square'
                ? 'border-purple-500 bg-purple-50'
                : 'border-gray-200 hover:border-purple-300'
            }`}
          >
            <div className="w-full h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded mb-2"></div>
            <p className="text-sm font-medium text-center">Square</p>
          </button>
        </div>
      </div>

      {/* Branding */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center space-x-2 mb-4">
          <Image className="w-5 h-5 text-purple-600" />
          <h3 className="text-lg font-semibold">Branding</h3>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Logo URL
            </label>
            <input
              type="url"
              value={customization.logo_url}
              onChange={(e) => handleChange('logo_url', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="https://example.com/logo.png"
            />
            {customization.logo_url && (
              <div className="mt-2 p-3 border border-gray-200 rounded-lg bg-gray-50">
                <p className="text-xs text-gray-500 mb-2">Logo Preview:</p>
                <img 
                  src={customization.logo_url} 
                  alt="Logo preview" 
                  className="h-12 object-contain"
                  onError={(e) => {
                    e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50"><rect width="100" height="50" fill="%23e5e7eb"/><text x="50" y="25" text-anchor="middle" fill="%236b7280" font-size="10">Invalid URL</text></svg>';
                    e.target.classList.add('opacity-50');
                  }}
                />
              </div>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Avatar URL
            </label>
            <input
              type="url"
              value={customization.avatar_url}
              onChange={(e) => handleChange('avatar_url', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="https://example.com/avatar.png"
            />
            {customization.avatar_url && (
              <div className="mt-2 p-3 border border-gray-200 rounded-lg bg-gray-50">
                <p className="text-xs text-gray-500 mb-2">Avatar Preview:</p>
                <img 
                  src={customization.avatar_url} 
                  alt="Avatar preview" 
                  className="w-12 h-12 rounded-full object-cover border-2 border-gray-300"
                  onError={(e) => {
                    e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48"><circle cx="24" cy="24" r="24" fill="%23e5e7eb"/><text x="24" y="28" text-anchor="middle" fill="%236b7280" font-size="12">!</text></svg>';
                    e.target.classList.add('opacity-50');
                  }}
                />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Welcome Message */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center space-x-2 mb-4">
          <Type className="w-5 h-5 text-purple-600" />
          <h3 className="text-lg font-semibold">Welcome Message</h3>
        </div>
        
        <textarea
          value={customization.welcome_message}
          onChange={(e) => handleChange('welcome_message', e.target.value)}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          placeholder="Enter welcome message..."
        />
      </div>

      {/* Widget Settings */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center space-x-2 mb-4">
          <Layout className="w-5 h-5 text-purple-600" />
          <h3 className="text-lg font-semibold">Widget Settings</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Position
            </label>
            <select
              value={customization.widget_position}
              onChange={(e) => handleChange('widget_position', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="bottom-right">Bottom Right</option>
              <option value="bottom-left">Bottom Left</option>
              <option value="top-right">Top Right</option>
              <option value="top-left">Top Left</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Theme
            </label>
            <select
              value={customization.widget_theme}
              onChange={(e) => handleChange('widget_theme', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="auto">Auto</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Widget Size
            </label>
            <select
              value={customization.widget_size}
              onChange={(e) => handleChange('widget_size', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="small">Small (360px)</option>
              <option value="medium">Medium (420px)</option>
              <option value="large">Large (500px)</option>
            </select>
          </div>
        </div>

        {/* Auto-expand Toggle */}
        <div className="flex items-center justify-between p-4 bg-purple-50 rounded-lg border border-purple-200">
          <div>
            <p className="font-medium text-gray-900">Auto-expand Widget</p>
            <p className="text-sm text-gray-600">Automatically open chat widget when page loads</p>
          </div>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={customization.auto_expand}
              onChange={(e) => handleChange('auto_expand', e.target.checked)}
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
          </label>
        </div>
      </div>

      {/* Live Preview Notice */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            <svg className="w-5 h-5 text-blue-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="flex-1">
            <h4 className="text-sm font-semibold text-blue-900 mb-1">Live Preview</h4>
            <p className="text-sm text-blue-700">
              After saving, click "View Live Preview" below to see your changes in action. The preview will open in a new tab with the latest appearance settings.
            </p>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-between items-center">
        <button
          onClick={handleViewLivePreview}
          className="px-6 py-3 bg-white border-2 border-purple-600 text-purple-600 rounded-lg hover:bg-purple-50 transition-all shadow-md font-semibold flex items-center space-x-2"
        >
          <Eye className="w-5 h-5" />
          <span>View Live Preview</span>
        </button>
        <button
          onClick={handleSave}
          disabled={saving}
          className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all shadow-lg disabled:opacity-50 font-semibold"
        >
          {saving ? 'Saving...' : 'Save Appearance'}
        </button>
      </div>
    </div>
  );
};

export default AppearanceTab;
