import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { ArrowLeft, Upload, Link2, FileText, Trash2, Settings, Palette, Code, BarChart3, Plus } from 'lucide-react';
import { mockSources, mockChatbots, mockAnalytics } from '../mock/mockData';
import { useToast } from '../hooks/use-toast';
import AddSourceModal from '../components/AddSourceModal';
import ChatPreviewModal from '../components/ChatPreviewModal';
import DeleteConfirmModal from '../components/DeleteConfirmModal';

const ChatbotBuilder = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();
  const [sources, setSources] = useState([]);
  const [chatbot, setChatbot] = useState(null);
  const [settings, setSettings] = useState({
    name: '',
    model: 'gpt-4',
    temperature: 0.7,
    instructions: '',
    welcomeMessage: 'Hello! How can I help you today?'
  });
  const [widgetSettings, setWidgetSettings] = useState({
    primaryColor: '#000000',
    position: 'bottom-right',
    buttonText: 'Chat with us'
  });
  const [isAddSourceModalOpen, setIsAddSourceModalOpen] = useState(false);
  const [isPreviewModalOpen, setIsPreviewModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [sourceToDelete, setSourceToDelete] = useState(null);
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    if (id === 'new') {
      setChatbot({ id: 'new', name: 'New Chatbot' });
    } else {
      const bot = mockChatbots.find(b => b.id === id);
      setChatbot(bot);
      if (bot) {
        setSettings(prev => ({ ...prev, name: bot.name, model: bot.model }));
        setSources(mockSources);
        setAnalytics(mockAnalytics);
      }
    }
  }, [id]);

  const handleAddSource = (newSource) => {
    setSources([...sources, newSource]);
  };

  const handleDeleteSource = (sourceId) => {
    setSources(sources.filter(s => s.id !== sourceId));
    toast({
      title: 'Source deleted',
      description: 'Training source has been removed'
    });
  };

  const handleSaveSettings = () => {
    toast({
      title: 'Settings saved',
      description: 'Your chatbot settings have been updated'
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <nav className="bg-white border-b border-gray-200">
        <div className="px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')}>
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div>
              <h1 className="text-xl font-semibold">{chatbot?.name || 'Loading...'}</h1>
              <p className="text-sm text-gray-500">Configure your AI agent</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" onClick={() => setIsPreviewModalOpen(true)}>Preview</Button>
            <Button className="bg-black hover:bg-gray-800 text-white" onClick={handleSaveSettings}>
              Save Changes
            </Button>
          </div>
        </div>
      </nav>

      <div className="p-6 max-w-7xl mx-auto">
        <Tabs defaultValue="sources" className="w-full">
          <TabsList className="mb-6">
            <TabsTrigger value="sources">Sources</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
            <TabsTrigger value="widget">Widget</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
          </TabsList>

          {/* Sources Tab */}
          <TabsContent value="sources">
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-2xl font-bold mb-2">Training Data</h2>
              <p className="text-gray-600 mb-6">Add data sources to train your AI agent</p>
              
              <div className="grid md:grid-cols-3 gap-4 mb-8">
                <button 
                  className="p-6 border-2 border-dashed border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all"
                  onClick={() => setIsAddSourceModalOpen(true)}
                >
                  <Upload className="w-8 h-8 mx-auto mb-3 text-gray-600" />
                  <p className="font-medium">Upload Files</p>
                  <p className="text-sm text-gray-500 mt-1">PDF, DOC, TXT</p>
                </button>
                
                <button 
                  className="p-6 border-2 border-dashed border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all"
                  onClick={() => setIsAddSourceModalOpen(true)}
                >
                  <Link2 className="w-8 h-8 mx-auto mb-3 text-gray-600" />
                  <p className="font-medium">Website URL</p>
                  <p className="text-sm text-gray-500 mt-1">Crawl & scrape</p>
                </button>
                
                <button 
                  className="p-6 border-2 border-dashed border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all"
                  onClick={() => setIsAddSourceModalOpen(true)}
                >
                  <FileText className="w-8 h-8 mx-auto mb-3 text-gray-600" />
                  <p className="font-medium">Text Content</p>
                  <p className="text-sm text-gray-500 mt-1">Paste directly</p>
                </button>
              </div>

              <div className="space-y-3">
                <h3 className="font-semibold mb-3">Current Sources</h3>
                {sources.map((source) => (
                  <div key={source.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div className="flex items-center gap-3">
                      {source.type === 'file' && <FileText className="w-5 h-5 text-gray-600" />}
                      {source.type === 'website' && <Link2 className="w-5 h-5 text-gray-600" />}
                      {source.type === 'text' && <FileText className="w-5 h-5 text-gray-600" />}
                      <div>
                        <p className="font-medium">{source.name}</p>
                        <p className="text-sm text-gray-500">
                          {source.size && `${source.size} • `}
                          Status: {source.status}
                        </p>
                      </div>
                    </div>
                    <Button variant="ghost" size="icon" onClick={() => {
                      setSourceToDelete(source);
                      setIsDeleteModalOpen(true);
                    }}>
                      <Trash2 className="w-4 h-4 text-red-500" />
                    </Button>
                  </div>
                ))}
              </div>
            </div>
          </TabsContent>

          {/* Settings Tab */}
          <TabsContent value="settings">
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-2xl font-bold mb-6">Chatbot Settings</h2>
              
              <div className="space-y-6 max-w-2xl">
                <div>
                  <Label htmlFor="name">Chatbot Name</Label>
                  <Input
                    id="name"
                    value={settings.name}
                    onChange={(e) => setSettings({...settings, name: e.target.value})}
                    placeholder="My Support Bot"
                    className="mt-2"
                  />
                </div>
                
                <div>
                  <Label htmlFor="model">AI Model</Label>
                  <Select value={settings.model} onValueChange={(value) => setSettings({...settings, model: value})}>
                    <SelectTrigger className="mt-2">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="gpt-4">GPT-4 (Most Capable)</SelectItem>
                      <SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo (Faster)</SelectItem>
                      <SelectItem value="claude-3">Claude 3 Opus</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <Label htmlFor="instructions">System Instructions</Label>
                  <Textarea
                    id="instructions"
                    value={settings.instructions}
                    onChange={(e) => setSettings({...settings, instructions: e.target.value})}
                    placeholder="You are a helpful customer support assistant. Always be polite and professional..."
                    className="mt-2 min-h-[120px]"
                  />
                </div>
                
                <div>
                  <Label htmlFor="welcome">Welcome Message</Label>
                  <Input
                    id="welcome"
                    value={settings.welcomeMessage}
                    onChange={(e) => setSettings({...settings, welcomeMessage: e.target.value})}
                    placeholder="Hello! How can I help you today?"
                    className="mt-2"
                  />
                </div>
                
                <div>
                  <Label htmlFor="temperature">Temperature: {settings.temperature}</Label>
                  <input
                    id="temperature"
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={settings.temperature}
                    onChange={(e) => setSettings({...settings, temperature: parseFloat(e.target.value)})}
                    className="w-full mt-2"
                  />
                  <p className="text-sm text-gray-500 mt-1">Lower values make the output more focused and deterministic</p>
                </div>
              </div>
            </div>
          </TabsContent>

          {/* Widget Tab */}
          <TabsContent value="widget">
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-2xl font-bold mb-6">Chat Widget Customization</h2>
              
              <div className="grid md:grid-cols-2 gap-8">
                <div className="space-y-6">
                  <div>
                    <Label htmlFor="primaryColor">Primary Color</Label>
                    <div className="flex gap-3 mt-2">
                      <Input
                        id="primaryColor"
                        type="color"
                        value={widgetSettings.primaryColor}
                        onChange={(e) => setWidgetSettings({...widgetSettings, primaryColor: e.target.value})}
                        className="w-20 h-12"
                      />
                      <Input
                        value={widgetSettings.primaryColor}
                        onChange={(e) => setWidgetSettings({...widgetSettings, primaryColor: e.target.value})}
                        className="flex-1"
                      />
                    </div>
                  </div>
                  
                  <div>
                    <Label htmlFor="position">Widget Position</Label>
                    <Select value={widgetSettings.position} onValueChange={(value) => setWidgetSettings({...widgetSettings, position: value})}>
                      <SelectTrigger className="mt-2">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="bottom-right">Bottom Right</SelectItem>
                        <SelectItem value="bottom-left">Bottom Left</SelectItem>
                        <SelectItem value="top-right">Top Right</SelectItem>
                        <SelectItem value="top-left">Top Left</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <Label htmlFor="buttonText">Button Text</Label>
                    <Input
                      id="buttonText"
                      value={widgetSettings.buttonText}
                      onChange={(e) => setWidgetSettings({...widgetSettings, buttonText: e.target.value})}
                      className="mt-2"
                    />
                  </div>
                  
                  <div>
                    <Label>Embed Code</Label>
                    <div className="mt-2 p-4 bg-gray-900 text-gray-100 rounded-lg font-mono text-sm overflow-x-auto">
                      <code>
                        {`<script>
  window.chatbaseConfig = {
    chatbotId: "${id}"
  };
</script>
<script src="https://chatbase.co/embed.js"></script>`}
                      </code>
                    </div>
                  </div>
                </div>
                
                <div>
                  <Label>Preview</Label>
                  <div className="mt-2 border-2 border-gray-200 rounded-xl p-8 bg-gray-50 min-h-[400px] relative">
                    <div 
                      className="absolute w-16 h-16 rounded-full shadow-lg flex items-center justify-center cursor-pointer hover:scale-110 transition-transform"
                      style={{ 
                        backgroundColor: widgetSettings.primaryColor,
                        [widgetSettings.position.split('-')[0]]: '20px',
                        [widgetSettings.position.split('-')[1]]: '20px'
                      }}
                    >
                      <span className="text-white text-2xl">💬</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </TabsContent>

          {/* Analytics Tab */}
          <TabsContent value="analytics">
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-2xl font-bold mb-6">Chatbot Analytics</h2>
              
              {analytics && (
                <>
                  <div className="grid md:grid-cols-4 gap-4 mb-8">
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <p className="text-2xl font-bold">{analytics.totalConversations}</p>
                      <p className="text-sm text-gray-600">Total Conversations</p>
                    </div>
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <p className="text-2xl font-bold">{analytics.activeChats}</p>
                      <p className="text-sm text-gray-600">Active Chats</p>
                    </div>
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <p className="text-2xl font-bold">{analytics.satisfaction}%</p>
                      <p className="text-sm text-gray-600">Satisfaction</p>
                    </div>
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <p className="text-2xl font-bold">{analytics.avgResponseTime}</p>
                      <p className="text-sm text-gray-600">Avg Response</p>
                    </div>
                  </div>
                  
                  <div className="mb-8">
                    <h3 className="font-semibold mb-4">Top Topics Discussed</h3>
                    <div className="space-y-3">
                      {analytics.topicsDiscussed.slice(0, 5).map((topic, index) => (
                        <div key={index} className="flex items-center gap-4">
                          <span className="font-medium w-32">{topic.topic}</span>
                          <div className="flex-1 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-black h-2 rounded-full" 
                              style={{ width: `${(topic.count / 500) * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-sm text-gray-600">{topic.count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </div>

      {/* Modals */}
      <AddSourceModal 
        isOpen={isAddSourceModalOpen}
        onClose={() => setIsAddSourceModalOpen(false)}
        onAdd={handleAddSource}
      />
      
      <ChatPreviewModal
        isOpen={isPreviewModalOpen}
        onClose={() => setIsPreviewModalOpen(false)}
        chatbot={settings}
      />
      
      <DeleteConfirmModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        onConfirm={() => handleDeleteSource(sourceToDelete?.id)}
        title="Delete Source"
        description="Are you sure you want to delete this training source? This action cannot be undone."
      />
    </div>
  );
};

export default ChatbotBuilder;
