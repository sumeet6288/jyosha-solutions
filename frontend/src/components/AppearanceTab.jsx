import React, { useState, useEffect } from 'react';
import { Palette, Image, Type, Layout } from 'lucide-react';
import api from '../services/api';
import { toast } from 'sonner';

const AppearanceTab = ({ chatbot, onUpdate }) => {
  const [customization, setCustomization] = useState({
    primary_color: chatbot?.primary_color || '#7c3aed',
    secondary_color: chatbot?.secondary_color || '#a78bfa',
    logo_url: chatbot?.logo_url || '',
    avatar_url: chatbot?.avatar_url || '',
    welcome_message: chatbot?.welcome_message || 'Hello! How can I help you today?',
    widget_position: chatbot?.widget_position || 'bottom-right',
    widget_theme: chatbot?.widget_theme || 'light',
  });

  const [saving, setSaving] = useState(false);

  const handleChange = (field, value) => {
    setCustomization(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await api.updateChatbot(chatbot.id, customization);
      toast.success('Appearance updated successfully!');
      onUpdate && onUpdate();
    } catch (error) {
      console.error('Error updating appearance:', error);
      toast.error('Failed to update appearance');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Color Customization */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center space-x-2 mb-4">
          <Palette className="w-5 h-5 text-purple-600" />
          <h3 className="text-lg font-semibold">Color Theme</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
          </div>
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
              <div className="mt-2">
                <img 
                  src={customization.logo_url} 
                  alt="Logo preview" 
                  className="h-12 object-contain"
                  onError={(e) => {
                    e.target.style.display = 'none';
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
              <div className="mt-2">
                <img 
                  src={customization.avatar_url} 
                  alt="Avatar preview" 
                  className="w-12 h-12 rounded-full object-cover"
                  onError={(e) => {
                    e.target.style.display = 'none';
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
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          disabled={saving}
          className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all shadow-lg disabled:opacity-50"
        >
          {saving ? 'Saving...' : 'Save Appearance'}
        </button>
      </div>
    </div>
  );
};

export default AppearanceTab;
