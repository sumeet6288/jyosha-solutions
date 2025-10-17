import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { MessageSquare, Zap, BarChart3, Globe, Shield, Sparkles } from 'lucide-react';

const LandingPage = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <MessageSquare className="w-6 h-6" />,
      title: 'Custom AI Agents',
      description: 'Train chatbots on your own content and data sources'
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: 'AI Actions',
      description: 'Execute real-world actions like bookings and payments'
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: 'Smart Analytics',
      description: 'Monitor performance with actionable insights'
    },
    {
      icon: <Globe className="w-6 h-6" />,
      title: 'Multi-Channel',
      description: 'Deploy on website, Slack, WhatsApp, and more'
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: 'Enterprise Security',
      description: 'Built with robust encryption and compliance'
    },
    {
      icon: <Sparkles className="w-6 h-6" />,
      title: 'No-Code Setup',
      description: 'Build and deploy without technical expertise'
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">C</span>
            </div>
            <span className="text-xl font-semibold">Chatbase</span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <button onClick={() => navigate('/pricing')} className="text-gray-700 hover:text-black transition-colors">Pricing</button>
            <button onClick={() => navigate('/enterprise')} className="text-gray-700 hover:text-black transition-colors">Enterprise</button>
            <button onClick={() => navigate('/resources')} className="text-gray-700 hover:text-black transition-colors">Resources</button>
          </div>
          <div className="flex items-center gap-4">
            <Button variant="ghost" onClick={() => navigate('/signin')}>Sign in</Button>
            <Button className="bg-black hover:bg-gray-800 text-white rounded-lg" onClick={() => navigate('/dashboard')}>
              Try for Free
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h1 className="text-6xl font-bold leading-tight mb-6">
              AI agents for<br />magical customer<br />experiences
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Chatbase is the complete platform for building &<br />deploying AI support agents for your business.
            </p>
            <div className="flex items-center gap-4">
              <Button 
                className="bg-black hover:bg-gray-800 text-white px-8 py-6 text-lg rounded-lg"
                onClick={() => navigate('/dashboard')}
              >
                Build your agent
              </Button>
              <span className="text-gray-500 flex items-center gap-2">
                <Shield className="w-4 h-4" />
                No credit card required
              </span>
            </div>
          </div>
          <div className="relative">
            <div className="w-full h-[500px] rounded-3xl bg-gradient-to-br from-pink-400 via-purple-400 to-orange-400 p-8 flex items-center justify-center">
              <div className="bg-white rounded-2xl p-8 shadow-2xl w-full max-w-md">
                <h3 className="text-lg font-semibold mb-6">Sources</h3>
                <button className="w-full border-2 border-dashed border-gray-300 rounded-xl p-8 hover:border-gray-400 transition-colors flex items-center justify-center gap-3 group">
                  <div className="text-4xl group-hover:scale-110 transition-transform">▶</div>
                  <span className="text-gray-700 font-medium">Add source</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-12 border-t border-gray-200 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6">
          <p className="text-center text-gray-600 mb-8">
            Trusted by <span className="font-semibold text-black">9000+</span> business worldwide
          </p>
          <div className="flex flex-wrap justify-center items-center gap-12 opacity-60">
            <div className="text-2xl font-bold">SIEMENS</div>
            <div className="text-2xl font-bold">POSTMAN</div>
            <div className="text-2xl font-bold">ALPIAN</div>
            <div className="text-2xl font-bold">ONAL</div>
            <div className="text-2xl font-bold">ALBARAKA</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold mb-6">Everything you need to delight customers</h2>
            <p className="text-xl text-gray-600">Powerful features to build, deploy, and optimize your AI agents</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="p-8 rounded-2xl border border-gray-200 hover:border-gray-300 hover:shadow-lg transition-all">
                <div className="w-12 h-12 bg-black rounded-xl flex items-center justify-center text-white mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-6 bg-black text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-5xl font-bold mb-6">Ready to transform your customer experience?</h2>
          <p className="text-xl text-gray-300 mb-8">Join thousands of businesses using AI agents to deliver magical customer experiences</p>
          <Button 
            className="bg-white hover:bg-gray-100 text-black px-8 py-6 text-lg rounded-lg"
            onClick={() => navigate('/signup')}
          >
            Get Started Free
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-gray-200">
        <div className="max-w-7xl mx-auto text-center text-gray-600">
          <p>&copy; 2025 Chatbase. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
