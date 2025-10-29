import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { BookOpen, Video, FileText, HelpCircle, Code, Lightbulb, Users2, ArrowRight, ArrowLeft } from 'lucide-react';

const Resources = () => {
  const navigate = useNavigate();
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  const resources = [
    {
      icon: <BookOpen className="w-8 h-8" />,
      title: 'Documentation',
      description: 'Complete guides and API references for developers',
      link: '/resources/documentation',
      gradient: 'from-purple-500 to-indigo-600'
    },
    {
      icon: <Video className="w-8 h-8" />,
      title: 'Video Tutorials',
      description: 'Step-by-step video guides to get you started quickly',
      link: '#',
      gradient: 'from-blue-500 to-cyan-600'
    },
    {
      icon: <FileText className="w-8 h-8" />,
      title: 'Blog',
      description: 'Latest news, updates, and best practices',
      link: '#',
      gradient: 'from-pink-500 to-rose-600'
    },
    {
      icon: <HelpCircle className="w-8 h-8" />,
      title: 'Help Center',
      description: 'Get answers to common questions instantly',
      link: '/resources/help-center',
      gradient: 'from-green-500 to-emerald-600'
    },
    {
      icon: <Lightbulb className="w-8 h-8" />,
      title: 'Use Cases',
      description: 'Real-world examples and implementation guides',
      link: '#',
      gradient: 'from-yellow-500 to-orange-600'
    },
    {
      icon: <Users2 className="w-8 h-8" />,
      title: 'Community',
      description: 'Join our community forum and connect with others',
      link: '/resources/community',
      gradient: 'from-teal-500 to-cyan-600'
    },
    {
      icon: <BookOpen className="w-8 h-8" />,
      title: 'Changelog',
      description: 'Stay updated with the latest features and fixes',
      link: '#',
      gradient: 'from-indigo-500 to-purple-600'
    }
  ];

  const categories = [
    { 
      title: 'Getting Started', 
      count: '4 articles', 
      color: 'from-purple-500 to-indigo-600',
      description: 'Learn the basics and create your first chatbot',
      icon: '🚀'
    },
    { 
      title: 'User Guides', 
      count: '5 articles', 
      color: 'from-blue-500 to-cyan-600',
      description: 'Master chatbot management and customization',
      icon: '📚'
    },
    { 
      title: 'Best Practices', 
      count: '15 articles', 
      color: 'from-pink-500 to-rose-600',
      description: 'Tips and tricks for optimal performance',
      icon: '💡'
    },
    { 
      title: 'Troubleshooting', 
      count: '20 articles', 
      color: 'from-green-500 to-emerald-600',
      description: 'Quick solutions to common issues',
      icon: '🔧'
    }
  ];

  return (
    <div className={`min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-pink-50 relative overflow-hidden transition-opacity duration-700 ${isLoaded ? 'opacity-100' : 'opacity-0'}`}>
      {/* Animated background elements */}
      <div className={`absolute inset-0 overflow-hidden pointer-events-none transition-transform duration-1000 ${isLoaded ? 'scale-100' : 'scale-110'}`}>
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-32 left-1/3 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <nav className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-lg border-b border-purple-200/50 z-50 shadow-sm">
        <div className="max-w-[95%] mx-auto px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 cursor-pointer group" onClick={() => navigate('/')}>
            <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300 shadow-lg shadow-purple-500/30">
              <span className="text-white font-bold text-lg">B</span>
            </div>
            <span className="text-xl font-semibold bg-gradient-to-r from-gray-900 to-purple-600 bg-clip-text text-transparent">BotSmith</span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <button onClick={() => navigate('/pricing')} className="text-gray-700 hover:text-purple-600 transition-colors font-medium">Pricing</button>
            <button onClick={() => navigate('/enterprise')} className="text-gray-700 hover:text-purple-600 transition-colors font-medium">Scale Up</button>
            <button onClick={() => navigate('/resources')} className="text-purple-600 font-semibold">Learn</button>
          </div>
          <div className="flex items-center gap-4">
            <Button variant="ghost" onClick={() => navigate('/signin')} className="hover:bg-purple-50">Sign in</Button>
            <Button className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-lg shadow-lg shadow-purple-500/30 transform hover:scale-105 transition-all duration-300" onClick={() => navigate('/signup')}>
              Try for Free
            </Button>
          </div>
        </div>
      </nav>

      <div className="pt-32 pb-20 px-8 relative z-10">
        <div className="max-w-[95%] mx-auto">
          {/* Back Button */}
          <div className="mb-6 animate-fade-in-up">
            <Button 
              variant="ghost" 
              onClick={() => navigate('/')} 
              className="group hover:bg-purple-50 text-gray-700 hover:text-purple-600"
            >
              <ArrowLeft className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" />
              Back to Home
            </Button>
          </div>
          
          {/* Hero Section */}
          <div className="text-center mb-20 animate-fade-in-up">
            <div className="inline-block mb-4">
              <span className="px-4 py-2 rounded-full bg-purple-100 text-purple-700 text-sm font-medium inline-flex items-center gap-2 animate-bounce-subtle">
                <Lightbulb className="w-4 h-4" />
                Learn & Grow
              </span>
            </div>
            <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-gray-900 via-purple-900 to-pink-900 bg-clip-text text-transparent">
              Learn
            </h1>
            <p className="text-2xl text-gray-600 max-w-3xl mx-auto">Everything you need to build, deploy, and optimize amazing AI chatbots</p>
          </div>

          {/* Quick Links Categories */}
          <div className="grid md:grid-cols-4 gap-6 mb-20 animate-fade-in-up">
            {categories.map((category, index) => (
              <div 
                key={index}
                className="group p-6 bg-white/80 backdrop-blur-sm rounded-2xl border-2 border-purple-200/50 hover:border-purple-400 hover:shadow-xl hover:shadow-purple-500/20 transition-all duration-300 transform hover:-translate-y-2 cursor-pointer"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="text-4xl mb-3 transform group-hover:scale-125 transition-transform duration-300">{category.icon}</div>
                <h3 className="text-lg font-bold mb-2 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-pink-600 group-hover:bg-clip-text transition-all duration-300">{category.title}</h3>
                <p className="text-sm text-gray-600 mb-2">{category.description}</p>
                <p className="text-xs text-gray-500 font-medium">{category.count}</p>
              </div>
            ))}
          </div>

          {/* Resources Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
            {resources.map((resource, index) => (
              <div 
                key={index} 
                className="group bg-white/90 backdrop-blur-sm p-8 rounded-2xl border-2 border-purple-200/50 hover:border-purple-400 hover:shadow-2xl hover:shadow-purple-500/30 transition-all duration-500 transform hover:-translate-y-3 cursor-pointer animate-fade-in-up relative overflow-hidden"
                style={{ animationDelay: `${index * 50}ms` }}
                onClick={() => resource.link !== '#' && navigate(resource.link)}
              >
                {/* Gradient overlay on hover */}
                <div className={`absolute inset-0 bg-gradient-to-br ${resource.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-500`}></div>
                
                <div className="relative z-10">
                  <div className={`w-16 h-16 bg-gradient-to-br ${resource.gradient} rounded-2xl flex items-center justify-center text-white mb-5 shadow-lg transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300`}>
                    {resource.icon}
                  </div>
                  <h3 className="text-2xl font-bold mb-3 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-pink-600 group-hover:bg-clip-text transition-all duration-300">{resource.title}</h3>
                  <p className="text-gray-600 mb-4 text-base line-clamp-2 min-h-[3rem]">{resource.description}</p>
                  <div className="flex items-center gap-2 text-purple-600 font-medium group-hover:text-pink-600 transition-colors">
                    {resource.link !== '#' ? (
                      <>
                        <span>Explore</span>
                        <ArrowRight className="w-5 h-5 group-hover:translate-x-2 transition-transform" />
                      </>
                    ) : (
                      <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">Coming Soon</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* CTA Section */}
          <div className="bg-gradient-to-br from-purple-600 via-pink-600 to-orange-500 rounded-2xl p-1 shadow-2xl animate-fade-in-up">
            <div className="bg-white/95 backdrop-blur-sm rounded-xl p-12 text-center">
              <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Still have questions?</h2>
              <p className="text-gray-600 text-lg mb-8 max-w-2xl mx-auto">Our support team is here to help you succeed. Get in touch with us anytime.</p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button 
                  className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-6 text-lg rounded-xl shadow-lg shadow-purple-500/30 transform hover:scale-105 transition-all duration-300"
                  onClick={() => navigate('/enterprise')}
                >
                  Contact Support
                </Button>
                <Button 
                  variant="outline" 
                  className="border-2 border-purple-300 hover:bg-purple-50 px-8 py-6 text-lg rounded-xl transform hover:scale-105 transition-all duration-300"
                  onClick={() => navigate('/dashboard')}
                >
                  Start Building
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Resources;