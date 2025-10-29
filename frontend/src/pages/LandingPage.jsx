import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { MessageSquare, Zap, BarChart3, Globe, Shield, Sparkles, ChevronRight, Menu, X, Star, ArrowRight, Check } from 'lucide-react';
import Footer from '../components/Footer';

const LandingPage = () => {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [scrollY, setScrollY] = useState(0);
  const [particles, setParticles] = useState([]);

  // Generate floating particles
  useEffect(() => {
    const newParticles = Array.from({ length: 20 }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      top: Math.random() * 100,
      size: Math.random() * 8 + 4,
      duration: Math.random() * 20 + 15,
      delay: Math.random() * 5
    }));
    setParticles(newParticles);
  }, []);

  // Track mouse movement for parallax effect
  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({
        x: (e.clientX / window.innerWidth - 0.5) * 20,
        y: (e.clientY / window.innerHeight - 0.5) * 20
      });
    };

    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const features = [
    {
      icon: <MessageSquare className="w-6 h-6" />,
      title: 'Custom AI Agents',
      description: 'Train chatbots on your own content and data sources',
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: 'AI Actions',
      description: 'Execute real-world actions like bookings and payments',
      gradient: 'from-yellow-500 to-orange-500'
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: 'Smart Analytics',
      description: 'Monitor performance with actionable insights',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      icon: <Globe className="w-6 h-6" />,
      title: 'Multi-Channel',
      description: 'Deploy on website, Slack, WhatsApp, and more',
      gradient: 'from-green-500 to-emerald-500'
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: 'Enterprise Security',
      description: 'Built with robust encryption and compliance',
      gradient: 'from-red-500 to-rose-500'
    },
    {
      icon: <Sparkles className="w-6 h-6" />,
      title: 'No-Code Setup',
      description: 'Build and deploy without technical expertise',
      gradient: 'from-indigo-500 to-purple-500'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-purple-50 overflow-hidden relative">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-yellow-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-32 left-1/3 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-lg border-b border-gray-200/50 z-50 shadow-sm">
        <div className="max-w-[95%] mx-auto px-4 sm:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3 group cursor-pointer" onClick={() => navigate('/')}>
            {/* Premium 3D Logo */}
            <div className="relative">
              {/* Background glow effect */}
              <div className="absolute inset-0 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl blur-xl opacity-40 group-hover:opacity-60 transition-opacity duration-500"></div>
              
              {/* Main logo container */}
              <div className="relative w-12 h-12 bg-gradient-to-br from-purple-600 via-fuchsia-500 to-pink-600 rounded-2xl flex items-center justify-center transform group-hover:scale-105 group-hover:rotate-6 transition-all duration-500 shadow-2xl border border-white/20">
                {/* Inner gradient highlight */}
                <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-white/30 to-transparent opacity-50"></div>
                
                {/* Bot icon with 3D effect */}
                <svg className="w-7 h-7 text-white relative z-10 drop-shadow-lg" fill="currentColor" viewBox="0 0 24 24">
                  {/* Robot head */}
                  <path d="M12 2C11.45 2 11 2.45 11 3V4H7C5.89 4 5 4.89 5 6V18C5 19.11 5.89 20 7 20H17C18.11 20 19 19.11 19 18V6C19 4.89 18.11 4 17 4H13V3C13 2.45 12.55 2 12 2M7 6H17V18H7V6Z"/>
                  {/* Eyes */}
                  <circle cx="9" cy="10" r="1.5" className="animate-pulse"/>
                  <circle cx="15" cy="10" r="1.5" className="animate-pulse"/>
                  {/* Smile */}
                  <path d="M9 14C9 14 10 15.5 12 15.5S15 14 15 14" strokeWidth="1.5" stroke="currentColor" fill="none" strokeLinecap="round"/>
                  {/* Antenna */}
                  <circle cx="12" cy="3" r="1"/>
                </svg>
                
                {/* Sparkle effects */}
                <div className="absolute -top-1 -right-1 w-2 h-2 bg-yellow-300 rounded-full animate-ping"></div>
                <div className="absolute -bottom-1 -left-1 w-1.5 h-1.5 bg-cyan-300 rounded-full animate-ping" style={{animationDelay: '0.5s'}}></div>
              </div>
              
              {/* Animated orbital ring */}
              <div className="absolute inset-0 rounded-2xl border-2 border-purple-400/30 opacity-0 group-hover:opacity-100 group-hover:scale-125 transition-all duration-700 animate-pulse"></div>
            </div>
            
            {/* Premium Brand Typography */}
            <div className="flex flex-col -space-y-0.5">
              <div className="flex items-baseline gap-1">
                <span className="text-2xl sm:text-3xl font-black tracking-tight bg-gradient-to-r from-purple-700 via-fuchsia-600 to-pink-600 bg-clip-text text-transparent group-hover:from-purple-800 group-hover:via-fuchsia-700 group-hover:to-pink-700 transition-all duration-300 drop-shadow-sm">
                  BotSmith
                </span>
                <span className="text-[9px] font-bold text-purple-600 bg-purple-100 px-1.5 py-0.5 rounded-md">AI</span>
              </div>
              <span className="text-[10px] font-semibold text-gray-400 tracking-wider uppercase">
                Powered by Jyosha Solutions
              </span>
            </div>
          </div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            <button onClick={() => navigate('/pricing')} className="text-gray-700 hover:text-purple-600 transition-colors font-medium">Pricing</button>
            <button onClick={() => navigate('/enterprise')} className="text-gray-700 hover:text-purple-600 transition-colors font-medium">Scale Up</button>
            <button onClick={() => navigate('/resources')} className="text-gray-700 hover:text-purple-600 transition-colors font-medium">Learn</button>
          </div>
          
          {/* Desktop Action Buttons */}
          <div className="hidden sm:flex items-center gap-2 sm:gap-4">
            <Button variant="ghost" onClick={() => navigate('/signin')} className="hover:bg-purple-50 transition-colors text-sm sm:text-base px-2 sm:px-4">Sign in</Button>
            <Button className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-lg shadow-lg shadow-purple-500/30 transform hover:scale-105 transition-all duration-300 text-sm sm:text-base px-3 sm:px-4" onClick={() => navigate('/dashboard')}>
              Try for Free
            </Button>
          </div>
          
          {/* Mobile Menu Button */}
          <button 
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="sm:hidden p-2 text-gray-700 hover:text-purple-600 transition-colors"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
        
        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="sm:hidden bg-white border-t border-gray-200 shadow-lg animate-fade-in">
            <div className="px-4 py-4 space-y-3">
              <button onClick={() => { navigate('/pricing'); setMobileMenuOpen(false); }} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-purple-50 hover:text-purple-600 rounded-lg transition-colors font-medium">
                Pricing
              </button>
              <button onClick={() => { navigate('/enterprise'); setMobileMenuOpen(false); }} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-purple-50 hover:text-purple-600 rounded-lg transition-colors font-medium">
                Scale Up
              </button>
              <button onClick={() => { navigate('/resources'); setMobileMenuOpen(false); }} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-purple-50 hover:text-purple-600 rounded-lg transition-colors font-medium">
                Learn
              </button>
              <div className="pt-3 border-t border-gray-200 space-y-2">
                <Button variant="ghost" onClick={() => { navigate('/signin'); setMobileMenuOpen(false); }} className="w-full hover:bg-purple-50 transition-colors">
                  Sign in
                </Button>
                <Button className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-lg shadow-lg shadow-purple-500/30" onClick={() => { navigate('/dashboard'); setMobileMenuOpen(false); }}>
                  Try for Free
                </Button>
              </div>
            </div>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section className="pt-24 sm:pt-32 pb-12 sm:pb-20 px-4 sm:px-8 relative z-10">
        <div className="max-w-[95%] mx-auto grid md:grid-cols-2 gap-8 sm:gap-16 items-center">
          <div className="space-y-6 sm:space-y-8 animate-fade-in-up">
            <div className="inline-block">
              <span className="px-3 sm:px-4 py-2 rounded-full bg-purple-100 text-purple-700 text-xs sm:text-sm font-medium inline-flex items-center gap-2 animate-bounce-subtle">
                <Sparkles className="w-3 h-3 sm:w-4 sm:h-4" />
                AI-Powered Customer Support
              </span>
            </div>
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold leading-tight">
              <span className="bg-gradient-to-r from-gray-900 via-purple-900 to-pink-900 bg-clip-text text-transparent animate-gradient">
                AI that listens,<br />learns, and delights<br />every customer
              </span>
            </h1>
            <p className="text-base sm:text-lg md:text-xl text-gray-600 leading-relaxed">
              BotSmith helps you design and deploy smart AI agents that enhance customer support.
            </p>
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
              <Button 
                className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-6 text-lg rounded-xl shadow-2xl shadow-purple-500/30 transform hover:scale-105 transition-all duration-300 group"
                onClick={() => navigate('/dashboard')}
              >
                Build your agent
                <ChevronRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <span className="text-gray-500 flex items-center gap-2">
                <Shield className="w-4 h-4" />
                No credit card required
              </span>
            </div>
          </div>
          <div className="relative animate-fade-in-right">
            <div className="absolute -inset-4 bg-gradient-to-r from-purple-600 to-pink-600 rounded-3xl blur-2xl opacity-20 animate-pulse-slow"></div>
            <div className="relative w-full h-[500px] rounded-3xl bg-gradient-to-br from-pink-400 via-purple-400 to-orange-400 p-8 flex items-center justify-center transform hover:scale-105 transition-transform duration-500 shadow-2xl">
              <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-8 shadow-2xl w-full max-w-md transform hover:shadow-purple-500/20 transition-all duration-300">
                <h3 className="text-lg font-semibold mb-6 text-gray-900">Sources</h3>
                <button className="w-full border-2 border-dashed border-purple-300 rounded-xl p-8 hover:border-purple-500 hover:bg-purple-50 transition-all duration-300 flex items-center justify-center gap-3 group">
                  <div className="text-4xl group-hover:scale-125 transition-transform duration-300">▶</div>
                  <span className="text-gray-700 font-medium group-hover:text-purple-600 transition-colors">Add source</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-12 border-y border-gray-200 bg-white/50 backdrop-blur-sm relative z-10">
        <div className="max-w-[95%] mx-auto px-8">
          <p className="text-center text-gray-600 mb-8 animate-fade-in">
            Trusted by <span className="font-semibold text-transparent bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text">9000+</span> business worldwide
          </p>
          <div className="flex flex-wrap justify-center items-center gap-12 opacity-60 animate-fade-in-up animation-delay-300">
            <div className="text-2xl font-bold hover:opacity-100 transition-opacity cursor-pointer">SIEMENS</div>
            <div className="text-2xl font-bold hover:opacity-100 transition-opacity cursor-pointer">POSTMAN</div>
            <div className="text-2xl font-bold hover:opacity-100 transition-opacity cursor-pointer">ALPIAN</div>
            <div className="text-2xl font-bold hover:opacity-100 transition-opacity cursor-pointer">ONAL</div>
            <div className="text-2xl font-bold hover:opacity-100 transition-opacity cursor-pointer">ALBARAKA</div>
          </div>
        </div>
      </section>

      {/* Features Section - Streamlined Premium */}
      <section className="py-16 px-4 sm:px-8 relative z-10">
        <div className="max-w-6xl mx-auto relative z-10">
          {/* Header */}
          <div className="text-center mb-12 animate-fade-in-up">
            <h2 className="text-4xl sm:text-5xl font-bold mb-4 bg-gradient-to-r from-gray-900 via-purple-900 to-gray-900 bg-clip-text text-transparent">
              Build Smarter, Support Better, Grow Faster
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              A complete platform to craft, deploy and refine your AI-Powered agent ecosystem.
            </p>
          </div>

          {/* Feature Cards */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <div 
                key={index} 
                className="group relative animate-fade-in-up"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {/* Subtle Glow on Hover */}
                <div className="absolute -inset-px bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl opacity-0 group-hover:opacity-100 blur-lg transition-opacity duration-500"></div>
                
                {/* Card */}
                <div className="relative h-full bg-white rounded-2xl border border-gray-200 p-6 shadow-sm hover:shadow-lg transition-all duration-300 group-hover:border-purple-200 group-hover:translate-y-[-4px]">
                  {/* Icon */}
                  <div className={`w-14 h-14 bg-gradient-to-br ${feature.gradient} rounded-xl flex items-center justify-center text-white mb-4 transform group-hover:scale-105 transition-transform duration-300 shadow-md`}>
                    {feature.icon}
                  </div>

                  {/* Title */}
                  <h3 className="text-xl font-bold mb-2 text-gray-900 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-pink-600 group-hover:bg-clip-text transition-all duration-300">
                    {feature.title}
                  </h3>

                  {/* Description */}
                  <p className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* Bottom Trust Badge */}
          <div className="mt-12 text-center animate-fade-in-up">
            <div className="flex justify-center items-center gap-2">
              {[1, 2, 3, 4, 5].map((_, i) => (
                <Star key={i} className="w-5 h-5 fill-yellow-400 text-yellow-400" />
              ))}
              <span className="ml-2 text-gray-700 font-medium">4.9/5 from 9000+ customers</span>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-8 bg-gradient-to-br from-gray-900 via-purple-900 to-pink-900 text-white relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob"></div>
          <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000"></div>
        </div>
        <div className="max-w-[80%] mx-auto text-center relative z-10 animate-fade-in-up">
          <h2 className="text-5xl font-bold mb-6">Take your customer service to the next level.</h2>
          <p className="text-xl text-purple-200 mb-8">Let AI agents create seamless experiences that keep clients coming back</p>
          <Button 
            className="bg-white hover:bg-gray-100 text-purple-900 px-8 py-6 text-lg rounded-xl shadow-2xl transform hover:scale-105 transition-all duration-300 group"
            onClick={() => navigate('/signup')}
          >
            Get Started Free
            <ChevronRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Button>
        </div>
      </section>

      {/* Footer */}
      <Footer variant="landing" />
    </div>
  );
};

export default LandingPage;