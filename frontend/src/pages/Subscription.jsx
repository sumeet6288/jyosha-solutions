import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import { 
  Sparkles, Zap, Crown, Check, ArrowRight, 
  TrendingUp, AlertCircle, Loader2, CreditCard, CheckCircle, Building2, ArrowLeft
} from 'lucide-react';
import { Button } from '../components/ui/button';
import Footer from '../components/Footer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const SubscriptionNew = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [subscriptionStatus, setSubscriptionStatus] = useState(null);
  const [checkingOut, setCheckingOut] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);

  // Define plans matching the Pricing page
  const plans = [
    {
      id: 'free',
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
      cta: 'Current Plan',
      isFree: true
    },
    {
      id: 'starter',
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
      cta: 'Subscribe Now'
    },
    {
      id: 'professional',
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
      cta: 'Subscribe Now'
    },
    {
      id: 'enterprise',
      name: 'Scale Up',
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
      cta: 'Contact Sales'
    }
  ];

  useEffect(() => {
    fetchData();
    
    // Check for success parameter
    if (searchParams.get('success') === 'true') {
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 5000);
      // Sync subscription after successful payment
      syncSubscription();
    }
  }, [searchParams]);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};

      // Fetch subscription status
      try {
        const statusResponse = await axios.get(`${BACKEND_URL}/api/lemonsqueezy/subscription/status`, {
          headers
        });
        setSubscriptionStatus(statusResponse.data);
      } catch (error) {
        console.log('No active subscription');
        setSubscriptionStatus({ has_subscription: false, plan: 'free' });
      }
    } catch (error) {
      console.error('Error fetching subscription data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCheckout = async (planId) => {
    if (checkingOut) return;

    // Handle Enterprise plan differently
    if (planId === 'enterprise') {
      navigate('/enterprise');
      return;
    }
    
    setCheckingOut(planId);
    try {
      const token = localStorage.getItem('token');
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      const response = await axios.post(
        `${BACKEND_URL}/api/lemonsqueezy/checkout/create`,
        {
          plan: planId,
          user_id: user.id || 'demo-user-123',
          user_email: user.email || 'demo@botsmith.com'
        },
        {
          headers
        }
      );

      // Redirect to checkout URL
      if (response.data.checkout_url) {
        window.location.href = response.data.checkout_url;
      }
    } catch (error) {
      console.error('Error creating checkout:', error);
      alert('Failed to create checkout. Please try again.');
    } finally {
      setCheckingOut(null);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-50 via-blue-50 to-purple-50 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-purple-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-purple-50 overflow-hidden relative p-4 sm:p-6 animate-fade-in">
      {/* Advanced Animated background matching Pricing Page */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none z-0" style={{ willChange: 'transform' }}>
        {/* Main gradient blobs */}
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-blob" style={{ transform: 'translateZ(0)' }}></div>
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-blob animation-delay-2000" style={{ transform: 'translateZ(0)' }}></div>
        <div className="absolute -bottom-32 left-1/3 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-blob animation-delay-4000" style={{ transform: 'translateZ(0)' }}></div>
        
        {/* Secondary animated layers */}
        <div className="absolute top-1/4 right-1/3 w-64 h-64 bg-cyan-200 rounded-full mix-blend-multiply filter blur-xl opacity-12 animate-blob animation-delay-1000" style={{ transform: 'translateZ(0)' }}></div>
        <div className="absolute bottom-1/4 left-1/4 w-80 h-80 bg-rose-200 rounded-full mix-blend-multiply filter blur-xl opacity-12 animate-blob animation-delay-3000" style={{ transform: 'translateZ(0)' }}></div>
        
        {/* Geometric floating shapes */}
        <div className="absolute top-20 right-20 w-32 h-32 bg-gradient-to-br from-purple-400/20 to-pink-400/20 rounded-3xl rotate-45 animate-float-rotate blur-sm"></div>
        <div className="absolute bottom-40 left-32 w-24 h-24 bg-gradient-to-br from-blue-400/20 to-cyan-400/20 rounded-2xl rotate-12 animate-float-rotate animation-delay-2000 blur-sm"></div>
        <div className="absolute top-1/2 right-1/4 w-40 h-40 bg-gradient-to-br from-orange-400/15 to-rose-400/15 rounded-full animate-float animation-delay-1000 blur-md"></div>
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Back to Dashboard Button */}
        <div className="mb-4">
          <button
            onClick={() => navigate('/dashboard')}
            className="inline-flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-all duration-200 text-gray-700 hover:text-purple-600 font-medium group text-sm"
          >
            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
            Back to Dashboard
          </button>
        </div>

        {/* Success Message */}
        {showSuccess && (
          <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2 animate-bounce-in">
            <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-green-900 text-sm">Payment Successful!</h3>
              <p className="text-xs text-green-700">Your subscription has been activated. Welcome aboard! 🎉</p>
            </div>
          </div>
        )}

        {/* Header - Match Pricing Page */}
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold mb-3 text-gray-900">
            Choose Your Perfect Plan
          </h1>
          <p className="text-base text-gray-600">
            Start free and scale as you grow. No hidden fees, cancel anytime.
          </p>
        </div>

        {/* Current Subscription Status */}
        {subscriptionStatus?.has_subscription && (
          <div className="mb-6 p-4 bg-purple-50 rounded-xl border border-purple-200">
            <div className="flex items-center gap-2 mb-2">
              <Crown className="w-5 h-5 text-purple-600" />
              <h2 className="text-base font-bold text-gray-900">Current Subscription</h2>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-700 text-sm">
                  <span className="font-semibold">Plan:</span> {subscriptionStatus.plan}
                </p>
                <p className="text-gray-700 text-sm">
                  <span className="font-semibold">Status:</span>{' '}
                  <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                    subscriptionStatus.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {subscriptionStatus.status}
                  </span>
                </p>
              </div>
              {subscriptionStatus.renews_at && (
                <div className="text-right">
                  <p className="text-xs text-gray-500">Renews on</p>
                  <p className="font-semibold text-gray-700 text-sm">
                    {new Date(subscriptionStatus.renews_at).toLocaleDateString()}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Pricing Cards - Match Pricing Page Design */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-5">
          {plans.map((plan, index) => {
            const Icon = plan.icon;
            const isPopular = plan.popular;
            const isFree = plan.isFree;
            const currentPlan = subscriptionStatus?.plan?.toLowerCase() === plan.id.toLowerCase();

            return (
              <div
                key={plan.id}
                className={`relative ${isPopular ? 'lg:-mt-2' : ''}`}
              >
                {/* Popular Badge */}
                {isPopular && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 z-10">
                    <span className="bg-purple-600 text-white px-3 py-1 rounded-full text-xs font-semibold">
                      Most Popular
                    </span>
                  </div>
                )}

                {/* Card */}
                <div className={`h-full bg-white rounded-xl border-2 hover:shadow-lg transition-all duration-300 ${
                  isPopular ? 'border-purple-500' : currentPlan ? 'border-green-500' : 'border-gray-200'
                }`}>
                  {/* Header */}
                  <div className="p-5 border-b border-gray-100">
                    <div className={`w-10 h-10 bg-gradient-to-br ${plan.gradient} rounded-lg flex items-center justify-center mb-3`}>
                      <Icon className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-lg font-bold mb-1">{plan.name}</h3>
                    <p className="text-gray-600 text-xs mb-3">{plan.description}</p>
                    
                    <div>
                      <span className="text-3xl font-bold">{plan.price}</span>
                      {plan.period && (
                        <span className="text-gray-500 text-sm">{plan.period}</span>
                      )}
                    </div>
                  </div>

                  {/* Features */}
                  <div className="p-5">
                    <ul className="space-y-2 mb-5">
                      {plan.features.map((feature, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <Check className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                          <span className="text-gray-700 text-xs">{feature}</span>
                        </li>
                      ))}
                    </ul>

                    {/* CTA Button */}
                    <Button 
                      className={`w-full py-2 rounded-lg text-sm font-medium transition-all ${
                        isFree || currentPlan
                          ? 'border border-gray-300 bg-gray-100 text-gray-500 cursor-not-allowed'
                          : `bg-gradient-to-r ${plan.gradient} hover:opacity-90 text-white border-0`
                      }`}
                      onClick={() => handleCheckout(plan.id)}
                      disabled={isFree || currentPlan || checkingOut !== null}
                    >
                      {checkingOut === plan.id ? (
                        <>
                          <Loader2 className="w-3 h-3 animate-spin mr-1.5 inline" />
                          Processing...
                        </>
                      ) : (
                        currentPlan ? '✓ Current Plan' : plan.cta
                      )}
                    </Button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Help Section - Match Pricing Page */}
        <div className="mt-12 text-center">
          <div className="bg-gray-50 rounded-xl p-6 max-w-2xl mx-auto border border-gray-200">
            <h2 className="text-xl font-bold mb-2">
              Need help choosing?
            </h2>
            <p className="text-gray-600 text-sm mb-4">
              Not sure which plan is right for you? Our team is here to help.
            </p>
            <div className="flex flex-wrap gap-3 justify-center">
              <Button 
                className="bg-purple-600 hover:bg-purple-700 text-white rounded-lg px-6 py-2 text-sm"
                onClick={() => navigate('/enterprise')}
              >
                Talk to Sales
              </Button>
              <Button 
                variant="outline"
                className="border rounded-lg px-6 py-2 text-sm"
                onClick={() => navigate('/resources')}
              >
                View Documentation
              </Button>
            </div>
          </div>
        </div>

        {/* Secure Payment Info */}
        <div className="mt-6 bg-blue-50 rounded-lg p-4 border border-blue-200">
          <div className="flex items-start gap-2">
            <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-gray-900 mb-1 text-sm">Secure Payment Processing</h3>
              <p className="text-gray-700 text-xs mb-2">
                All payments are processed securely through Lemon Squeezy. We never store your payment information.
              </p>
              <ul className="space-y-0.5 text-xs text-gray-600">
                <li>✓ Test mode enabled - No real charges</li>
                <li>✓ Cancel anytime</li>
                <li>✓ Instant activation</li>
                <li>✓ 24/7 support</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default SubscriptionNew;
