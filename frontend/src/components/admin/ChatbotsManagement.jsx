import React, { useState, useEffect } from 'react';
import { Bot, Power, PowerOff, Trash2, Search, CheckSquare } from 'lucide-react';
import { Button } from '../ui/button';

const ChatbotsManagement = ({ backendUrl }) => {
  const [chatbots, setChatbots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);

  useEffect(() => {
    fetchChatbots();
  }, []);

  const fetchChatbots = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${backendUrl}/api/admin/chatbots/detailed`);
      const data = await response.json();
      setChatbots(data.chatbots || []);
    } catch (error) {
      console.error('Error fetching chatbots:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleChatbot = async (chatbotId) => {
    try {
      const response = await fetch(`${backendUrl}/api/admin/chatbots/${chatbotId}/toggle`, {
        method: 'PUT'
      });
      const data = await response.json();
      if (data.success) {
        fetchChatbots();
      }
    } catch (error) {
      console.error('Error toggling chatbot:', error);
    }
  };

  const bulkOperation = async (operation) => {
    if (selectedIds.length === 0) {
      alert('Please select chatbots first');
      return;
    }

    if (operation === 'delete' && !window.confirm(`Delete ${selectedIds.length} chatbots?`)) {
      return;
    }

    try {
      const response = await fetch(`${backendUrl}/api/admin/chatbots/bulk`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ids: selectedIds,
          operation: operation
        })
      });
      const data = await response.json();
      if (data.success) {
        alert(`${operation} completed: ${data.affected} chatbots affected`);
        setSelectedIds([]);
        fetchChatbots();
      }
    } catch (error) {
      console.error('Error in bulk operation:', error);
    }
  };

  const toggleSelection = (id) => {
    setSelectedIds(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  const filteredChatbots = chatbots.filter(bot =>
    bot.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    bot.user_id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">Chatbot Management</h2>
        <div className="flex gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search chatbots..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {selectedIds.length > 0 && (
        <div className="mb-4 p-4 bg-purple-50 rounded-lg flex items-center justify-between">
          <span className="text-sm font-medium">
            {selectedIds.length} chatbot(s) selected
          </span>
          <div className="flex gap-2">
            <Button size="sm" onClick={() => bulkOperation('enable')} className="bg-green-600 hover:bg-green-700">
              <Power className="w-4 h-4 mr-2" />
              Enable
            </Button>
            <Button size="sm" onClick={() => bulkOperation('disable')} className="bg-yellow-600 hover:bg-yellow-700">
              <PowerOff className="w-4 h-4 mr-2" />
              Disable
            </Button>
            <Button size="sm" onClick={() => bulkOperation('delete')} className="bg-red-600 hover:bg-red-700">
              <Trash2 className="w-4 h-4 mr-2" />
              Delete
            </Button>
          </div>
        </div>
      )}

      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
        </div>
      ) : filteredChatbots.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <Bot className="w-16 h-16 mx-auto mb-4 opacity-50" />
          <p>No chatbots found</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4">
                  <input
                    type="checkbox"
                    checked={selectedIds.length === filteredChatbots.length}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedIds(filteredChatbots.map(b => b.id));
                      } else {
                        setSelectedIds([]);
                      }
                    }}
                    className="rounded"
                  />
                </th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Name</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Owner</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Provider</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Model</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Sources</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Conversations</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Messages</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredChatbots.map((bot) => (
                <tr key={bot.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4">
                    <input
                      type="checkbox"
                      checked={selectedIds.includes(bot.id)}
                      onChange={() => toggleSelection(bot.id)}
                      className="rounded"
                    />
                  </td>
                  <td className="py-3 px-4 font-medium">{bot.name}</td>
                  <td className="py-3 px-4 text-sm text-gray-600">{bot.user_id}</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">
                      {bot.ai_provider}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-sm">{bot.ai_model}</td>
                  <td className="py-3 px-4 text-center">{bot.sources_count}</td>
                  <td className="py-3 px-4 text-center">{bot.conversations_count}</td>
                  <td className="py-3 px-4 text-center">{bot.messages_count}</td>
                  <td className="py-3 px-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      bot.enabled !== false ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                    }`}>
                      {bot.enabled !== false ? 'Enabled' : 'Disabled'}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => toggleChatbot(bot.id)}
                    >
                      {bot.enabled !== false ? (
                        <PowerOff className="w-4 h-4 text-yellow-600" />
                      ) : (
                        <Power className="w-4 h-4 text-green-600" />
                      )}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ChatbotsManagement;
