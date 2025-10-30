import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { MessageSquare, Zap, BarChart3, Globe, Shield, Sparkles, ChevronRight, Menu, X, Star, ArrowRight, Check, Upload, Brain, Palette, Rocket, ShoppingCart, GraduationCap, Heart, Briefcase, Users, TrendingUp, Clock, Award } from 'lucide-react';
import Footer from '../components/Footer';
import { useScrollAnimation } from '../hooks/useScrollAnimation';

const LandingPage = () => {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [particles, setParticles] = useState([]);

  // Scroll animation hooks for different sections
  const [featuresRef, featuresVisible] = useScrollAnimation({ threshold: 0.1 });
  const [howItWorksRef, howItWorksVisible] = useScrollAnimation({ threshold: 0.1 });
  const [useCasesRef, useCasesVisible] = useScrollAnimation({ threshold: 0.1 });
  const [differentiatorsRef, differentiatorsVisible] = useScrollAnimation({ threshold: 0.1 });
  const [testimonialsRef, testimonialsVisible] = useScrollAnimation({ threshold: 0.1 });

  // Scroll to top on mount to fix reload issue
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  // Generate optimized floating particles (reduced from 20 to 10)
  useEffect(() => {
    const newParticles = Array.from({ length: 10 }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      top: Math.random() * 100,
      size: Math.random() * 8 + 4,
      duration: Math.random() * 20 + 15,
      delay: Math.random() * 5
    }));
    setParticles(newParticles);
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

  const howItWorksSteps = [
    {
      step: '01',
      icon: <Upload className="w-8 h-8" />,
      title: 'Connect Your Data',
      description: 'Upload documents, add websites, or paste text content. Support for PDF, DOCX, TXT, and more.',
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      step: '02',
      icon: <Brain className="w-8 h-8" />,
      title: 'Train Your AI',
      description: 'Our intelligent system automatically processes and learns from your content using advanced RAG technology.',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      step: '03',
      icon: <Palette className="w-8 h-8" />,
      title: 'Customize & Brand',
      description: 'Choose colors, upload your logo, set personality, and configure widget appearance to match your brand.',
      gradient: 'from-orange-500 to-rose-500'
    },
    {
      step: '04',
      icon: <Rocket className="w-8 h-8" />,
      title: 'Deploy Anywhere',
      description: 'Get embed code for your website or share a public chat link. Go live in minutes, not weeks.',
      gradient: 'from-green-500 to-emerald-500'
    }
  ];

  const useCases = [
    {
      icon: <ShoppingCart className="w-8 h-8" />,
      title: 'E-commerce Support',
      description: 'Handle orders, track shipments, and manage returns 24/7',
      stats: '3x faster resolution',
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      icon: <Briefcase className="w-8 h-8" />,
      title: 'SaaS Onboarding',
      description: 'Guide new users through features and answer product questions',
      stats: '60% less support tickets',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      icon: <Heart className="w-8 h-8" />,
      title: 'Healthcare FAQ',
      description: 'Answer patient questions about services, hours, and procedures',
      stats: '85% satisfaction rate',
      gradient: 'from-rose-500 to-red-500'
    },
    {
      icon: <GraduationCap className="w-8 h-8" />,
      title: 'Education Assistant',
      description: 'Help students with course materials, assignments, and schedules',
      stats: '24/7 availability',
      gradient: 'from-green-500 to-emerald-500'
    }
  ];

  const differentiators = [
    {
      icon: <Users className="w-8 h-8" />,
      title: 'Multi-AI Provider',
      description: 'Choose from GPT-4o, Claude 3.5 Sonnet, or Gemini 2.0 Flash for your chatbot',
      gradient: 'from-purple-600 to-pink-600'
    },
    {
      icon: <Brain className="w-8 h-8" />,
      title: 'Knowledge Base RAG',
      description: 'AI answers from YOUR data, not generic training. Accurate and contextual responses',
      gradient: 'from-blue-600 to-cyan-600'
    },
    {
      icon: <Sparkles className="w-8 h-8" />,
      title: 'No-Code Builder',
      description: 'Beautiful drag-and-drop interface. Zero coding required, maximum customization',
      gradient: 'from-orange-600 to-rose-600'
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: 'Real-Time Analytics',
      description: 'Track conversations, satisfaction scores, peak hours, and response times instantly',
      gradient: 'from-green-600 to-emerald-600'
    }
  ];

  const testimonials = [
    {
      name: 'Sarah Chen',
      role: 'CEO, TechFlow',
      avatar: '👩‍💼',
      rating: 5,
      text: 'BotSmith reduced our support tickets by 60% in the first month. The AI understands our products perfectly!',
      company: 'SaaS Company'
    },
    {
      name: 'Michael Rodriguez',
      role: 'Customer Success Manager',
      avatar: '👨‍💻',
      rating: 5,
      text: 'The multi-provider AI support is game-changing. We can switch between GPT-4 and Claude based on our needs.',
      company: 'E-commerce Platform'
    },
    {
      name: 'Emily Watson',
      role: 'Operations Director',
      avatar: '👩‍🔬',
      rating: 5,
      text: 'Setup took 15 minutes. Our patients love the instant responses. This is the future of healthcare communication.',
      company: 'Healthcare Provider'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-purple-50 overflow-hidden relative">
      {/* Advanced Animated background with glassmorphism - Lower z-index */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none z-0" style={{ willChange: 'transform' }}>
        {/* Main gradient blobs */}
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob" style={{ transform: 'translateZ(0)' }}></div>
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-yellow-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000" style={{ transform: 'translateZ(0)' }}></div>
        <div className="absolute -bottom-32 left-1/3 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000" style={{ transform: 'translateZ(0)' }}></div>
        
        {/* Secondary animated layers */}
        <div className="absolute top-1/4 right-1/3 w-64 h-64 bg-cyan-200 rounded-full mix-blend-multiply filter blur-3xl opacity-15 animate-blob animation-delay-1000" style={{ transform: 'translateZ(0)' }}></div>
        <div className="absolute bottom-1/4 left-1/4 w-80 h-80 bg-rose-200 rounded-full mix-blend-multiply filter blur-3xl opacity-15 animate-blob animation-delay-3000" style={{ transform: 'translateZ(0)' }}></div>
        
        {/* Geometric floating shapes */}
        <div className="absolute top-20 right-20 w-32 h-32 bg-gradient-to-br from-purple-400/20 to-pink-400/20 rounded-3xl rotate-45 animate-float-rotate blur-sm"></div>
        <div className="absolute bottom-40 left-32 w-24 h-24 bg-gradient-to-br from-blue-400/20 to-cyan-400/20 rounded-2xl rotate-12 animate-float-rotate animation-delay-2000 blur-sm"></div>
        <div className="absolute top-1/2 right-1/4 w-40 h-40 bg-gradient-to-br from-orange-400/15 to-rose-400/15 rounded-full animate-float animation-delay-1000 blur-md"></div>
        
        {/* Animated gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 via-transparent to-pink-500/5 animate-gradient-xy opacity-50"></div>
        
        {/* Premium floating particles with glassmorphism */}
        {particles.map((particle) => (
          <div
            key={particle.id}
            className="absolute rounded-full bg-gradient-to-br from-purple-400 to-pink-400 opacity-20 glass"
            style={{
              left: `${particle.left}%`,
              top: `${particle.top}%`,
              width: `${particle.size}px`,
              height: `${particle.size}px`,
              animation: `float ${particle.duration}s ease-in-out infinite`,
              animationDelay: `${particle.delay}s`,
              transform: 'translateZ(0)',
              willChange: 'transform'
            }}
          />
        ))}
        
        {/* Grid pattern overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(139,92,246,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(139,92,246,0.03)_1px,transparent_1px)] bg-[size:50px_50px] [mask-image:radial-gradient(ellipse_at_center,black_20%,transparent_80%)]"></div>
      </div>

      {/* Navigation with Glassmorphism - Highest z-index */}
      <nav className="fixed top-0 left-0 right-0 glass-strong backdrop-blur-xl border-b border-white/30 z-[100] shadow-lg shadow-purple-500/10">
        <div className="max-w-[95%] mx-auto px-4 sm:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3 group cursor-pointer" onClick={() => navigate('/')}>
            {/* Premium 3D Logo with glow animation */}
            <div className="relative transform-3d">
              {/* Background glow effect with animation */}
              <div className="absolute inset-0 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl blur-xl opacity-40 group-hover:opacity-60 animate-glow-pulse"></div>
              
              {/* Main logo container */}
              <div className="relative w-12 h-12 bg-gradient-to-br from-purple-600 via-fuchsia-500 to-pink-600 rounded-2xl flex items-center justify-center transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-500 shadow-2xl border border-white/20 animate-gradient-xy">
                {/* Inner gradient highlight */}
                <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-white/30 to-transparent opacity-50"></div>
                
                {/* Bot icon with 3D effect */}
                <svg className="w-7 h-7 text-white relative z-10 drop-shadow-lg group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 24 24">
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
                
                {/* Sparkle effects with animation */}
                <div className="absolute -top-1 -right-1 w-2 h-2 bg-yellow-300 rounded-full animate-ping"></div>
                <div className="absolute -bottom-1 -left-1 w-1.5 h-1.5 bg-cyan-300 rounded-full animate-ping" style={{animationDelay: '0.5s'}}></div>
              </div>
              
              {/* Animated orbital ring */}
              <div className="absolute inset-0 rounded-2xl border-2 border-purple-400/30 opacity-0 group-hover:opacity-100 group-hover:scale-125 transition-all duration-700 animate-rotate-slow"></div>
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
            <Button className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-lg shadow-lg shadow-purple-500/30 transform hover:scale-105 transition-all duration-300 text-sm sm:text-base px-3 sm:px-4" onClick={() => navigate('/signup')}>
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
                <Button className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-lg shadow-lg shadow-purple-500/30" onClick={() => { navigate('/signup'); setMobileMenuOpen(false); }}>
                  Try for Free
                </Button>
              </div>
            </div>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section className="pt-32 sm:pt-40 pb-12 sm:pb-20 px-4 sm:px-8 relative z-10">
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
            {/* Optimized glow with GPU acceleration */}
            <div className="absolute -inset-4 bg-gradient-to-r from-purple-600 to-pink-600 rounded-3xl blur-2xl opacity-20 animate-pulse-slow" style={{ transform: 'translateZ(0)', willChange: 'opacity' }}></div>
            
            {/* Main card with enhanced styling and performance optimization - Now fully clickable */}
            <div 
              onClick={() => navigate('/dashboard')}
              className="relative w-full h-[500px] rounded-3xl bg-gradient-to-br from-pink-400 via-purple-400 to-orange-400 p-8 flex items-center justify-center transform hover:scale-105 transition-transform duration-500 shadow-2xl cursor-pointer" 
              style={{ transform: 'translateZ(0)', willChange: 'transform' }}
            >
              {/* Shine effect overlay */}
              <div className="absolute inset-0 rounded-3xl bg-gradient-to-tr from-white/20 via-transparent to-transparent opacity-40 pointer-events-none"></div>
              <div className="absolute inset-0 rounded-3xl overflow-hidden pointer-events-none">
                <div className="absolute top-0 left-0 right-0 h-1/2 bg-gradient-to-b from-white/10 to-transparent"></div>
              </div>
              
              {/* Optimized floating decorative elements */}
              <div className="absolute top-8 right-8 w-4 h-4 bg-white/30 rounded-full animate-ping pointer-events-none" style={{ transform: 'translateZ(0)' }}></div>
              <div className="absolute bottom-12 left-12 w-3 h-3 bg-yellow-300/40 rounded-full animate-ping animation-delay-1000 pointer-events-none" style={{ transform: 'translateZ(0)' }}></div>
              
              <div className="relative bg-white/95 backdrop-blur-sm rounded-2xl p-8 shadow-2xl w-full max-w-md transform hover:shadow-purple-500/20 transition-all duration-300 border border-white/50 pointer-events-none">
                {/* Inner card glow */}
                <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-purple-500/5 to-pink-500/5"></div>
                
                <div className="relative">
                  <h3 className="text-lg font-semibold mb-6 text-gray-900 flex items-center gap-2">
                    <span className="w-2 h-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full animate-pulse"></span>
                    Sources
                  </h3>
                  <div className="w-full border-2 border-dashed border-purple-300 rounded-xl p-8 hover:border-purple-500 hover:bg-purple-50 transition-all duration-300 flex items-center justify-center gap-3 group relative overflow-hidden">
                    {/* Optimized button hover effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-purple-500/0 via-purple-500/5 to-purple-500/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" style={{ transform: 'translateZ(0)' }}></div>
                    <div className="text-4xl group-hover:scale-125 transition-transform duration-300 relative z-10">▶</div>
                    <span className="text-gray-700 font-medium group-hover:text-purple-600 transition-colors relative z-10">Add source</span>
                  </div>
                </div>
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
      <section className="py-16 px-4 sm:px-8 relative z-10" ref={featuresRef}>
        <div className="max-w-6xl mx-auto relative z-10">
          {/* Header */}
          <div className={`text-center mb-12 transition-all duration-800 ${featuresVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}>
            <h2 className="text-4xl sm:text-5xl font-bold mb-4 bg-gradient-to-r from-gray-900 via-purple-900 to-gray-900 bg-clip-text text-transparent">
              Build Smarter, Support Better, Grow Faster
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              A complete platform to craft, deploy and refine your AI-Powered agent ecosystem.
            </p>
          </div>

          {/* Feature Cards with Glassmorphism and Scroll Animation */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <div 
                key={index} 
                className={`group relative transform-3d transition-all duration-700 ${
                  featuresVisible 
                    ? 'opacity-100 translate-y-0' 
                    : 'opacity-0 translate-y-16'
                }`}
                style={{ 
                  transitionDelay: featuresVisible ? `${index * 100}ms` : '0ms'
                }}
              >
                {/* Animated Glow on Hover */}
                <div className="absolute -inset-px bg-gradient-to-r from-purple-500 via-pink-500 to-purple-500 rounded-2xl opacity-0 group-hover:opacity-100 blur-lg transition-opacity duration-500 animate-gradient-x"></div>
                
                {/* Card with Glassmorphism */}
                <div className="relative h-full glass-card rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-500 group-hover:translate-y-[-8px] hover-3d overflow-hidden">
                  {/* Animated background shine */}
                  <div className="absolute inset-0 bg-gradient-to-br from-white/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  
                  {/* Animated corner accent */}
                  <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-purple-500/10 to-pink-500/10 rounded-bl-full opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  
                  {/* Icon with 3D animation */}
                  <div className={`relative w-14 h-14 bg-gradient-to-br ${feature.gradient} rounded-xl flex items-center justify-center text-white mb-4 transform group-hover:scale-110 group-hover:rotate-12 transition-all duration-500 shadow-lg group-hover:shadow-2xl animate-glow-pulse`}>
                    <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-white/30 to-transparent"></div>
                    <div className="relative z-10">{feature.icon}</div>
                  </div>

                  {/* Title with gradient on hover */}
                  <h3 className="relative text-xl font-bold mb-2 text-gray-900 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-pink-600 group-hover:bg-clip-text transition-all duration-300 z-10">
                    {feature.title}
                  </h3>

                  {/* Description */}
                  <p className="relative text-gray-600 leading-relaxed z-10">
                    {feature.description}
                  </p>
                  
                  {/* Hover indicator */}
                  <div className="absolute bottom-4 right-4 w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 shadow-lg">
                    <ChevronRight className="w-4 h-4 text-white" />
                  </div>
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

      {/* How It Works Section */}
      <section className="py-20 px-4 sm:px-8 bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50 relative overflow-hidden" ref={howItWorksRef}>
        {/* Background decoration */}
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-20 left-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl animate-blob"></div>
          <div className="absolute bottom-20 right-10 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000"></div>
        </div>

        <div className="max-w-6xl mx-auto relative z-10">
          {/* Header */}
          <div className={`text-center mb-16 transition-all duration-800 ${howItWorksVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}>
            <span className="px-4 py-2 rounded-full bg-purple-100 text-purple-700 text-sm font-medium inline-flex items-center gap-2 mb-4">
              <Clock className="w-4 h-4" />
              Launch in Minutes
            </span>
            <h2 className="text-4xl sm:text-5xl font-bold mb-4 bg-gradient-to-r from-purple-900 via-pink-900 to-orange-900 bg-clip-text text-transparent">
              How It Works
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Four simple steps to transform your customer support with AI
            </p>
          </div>

          {/* Steps with Premium Glassmorphism and Scroll Animation */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {howItWorksSteps.map((step, index) => (
              <div 
                key={index}
                className={`relative group transform-3d transition-all duration-800 ${
                  howItWorksVisible 
                    ? 'opacity-100 translate-y-0' 
                    : 'opacity-0 translate-y-20'
                }`}
                style={{ 
                  transitionDelay: howItWorksVisible ? `${index * 150}ms` : '0ms'
                }}
              >
                {/* Connecting Arrow with glow (hidden on last item and mobile) */}
                {index < howItWorksSteps.length - 1 && (
                  <div className="hidden lg:block absolute top-16 -right-4 z-10">
                    <div className="relative">
                      <div className="absolute inset-0 blur-md bg-purple-500/50 rounded-full"></div>
                      <ArrowRight className="relative w-8 h-8 text-purple-400 group-hover:text-purple-600 transition-colors animate-bounce-subtle" />
                    </div>
                  </div>
                )}

                {/* Card with Advanced Glassmorphism */}
                <div className="relative glass-strong rounded-2xl p-6 shadow-xl hover:shadow-2xl transition-all duration-500 hover:translate-y-[-8px] hover-3d overflow-hidden group">
                  {/* Animated gradient background */}
                  <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 via-pink-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 animate-gradient-xy"></div>
                  
                  {/* Glowing border effect */}
                  <div className="absolute -inset-[1px] bg-gradient-to-r from-purple-500 via-pink-500 to-purple-500 rounded-2xl opacity-20 group-hover:opacity-40 blur-sm transition-opacity duration-500 animate-gradient-x"></div>
                  
                  {/* Step Number with 3D effect */}
                  <div className="absolute -top-4 -left-4 w-12 h-12 bg-gradient-to-br from-purple-600 to-pink-600 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-2xl transform group-hover:scale-110 group-hover:rotate-12 transition-all duration-500 z-10 animate-gradient-xy">
                    <div className="absolute inset-0 rounded-full bg-gradient-to-br from-white/30 to-transparent"></div>
                    <span className="relative z-10">{step.step}</span>
                  </div>

                  {/* Icon with enhanced animation */}
                  <div className={`relative w-16 h-16 bg-gradient-to-br ${step.gradient} rounded-xl flex items-center justify-center text-white mb-4 mt-2 transform group-hover:scale-125 group-hover:rotate-12 transition-all duration-500 shadow-xl z-10 animate-glow-pulse`}>
                    <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-white/40 to-transparent"></div>
                    <div className="relative z-10 transform group-hover:scale-110 transition-transform">{step.icon}</div>
                  </div>

                  {/* Content */}
                  <h3 className="relative text-xl font-bold mb-2 text-gray-900 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-pink-600 group-hover:bg-clip-text transition-all duration-300 z-10">
                    {step.title}
                  </h3>
                  <p className="relative text-gray-600 leading-relaxed text-sm z-10">
                    {step.description}
                  </p>
                  
                  {/* Floating particles in card */}
                  <div className="absolute top-2 right-2 w-2 h-2 bg-purple-400 rounded-full opacity-50 group-hover:opacity-100 animate-bounce-rotate"></div>
                  <div className="absolute bottom-4 left-4 w-1.5 h-1.5 bg-pink-400 rounded-full opacity-50 group-hover:opacity-100 animate-bounce-rotate animation-delay-1000"></div>
                </div>
              </div>
            ))}
          </div>

          {/* Bottom CTA */}
          <div className="text-center mt-12 animate-fade-in-up">
            <Button 
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-6 text-lg rounded-xl shadow-xl transform hover:scale-105 transition-all duration-300 group"
              onClick={() => navigate('/dashboard')}
            >
              Start Building Now
              <Rocket className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="py-20 px-4 sm:px-8 relative z-10 bg-white" ref={useCasesRef}>
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className={`text-center mb-16 transition-all duration-800 ${useCasesVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}>
            <span className="px-4 py-2 rounded-full bg-green-100 text-green-700 text-sm font-medium inline-flex items-center gap-2 mb-4">
              <Award className="w-4 h-4" />
              Trusted Across Industries
            </span>
            <h2 className="text-4xl sm:text-5xl font-bold mb-4 bg-gradient-to-r from-gray-900 via-purple-900 to-gray-900 bg-clip-text text-transparent">
              Built for Every Business
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              From startups to enterprises, see how teams use BotSmith to revolutionize customer experience
            </p>
          </div>

          {/* Use Case Cards with Glassmorphism and Scroll Animation */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {useCases.map((useCase, index) => (
              <div 
                key={index}
                className={`group relative transform-3d transition-all duration-800 ${
                  useCasesVisible 
                    ? 'opacity-100 translate-y-0' 
                    : 'opacity-0 translate-y-20'
                }`}
                style={{ 
                  transitionDelay: useCasesVisible ? `${index * 100}ms` : '0ms'
                }}
              >
                {/* Animated Glow Effect */}
                <div className="absolute -inset-px bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl opacity-0 group-hover:opacity-100 blur-lg transition-opacity duration-500 animate-gradient-x"></div>
                
                {/* Card with Premium Glassmorphism */}
                <div className="relative h-full glass-card rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-500 group-hover:translate-y-[-8px] hover-3d overflow-hidden">
                  {/* Animated gradient overlay */}
                  <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 via-pink-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 animate-gradient-xy"></div>
                  
                  {/* Icon with 3D effect and glow */}
                  <div className={`relative w-16 h-16 bg-gradient-to-br ${useCase.gradient} rounded-2xl flex items-center justify-center text-white mb-4 transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-500 shadow-xl animate-glow-pulse z-10`}>
                    <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-white/30 to-transparent"></div>
                    <div className="relative z-10 transform group-hover:scale-110 transition-transform">{useCase.icon}</div>
                  </div>

                  {/* Title */}
                  <h3 className="relative text-xl font-bold mb-2 text-gray-900 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-pink-600 group-hover:bg-clip-text transition-all duration-300 z-10">
                    {useCase.title}
                  </h3>

                  {/* Description */}
                  <p className="relative text-gray-600 leading-relaxed text-sm mb-4 z-10">
                    {useCase.description}
                  </p>

                  {/* Stats Badge with glassmorphism */}
                  <div className="relative inline-flex items-center gap-2 px-3 py-1 glass rounded-full text-xs font-semibold text-purple-700 z-10 group-hover:scale-105 transition-transform">
                    <TrendingUp className="w-3 h-3 animate-bounce-subtle" />
                    {useCase.stats}
                  </div>
                  
                  {/* Decorative element */}
                  <div className="absolute bottom-0 right-0 w-24 h-24 bg-gradient-to-tl from-purple-500/10 to-transparent rounded-tl-full opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* What Makes Us Different Section */}
      <section className="py-20 px-4 sm:px-8 bg-gradient-to-br from-gray-50 to-purple-50 relative overflow-hidden" ref={differentiatorsRef}>
        {/* Background Elements */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-0 right-0 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl animate-pulse-slow"></div>
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl animate-pulse-slow animation-delay-2000"></div>
        </div>

        <div className="max-w-6xl mx-auto relative z-10">
          {/* Header */}
          <div className={`text-center mb-16 transition-all duration-800 ${differentiatorsVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}>
            <span className="px-4 py-2 rounded-full bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 text-sm font-medium inline-flex items-center gap-2 mb-4">
              <Sparkles className="w-4 h-4" />
              Why Choose BotSmith
            </span>
            <h2 className="text-4xl sm:text-5xl font-bold mb-4 bg-gradient-to-r from-purple-900 via-pink-900 to-purple-900 bg-clip-text text-transparent">
              What Makes Us Different
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Powerful features that set us apart from traditional chatbot builders
            </p>
          </div>

          {/* Differentiator Cards with Advanced Effects and Scroll Animation */}
          <div className="grid md:grid-cols-2 gap-8">
            {differentiators.map((item, index) => (
              <div 
                key={index}
                className={`group relative transform-3d transition-all duration-800 ${
                  differentiatorsVisible 
                    ? 'opacity-100 translate-y-0' 
                    : 'opacity-0 translate-y-20'
                }`}
                style={{ 
                  transitionDelay: differentiatorsVisible ? `${index * 150}ms` : '0ms'
                }}
              >
                {/* Animated Border Gradient with stronger effect */}
                <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 via-pink-600 to-purple-600 rounded-2xl opacity-30 group-hover:opacity-100 blur-md transition-all duration-500 animate-gradient-x"></div>
                
                {/* Card with Premium Glassmorphism */}
                <div className="relative glass-strong rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-all duration-500 hover:translate-y-[-8px] hover-3d overflow-hidden">
                  {/* Animated background pattern */}
                  <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 via-pink-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 animate-gradient-xy"></div>
                  
                  {/* Glowing grid pattern */}
                  <div className="absolute inset-0 bg-[linear-gradient(rgba(139,92,246,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(139,92,246,0.1)_1px,transparent_1px)] bg-[size:20px_20px] opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  
                  <div className="relative flex items-start gap-4 z-10">
                    {/* Icon with 3D effect */}
                    <div className={`flex-shrink-0 w-16 h-16 bg-gradient-to-br ${item.gradient} rounded-xl flex items-center justify-center text-white transform group-hover:scale-125 group-hover:rotate-12 transition-all duration-500 shadow-2xl animate-glow-pulse`}>
                      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-white/40 to-transparent"></div>
                      <div className="relative z-10 transform group-hover:scale-110 transition-transform">{item.icon}</div>
                    </div>

                    {/* Content */}
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold mb-3 text-gray-900 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-pink-600 group-hover:bg-clip-text transition-all duration-300">
                        {item.title}
                      </h3>
                      <p className="text-gray-600 leading-relaxed mb-4">
                        {item.description}
                      </p>
                      
                      {/* Check Icon with glassmorphism */}
                      <div className="flex items-center gap-2 glass text-green-600 px-3 py-1.5 rounded-full inline-flex group-hover:scale-105 transition-transform">
                        <Check className="w-5 h-5 animate-bounce-subtle" />
                        <span className="text-sm font-semibold">Available Now</span>
                      </div>
                    </div>
                  </div>
                  
                  {/* Decorative floating elements */}
                  <div className="absolute top-4 right-4 w-3 h-3 bg-purple-400 rounded-full opacity-50 group-hover:opacity-100 animate-float-rotate"></div>
                  <div className="absolute bottom-6 right-8 w-2 h-2 bg-pink-400 rounded-full opacity-50 group-hover:opacity-100 animate-float-rotate animation-delay-1000"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 px-4 sm:px-8 bg-white relative z-10" ref={testimonialsRef}>
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className={`text-center mb-16 transition-all duration-800 ${testimonialsVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}>
            <span className="px-4 py-2 rounded-full bg-yellow-100 text-yellow-700 text-sm font-medium inline-flex items-center gap-2 mb-4">
              <Star className="w-4 h-4 fill-yellow-700" />
              Loved by Teams Worldwide
            </span>
            <h2 className="text-4xl sm:text-5xl font-bold mb-4 bg-gradient-to-r from-gray-900 via-purple-900 to-gray-900 bg-clip-text text-transparent">
              What Our Customers Say
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Join thousands of happy customers who transformed their support with BotSmith
            </p>
          </div>

          {/* Testimonial Cards with Glassmorphism and Scroll Animation */}
          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div 
                key={index}
                className={`group relative transform-3d transition-all duration-800 ${
                  testimonialsVisible 
                    ? 'opacity-100 translate-y-0' 
                    : 'opacity-0 translate-y-20'
                }`}
                style={{ 
                  transitionDelay: testimonialsVisible ? `${index * 150}ms` : '0ms'
                }}
              >
                {/* Animated glow border */}
                <div className="absolute -inset-[2px] bg-gradient-to-r from-purple-500 via-pink-500 to-purple-500 rounded-2xl opacity-0 group-hover:opacity-100 blur-sm transition-all duration-500 animate-gradient-x"></div>
                
                {/* Card with Premium Glassmorphism */}
                <div className="relative h-full glass-strong rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-all duration-500 hover:translate-y-[-8px] hover-3d overflow-hidden">
                  {/* Animated background */}
                  <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 via-pink-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 animate-gradient-xy"></div>
                  
                  {/* Quote Mark with glow */}
                  <div className="absolute top-6 right-6 text-6xl text-purple-300 font-serif opacity-50 group-hover:opacity-100 group-hover:scale-110 transition-all duration-500">"</div>
                  
                  {/* Stars with animation */}
                  <div className="relative flex gap-1 mb-4 z-10">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star 
                        key={i} 
                        className="w-5 h-5 fill-yellow-400 text-yellow-400 animate-bounce-subtle" 
                        style={{ animationDelay: `${i * 100}ms` }}
                      />
                    ))}
                  </div>

                  {/* Testimonial Text */}
                  <p className="relative text-gray-700 leading-relaxed mb-6 z-10 italic font-medium">
                    {testimonial.text}
                  </p>

                  {/* Author with glassmorphism */}
                  <div className="relative flex items-center gap-4 pt-4 border-t border-purple-200/50 z-10">
                    <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center text-2xl shadow-lg transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-500 animate-glow-pulse">
                      <div className="absolute inset-0 rounded-full bg-gradient-to-br from-white/30 to-transparent"></div>
                      <span className="relative z-10">{testimonial.avatar}</span>
                    </div>
                    <div>
                      <h4 className="font-bold text-gray-900 group-hover:text-purple-600 transition-colors">{testimonial.name}</h4>
                      <p className="text-sm text-gray-600">{testimonial.role}</p>
                      <p className="text-xs text-purple-600 font-semibold">{testimonial.company}</p>
                    </div>
                  </div>
                  
                  {/* Decorative particles */}
                  <div className="absolute top-1/4 left-4 w-2 h-2 bg-purple-400 rounded-full opacity-50 group-hover:opacity-100 animate-float-rotate"></div>
                  <div className="absolute bottom-1/3 right-6 w-1.5 h-1.5 bg-pink-400 rounded-full opacity-50 group-hover:opacity-100 animate-float-rotate animation-delay-1000"></div>
                </div>
              </div>
            ))}
          </div>

          {/* Bottom Stats with Scroll Animation */}
          <div className={`mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 text-center transition-all duration-800 ${
            testimonialsVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'
          }`}
          style={{ transitionDelay: testimonialsVisible ? '500ms' : '0ms' }}
          >
            <div>
              <div className="text-4xl font-bold text-transparent bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text mb-2">9000+</div>
              <div className="text-gray-600 font-medium">Happy Customers</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-transparent bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text mb-2">500K+</div>
              <div className="text-gray-600 font-medium">Conversations/Day</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-transparent bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text mb-2">98%</div>
              <div className="text-gray-600 font-medium">Uptime</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-transparent bg-gradient-to-r from-orange-600 to-rose-600 bg-clip-text mb-2">4.9/5</div>
              <div className="text-gray-600 font-medium">Customer Rating</div>
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