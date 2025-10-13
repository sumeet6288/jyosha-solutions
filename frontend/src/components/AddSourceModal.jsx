import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Upload, Link2, FileText } from 'lucide-react';
import { useToast } from '../hooks/use-toast';

const AddSourceModal = ({ isOpen, onClose, onAdd }) => {
  const { toast } = useToast();
  const [fileData, setFileData] = useState(null);
  const [urlData, setUrlData] = useState('');
  const [textData, setTextData] = useState({ name: '', content: '' });

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileData(file);
    }
  };

  const handleAddFile = () => {
    if (!fileData) {
      toast({ title: 'Error', description: 'Please select a file', variant: 'destructive' });
      return;
    }
    const newSource = {
      id: Date.now().toString(),
      type: 'file',
      name: fileData.name,
      size: `${(fileData.size / 1024 / 1024).toFixed(2)} MB`,
      status: 'processing',
      addedAt: new Date().toISOString().split('T')[0]
    };
    onAdd(newSource);
    toast({ title: 'Success', description: 'File uploaded successfully' });
    setFileData(null);
    onClose();
  };

  const handleAddUrl = () => {
    if (!urlData) {
      toast({ title: 'Error', description: 'Please enter a URL', variant: 'destructive' });
      return;
    }
    const newSource = {
      id: Date.now().toString(),
      type: 'website',
      name: urlData,
      status: 'processing',
      addedAt: new Date().toISOString().split('T')[0]
    };
    onAdd(newSource);
    toast({ title: 'Success', description: 'Website URL added successfully' });
    setUrlData('');
    onClose();
  };

  const handleAddText = () => {
    if (!textData.name || !textData.content) {
      toast({ title: 'Error', description: 'Please provide both name and content', variant: 'destructive' });
      return;
    }
    const newSource = {
      id: Date.now().toString(),
      type: 'text',
      name: textData.name,
      status: 'processed',
      addedAt: new Date().toISOString().split('T')[0]
    };
    onAdd(newSource);
    toast({ title: 'Success', description: 'Text content added successfully' });
    setTextData({ name: '', content: '' });
    onClose();
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
                  className="hidden"
                  onChange={handleFileUpload}
                  accept=".pdf,.doc,.docx,.txt"
                />
              </Label>
              {fileData && (
                <p className="mt-4 text-sm font-medium">{fileData.name}</p>
              )}
            </div>
            <Button onClick={handleAddFile} className="w-full bg-black hover:bg-gray-800 text-white">
              Upload File
            </Button>
          </TabsContent>

          <TabsContent value="url" className="space-y-4">
            <div>
              <Label htmlFor="website-url">Website URL</Label>
              <Input
                id="website-url"
                type="url"
                placeholder="https://example.com"
                value={urlData}
                onChange={(e) => setUrlData(e.target.value)}
                className="mt-2"
              />
            </div>
            <Button onClick={handleAddUrl} className="w-full bg-black hover:bg-gray-800 text-white">
              Add Website
            </Button>
          </TabsContent>

          <TabsContent value="text" className="space-y-4">
            <div>
              <Label htmlFor="text-name">Content Name</Label>
              <Input
                id="text-name"
                placeholder="FAQ Content"
                value={textData.name}
                onChange={(e) => setTextData({ ...textData, name: e.target.value })}
                className="mt-2"
              />
            </div>
            <div>
              <Label htmlFor="text-content">Content</Label>
              <Textarea
                id="text-content"
                placeholder="Paste your content here..."
                value={textData.content}
                onChange={(e) => setTextData({ ...textData, content: e.target.value })}
                className="mt-2 min-h-[200px]"
              />
            </div>
            <Button onClick={handleAddText} className="w-full bg-black hover:bg-gray-800 text-white">
              Add Text Content
            </Button>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
};

export default AddSourceModal;