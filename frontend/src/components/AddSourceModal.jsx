import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Upload, Link2, FileText, Loader2 } from 'lucide-react';
import { useToast } from '../hooks/use-toast';
import { sourceAPI } from '../utils/api';

const AddSourceModal = ({ isOpen, onClose, chatbotId, onSuccess }) => {
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);
  const [fileData, setFileData] = useState(null);
  const [urlData, setUrlData] = useState('');
  const [textData, setTextData] = useState({ name: '', content: '' });

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Check file size (max 100MB)
      if (file.size > 100 * 1024 * 1024) {
        toast({ 
          title: 'Error', 
          description: 'File size must be less than 100MB', 
          variant: 'destructive' 
        });
        return;
      }
      setFileData(file);
    }
  };

  const handleAddFile = async () => {
    if (!fileData) {
      toast({ title: 'Error', description: 'Please select a file', variant: 'destructive' });
      return;
    }
    
    setLoading(true);
    try {
      await sourceAPI.uploadFile(chatbotId, fileData);
      toast({ title: 'Success', description: 'File uploaded successfully. Processing...' });
      setFileData(null);
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Error uploading file:', error);
      toast({ 
        title: 'Error', 
        description: error.response?.data?.detail || 'Failed to upload file', 
        variant: 'destructive' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAddUrl = async () => {
    if (!urlData) {
      toast({ title: 'Error', description: 'Please enter a URL', variant: 'destructive' });
      return;
    }
    
    // Basic URL validation
    try {
      new URL(urlData);
    } catch {
      toast({ title: 'Error', description: 'Please enter a valid URL', variant: 'destructive' });
      return;
    }
    
    setLoading(true);
    try {
      await sourceAPI.addWebsite(chatbotId, urlData);
      toast({ title: 'Success', description: 'Website URL added successfully. Scraping...' });
      setUrlData('');
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Error adding URL:', error);
      toast({ 
        title: 'Error', 
        description: error.response?.data?.detail || 'Failed to add website', 
        variant: 'destructive' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAddText = async () => {
    if (!textData.name || !textData.content) {
      toast({ title: 'Error', description: 'Please provide both name and content', variant: 'destructive' });
      return;
    }
    
    setLoading(true);
    try {
      await sourceAPI.addText(chatbotId, textData.name, textData.content);
      toast({ title: 'Success', description: 'Text content added successfully' });
      setTextData({ name: '', content: '' });
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Error adding text:', error);
      let errorMessage = 'Failed to add text';
      if (error.response?.data?.detail) {
        // Handle both string and array formats from FastAPI
        if (Array.isArray(error.response.data.detail)) {
          errorMessage = error.response.data.detail.map(err => err.msg).join(', ');
        } else {
          errorMessage = error.response.data.detail;
        }
      }
      toast({ 
        title: 'Error', 
        description: errorMessage, 
        variant: 'destructive' 
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Add Training Source</DialogTitle>
          <DialogDescription>Add data to train your AI chatbot</DialogDescription>
        </DialogHeader>
        
        <Tabs defaultValue="file" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="file">File Upload</TabsTrigger>
            <TabsTrigger value="url">Website URL</TabsTrigger>
            <TabsTrigger value="text">Text Content</TabsTrigger>
          </TabsList>

          <TabsContent value="file" className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-gray-400 transition-colors">
              <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
              <Label htmlFor="file-upload" className="cursor-pointer">
                <span className="text-sm text-gray-600">Click to upload or drag and drop</span>
                <Input
                  id="file-upload"
                  type="file"
                  onChange={handleFileUpload}
                  className="hidden"
                  accept=".pdf,.docx,.doc,.txt,.xlsx,.xls,.csv"
                />
              </Label>
              <p className="text-xs text-gray-500 mt-2">Supported: PDF, DOCX, TXT, XLSX, CSV (Max 100MB)</p>
              {fileData && (
                <p className="text-sm text-gray-700 mt-4 font-medium">Selected: {fileData.name}</p>
              )}
            </div>
            <Button onClick={handleAddFile} className="w-full" disabled={!fileData || loading}>
              {loading ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Uploading...</> : 'Upload File'}
            </Button>
          </TabsContent>

          <TabsContent value="url" className="space-y-4">
            <div className="space-y-2">
              <Label>Website URL</Label>
              <div className="flex items-center gap-2">
                <Link2 className="w-5 h-5 text-gray-400" />
                <Input
                  placeholder="https://example.com"
                  value={urlData}
                  onChange={(e) => setUrlData(e.target.value)}
                />
              </div>
              <p className="text-xs text-gray-500">We'll scrape and extract text content from this page</p>
            </div>
            <Button onClick={handleAddUrl} className="w-full" disabled={!urlData || loading}>
              {loading ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Adding...</> : 'Add Website'}
            </Button>
          </TabsContent>

          <TabsContent value="text" className="space-y-4">
            <div className="space-y-4">
              <div className="space-y-2">
                <Label>Content Name</Label>
                <Input
                  placeholder="e.g., Product Information"
                  value={textData.name}
                  onChange={(e) => setTextData({ ...textData, name: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <Label>Content</Label>
                <Textarea
                  placeholder="Paste your text content here..."
                  value={textData.content}
                  onChange={(e) => setTextData({ ...textData, content: e.target.value })}
                  rows={8}
                />
              </div>
            </div>
            <Button onClick={handleAddText} className="w-full" disabled={!textData.name || !textData.content || loading}>
              {loading ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Adding...</> : 'Add Text Content'}
            </Button>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
};

export default AddSourceModal;