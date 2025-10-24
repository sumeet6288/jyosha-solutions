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
      cta: 'Contact Sales'
    }
  ];

  useEffect(() => {
    fetchData();
    
    // Check for success parameter
    if (searchParams.get('success') === 'true') {
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 5000);
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
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-blue-50 to-purple-50 p-4 sm:p-6 animate-fade-in">
      <div className="max-w-[95%] mx-auto">
        {/* Back to Dashboard Button */}
        <div className="mb-4 sm:mb-6">
          <button
            onClick={() => navigate('/dashboard')}
            className="inline-flex items-center gap-2 px-3 sm:px-4 py-2 bg-white rounded-lg shadow-md hover:shadow-lg transition-all duration-200 text-gray-700 hover:text-purple-600 font-medium group text-sm sm:text-base"
          >
            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
            <span className="hidden sm:inline">Back to Dashboard</span>
            <span className="sm:hidden">Back</span>
          </button>
        </div>

        {/* Success Message */}
        {showSuccess && (
          <div className="mb-4 sm:mb-6 p-3 sm:p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2 sm:gap-3 animate-bounce-in">
            <CheckCircle className="w-5 h-5 sm:w-6 sm:h-6 text-green-600 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-green-900 text-sm sm:text-base">Payment Successful!</h3>
              <p className="text-xs sm:text-sm text-green-700">Your subscription has been activated. Welcome aboard! 🎉</p>
            </div>
          </div>
        )}

        {/* Header - Reduced to 80% */}
        <div className="text-center mb-6 sm:mb-8">
          <div className="inline-flex items-center gap-1.5 px-2.5 sm:px-3 py-1 sm:py-1.5 bg-gradient-to-r from-pink-500 to-blue-500 rounded-full text-white font-medium mb-2 sm:mb-3 shadow-md text-[10px] sm:text-xs">
            <Sparkles className="w-2.5 h-2.5 sm:w-3 sm:h-3" />
            <span>Simple, Transparent Pricing</span>
          </div>
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-2 sm:mb-3 bg-gradient-to-r from-pink-600 via-purple-600 to-blue-600 bg-clip-text text-transparent px-4">
            Choose Your Perfect Plan
          </h1>
          <p className="text-gray-600 text-xs sm:text-base md:text-lg max-w-2xl mx-auto px-4">
            Start free and scale as you grow. No hidden fees, cancel anytime.
          </p>
        </div>

        {/* Current Subscription Status */}
        {subscriptionStatus?.has_subscription && (
          <div className="mb-8 p-6 bg-white rounded-xl shadow-lg border-2 border-purple-200">
            <div className="flex items-center gap-3 mb-2">
              <Crown className="w-6 h-6 text-purple-600" />
              <h2 className="text-xl font-bold text-gray-900">Current Subscription</h2>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-700">
                  <span className="font-semibold">Plan:</span> {subscriptionStatus.plan}
                </p>
                <p className="text-gray-700">
                  <span className="font-semibold">Status:</span>{' '}
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    subscriptionStatus.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {subscriptionStatus.status}
                  </span>
                </p>
              </div>
              {subscriptionStatus.renews_at && (
                <div className="text-right">
                  <p className="text-sm text-gray-500">Renews on</p>
                  <p className="font-semibold text-gray-700">
                    {new Date(subscriptionStatus.renews_at).toLocaleDateString()}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* All Plans Grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8 mb-8 sm:mb-12">
          {plans.map((plan, index) => {
            const Icon = plan.icon;
            const isPopular = plan.popular;
            const isFree = plan.isFree;
            const currentPlan = subscriptionStatus?.plan?.toLowerCase() === plan.id.toLowerCase();

            return (
              <div
                key={plan.id}
                className={`relative group ${
                  isPopular ? 'lg:-mt-4 lg:mb-4' : ''
                }`}
              >
                {/* Popular Badge */}
                {isPopular && (
                  <div className="absolute -top-4 sm:-top-5 left-1/2 transform -translate-x-1/2 z-10">
                    <span className="bg-gradient-to-r from-pink-500 to-purple-500 text-white px-3 sm:px-4 py-1.5 sm:py-2 rounded-full text-xs sm:text-sm font-bold shadow-lg">
                      ⭐ Most Popular
                    </span>
                  </div>
                )}

                {/* Card */}
                <div className={`h-full bg-white rounded-2xl sm:rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-300 overflow-hidden ${
                  isPopular ? 'ring-2 sm:ring-4 ring-purple-500 ring-opacity-50' : ''
                }`}>
                  {/* Gradient Header */}
                  <div className={`bg-gradient-to-br ${plan.gradient} p-5 sm:p-8 text-white`}>
                    <div className="flex items-center justify-between mb-3 sm:mb-4">
                      <Icon className="w-8 h-8 sm:w-10 sm:h-10" />
                      {isPopular && (
                        <Sparkles className="w-5 h-5 sm:w-6 sm:h-6 animate-pulse" />
                      )}
                    </div>
                    <h3 className="text-xl sm:text-2xl font-bold mb-1 sm:mb-2">{plan.name}</h3>
                    <p className="text-white/90 text-xs sm:text-sm mb-4 sm:mb-6">{plan.description}</p>
                    
                    <div className="mb-2">
                      <span className="text-3xl sm:text-4xl md:text-5xl font-bold">{plan.price}</span>
                      {plan.period && (
                        <span className="text-white/80 text-sm sm:text-base md:text-lg">{plan.period}</span>
                      )}
                    </div>
                  </div>

                  {/* Features */}
                  <div className="p-5 sm:p-8">
                    <ul className="space-y-2.5 sm:space-y-4 mb-6 sm:mb-8">
                      {plan.features.map((feature, i) => (
                        <li key={i} className="flex items-start gap-2 sm:gap-3">
                          <div className={`mt-0.5 bg-gradient-to-r ${plan.gradient} rounded-full p-0.5 sm:p-1 flex-shrink-0`}>
                            <Check className="w-3 h-3 sm:w-4 sm:h-4 text-white" />
                          </div>
                          <span className="text-gray-700 text-xs sm:text-sm leading-tight">{feature}</span>
                        </li>
                      ))}
                    </ul>

                    {/* CTA Button */}
                    <Button 
                      className={`w-full py-4 sm:py-6 rounded-lg sm:rounded-xl font-semibold text-sm sm:text-base transition-all duration-300 ${
                        isFree || currentPlan
                          ? 'border-2 border-gray-300 bg-gray-100 text-gray-500 cursor-not-allowed'
                          : `bg-gradient-to-r ${plan.gradient} hover:shadow-lg hover:scale-105 text-white border-0`
                      }`}
                      onClick={() => handleCheckout(plan.id)}
                      disabled={isFree || currentPlan || checkingOut !== null}
                    >
                      {checkingOut === plan.id ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin mr-2 inline" />
                          Processing...
                        </>
                      ) : (
                        currentPlan ? 'Current Plan' : plan.cta
                      )}
                    </Button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Additional Info Section */}
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl p-12 shadow-xl max-w-4xl mx-auto mb-8">
          <h2 className="text-3xl font-bold mb-6 bg-gradient-to-r from-pink-600 to-blue-600 bg-clip-text text-transparent text-center">
            Need help choosing?
          </h2>
          <p className="text-gray-600 text-lg mb-8 text-center">
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

        {/* Secure Payment Info */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-200">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Secure Payment Processing</h3>
              <p className="text-gray-700 text-sm mb-3">
                All payments are processed securely through Lemon Squeezy. We never store your payment information.
              </p>
              <ul className="space-y-1 text-sm text-gray-600">
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
