import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Check, Sparkles, Zap, Crown, Building2 } from 'lucide-react';

const Pricing = () => {
  const navigate = useNavigate();

  const plans = [
    {
      name: 'Free',
      price: '$0',
      period: '/month',
      description: 'Perfect for trying out BotSmith',
      icon: Sparkles,
      gradient: 'from-blue-400 to-cyan-400',
      features: [
        '1 chatbot',
        '100 messages/month',
        'Basic analytics',
        'Community support',
        'Standard AI models'
      ],
      cta: 'Start Free',
      ctaVariant: 'outline'
    },
    {
      name: 'Starter',
      price: '$150',
      period: '/month',
      description: 'For growing businesses',
      icon: Zap,
      gradient: 'from-pink-500 to-purple-500',
      popular: true,
      features: [
        '5 chatbots',
        '10,000 messages/month',
        'Advanced analytics',
        'Priority support',
        'Custom branding',
        'API access',
        'All AI models'
      ],
      cta: 'Get Started',
      ctaVariant: 'default'
    },
    {
      name: 'Professional',
      price: '$499',
      period: '/month',
      description: 'For large teams & high volume',
      icon: Crown,
      gradient: 'from-blue-600 to-indigo-600',
      features: [
        '25 chatbots',
        '100,000 messages/month',
        'Advanced analytics',
        '24/7 priority support',
        'Custom branding',
        'Full API access',
        'All AI models',
        'Custom integrations',
        'Dedicated account manager'
      ],
      cta: 'Get Started',
      ctaVariant: 'default'
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: '',
      description: 'Tailored solutions for your needs',
      icon: Building2,
      gradient: 'from-purple-600 to-pink-600',
      features: [
        'Unlimited chatbots',
        'Unlimited messages',
        'Custom analytics',
        'Dedicated 24/7 support',
        'White-label solution',
        'Custom AI model training',
        'On-premise deployment',
        'SLA guarantee',
        'Custom contracts',
        'Enterprise security'
      ],
      cta: 'Contact Sales',
      ctaVariant: 'default'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-blue-50 to-purple-50">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate('/')}>
            <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">B</span>
            </div>
            <span className="text-xl font-semibold">BotSmith</span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <button onClick={() => navigate('/pricing')} className="text-black font-medium">Pricing</button>
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

      <div className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="text-center mb-20">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-pink-500 to-blue-500 rounded-full text-white font-medium mb-6">
              <Sparkles className="w-4 h-4" />
              <span>Simple, Transparent Pricing</span>
            </div>
            <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-pink-600 via-purple-600 to-blue-600 bg-clip-text text-transparent">
              Choose Your Perfect Plan
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Start free and scale as you grow. No hidden fees, cancel anytime.
            </p>
          </div>

          {/* Pricing Cards */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {plans.map((plan, index) => {
              const Icon = plan.icon;
              return (
                <div 
                  key={index} 
                  className={`relative group ${
                    plan.popular ? 'lg:-mt-4 lg:mb-4' : ''
                  }`}
                >
                  {/* Popular Badge */}
                  {plan.popular && (
                    <div className="absolute -top-5 left-1/2 transform -translate-x-1/2 z-10">
                      <span className="bg-gradient-to-r from-pink-500 to-purple-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-lg">
                        ⭐ Most Popular
                      </span>
                    </div>
                  )}

                  {/* Card */}
                  <div className={`h-full bg-white rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-300 overflow-hidden ${
                    plan.popular ? 'ring-4 ring-purple-500 ring-opacity-50' : ''
                  }`}>
                    {/* Gradient Header */}
                    <div className={`bg-gradient-to-br ${plan.gradient} p-8 text-white`}>
                      <div className="flex items-center justify-between mb-4">
                        <Icon className="w-10 h-10" />
                        {plan.popular && (
                          <Sparkles className="w-6 h-6 animate-pulse" />
                        )}
                      </div>
                      <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                      <p className="text-white/90 text-sm mb-6">{plan.description}</p>
                      
                      <div className="mb-2">
                        <span className="text-5xl font-bold">{plan.price}</span>
                        {plan.period && (
                          <span className="text-white/80 text-lg">{plan.period}</span>
                        )}
                      </div>
                    </div>

                    {/* Features */}
                    <div className="p-8">
                      <ul className="space-y-4 mb-8">
                        {plan.features.map((feature, i) => (
                          <li key={i} className="flex items-start gap-3">
                            <div className={`mt-0.5 bg-gradient-to-r ${plan.gradient} rounded-full p-1`}>
                              <Check className="w-4 h-4 text-white" />
                            </div>
                            <span className="text-gray-700 text-sm">{feature}</span>
                          </li>
                        ))}
                      </ul>

                      {/* CTA Button */}
                      <Button 
                        className={`w-full py-6 rounded-xl font-semibold text-base transition-all duration-300 ${
                          plan.ctaVariant === 'default'
                            ? `bg-gradient-to-r ${plan.gradient} hover:shadow-lg hover:scale-105 text-white border-0`
                            : 'border-2 border-gray-300 hover:border-gray-400 bg-white text-gray-700 hover:bg-gray-50'
                        }`}
                        onClick={() => plan.name === 'Enterprise' ? navigate('/enterprise') : navigate('/dashboard')}
                      >
                        {plan.cta}
                      </Button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* FAQ or Additional Info */}
          <div className="mt-20 text-center">
            <div className="bg-white/80 backdrop-blur-sm rounded-3xl p-12 shadow-xl max-w-4xl mx-auto">
              <h2 className="text-3xl font-bold mb-6 bg-gradient-to-r from-pink-600 to-blue-600 bg-clip-text text-transparent">
                Need help choosing?
              </h2>
              <p className="text-gray-600 text-lg mb-8">
                Not sure which plan is right for you? Our team is here to help you find the perfect fit for your needs.
              </p>
              <div className="flex flex-wrap gap-4 justify-center">
                <Button 
                  className="bg-gradient-to-r from-pink-500 to-purple-500 hover:shadow-lg text-white rounded-xl px-8 py-6"
                  onClick={() => navigate('/enterprise')}
                >
                  Talk to Sales
                </Button>
                <Button 
                  variant="outline"
                  className="border-2 rounded-xl px-8 py-6"
                  onClick={() => navigate('/resources')}
                >
                  View Documentation
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Pricing;