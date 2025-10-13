import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { BookOpen, Video, FileText, HelpCircle } from 'lucide-react';

const Resources = () => {
  const navigate = useNavigate();

  const resources = [
    {
      icon: <BookOpen className="w-8 h-8" />,
      title: 'Documentation',
      description: 'Complete guides and API references',
      link: '#'
    },
    {
      icon: <Video className="w-8 h-8" />,
      title: 'Video Tutorials',
      description: 'Step-by-step video guides',
      link: '#'
    },
    {
      icon: <FileText className="w-8 h-8" />,
      title: 'Blog',
      description: 'Latest news and best practices',
      link: '#'
    },
    {
      icon: <HelpCircle className="w-8 h-8" />,
      title: 'Help Center',
      description: 'Get answers to common questions',
      link: '#'
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      <nav className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate('/')}>
            <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">C</span>
            </div>
            <span className="text-xl font-semibold">Chatbase</span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <button onClick={() => navigate('/pricing')} className="text-gray-700 hover:text-black transition-colors">Pricing</button>
            <button onClick={() => navigate('/enterprise')} className="text-gray-700 hover:text-black transition-colors">Enterprise</button>
            <button onClick={() => navigate('/resources')} className="text-black font-medium">Resources</button>
          </div>
          <div className="flex items-center gap-4">
            <Button variant="ghost" onClick={() => navigate('/signin')}>Sign in</Button>
            <Button className="bg-black hover:bg-gray-800 text-white rounded-lg" onClick={() => navigate('/signup')}>
              Try for Free
            </Button>
          </div>
        </div>
      </nav>

      <div className="pt-24 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h1 className="text-5xl font-bold mb-4">Resources</h1>
            <p className="text-xl text-gray-600">Everything you need to build amazing chatbots</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {resources.map((resource, index) => (
              <div key={index} className="p-8 rounded-2xl border border-gray-200 hover:shadow-lg transition-all cursor-pointer">
                <div className="w-16 h-16 bg-black rounded-xl flex items-center justify-center text-white mb-4">
                  {resource.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2">{resource.title}</h3>
                <p className="text-gray-600 mb-4">{resource.description}</p>
                <button className="text-black font-medium hover:underline">Learn more →</button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Resources;