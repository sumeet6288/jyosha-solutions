import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Check } from 'lucide-react';

const Pricing = () => {
  const navigate = useNavigate();

  const plans = [
    {
      name: 'Free',
      price: '$0',
      description: 'Perfect for trying out Chatbase',
      features: [
        '1 chatbot',
        '100 messages/month',
        'Basic analytics',
        'Community support'
      ]
    },
    {
      name: 'Pro',
      price: '$49',
      description: 'For growing businesses',
      popular: true,
      features: [
        '5 chatbots',
        '10,000 messages/month',
        'Advanced analytics',
        'Priority support',
        'Custom branding',
        'API access'
      ]
    },
    {
      name: 'Business',
      price: '$199',
      description: 'For large teams',
      features: [
        'Unlimited chatbots',
        'Unlimited messages',
        'Advanced analytics',
        '24/7 support',
        'Custom branding',
        'API access',
        'Custom integrations',
        'Dedicated account manager'
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate('/')}>
            <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">C</span>
            </div>
            <span className="text-xl font-semibold">Chatbase</span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <button onClick={() => navigate('/pricing')} className="text-black font-medium">Pricing</button>
            <button onClick={() => navigate('/enterprise')} className="text-gray-700 hover:text-black transition-colors">Enterprise</button>
            <button onClick={() => navigate('/resources')} className="text-gray-700 hover:text-black transition-colors">Resources</button>
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
            <h1 className="text-5xl font-bold mb-4">Simple, transparent pricing</h1>
            <p className="text-xl text-gray-600">Choose the plan that's right for your business</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {plans.map((plan, index) => (
              <div key={index} className={`p-8 rounded-2xl border-2 ${
                plan.popular ? 'border-black bg-gray-50' : 'border-gray-200'
              } hover:shadow-xl transition-all`}>
                {plan.popular && (
                  <span className="bg-black text-white px-3 py-1 rounded-full text-sm font-medium">Most Popular</span>
                )}
                <div className="mt-4">
                  <h3 className="text-2xl font-bold">{plan.name}</h3>
                  <div className="mt-4 mb-2">
                    <span className="text-5xl font-bold">{plan.price}</span>
                    <span className="text-gray-600">/month</span>
                  </div>
                  <p className="text-gray-600 mb-6">{plan.description}</p>
                  <Button 
                    className={`w-full ${
                      plan.popular ? 'bg-black hover:bg-gray-800 text-white' : 'border border-black hover:bg-gray-100'
                    }`}
                    onClick={() => navigate('/signup')}
                  >
                    Get Started
                  </Button>
                </div>
                <ul className="mt-8 space-y-4">
                  {plan.features.map((feature, i) => (
                    <li key={i} className="flex items-center gap-3">
                      <Check className="w-5 h-5 text-green-600" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Pricing;