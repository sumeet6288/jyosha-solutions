import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import { 
  Sparkles, Zap, Crown, Check, ArrowRight, 
  TrendingUp, AlertCircle, Loader2, CreditCard, CheckCircle
} from 'lucide-react';
import { Button } from '../components/ui/button';
import Footer from '../components/Footer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const SubscriptionNew = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [plans, setPlans] = useState([]);
  const [subscriptionStatus, setSubscriptionStatus] = useState(null);
  const [checkingOut, setCheckingOut] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);

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
      
      // Fetch available plans
      const plansResponse = await axios.get(`${BACKEND_URL}/api/lemonsqueezy/plans`, {
        headers
      });
      setPlans(plansResponse.data.plans);

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

  const getPlanIcon = (planId) => {
    const icons = {
      starter: Zap,
      professional: Crown
    };
    return icons[planId] || Sparkles;
  };

  const getPlanGradient = (planId) => {
    const gradients = {
      starter: 'from-pink-500 to-purple-500',
      professional: 'from-blue-600 to-indigo-600'
    };
    return gradients[planId] || 'from-gray-400 to-gray-600';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-50 via-blue-50 to-purple-50 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-purple-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-blue-50 to-purple-50 p-6 animate-fade-in">
      <div className="max-w-7xl mx-auto">
        {/* Success Message */}
        {showSuccess && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-3 animate-bounce-in">
            <CheckCircle className="w-6 h-6 text-green-600" />
            <div>
              <h3 className="font-semibold text-green-900">Payment Successful!</h3>
              <p className="text-sm text-green-700">Your subscription has been activated. Welcome aboard! 🎉</p>
            </div>
          </div>
        )}

        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full text-sm font-medium mb-4 shadow-lg">
            <Sparkles className="w-4 h-4" />
            <span>Powered by Lemon Squeezy</span>
          </div>
          <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            Choose Your Plan
          </h1>
          <p className="text-gray-600 text-lg">
            Unlock powerful features for your chatbot business
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

        {/* Free Plan Card */}
        <div className="mb-8">
          <div className="bg-white rounded-2xl shadow-lg border-2 border-gray-200 p-8 hover:shadow-xl transition-all duration-300">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-3 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-xl shadow-lg">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-gray-900">Free Plan</h3>
                <p className="text-gray-600">Perfect for getting started</p>
              </div>
            </div>

            <div className="mb-6">
              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-bold text-gray-900">₹0</span>
                <span className="text-gray-600">/forever</span>
              </div>
            </div>

            <div className="space-y-3 mb-6">
              {['1 Chatbot', '100 messages/month', 'Basic features', 'Community support'].map((feature, idx) => (
                <div key={idx} className="flex items-center gap-2">
                  <Check className="w-5 h-5 text-green-500 flex-shrink-0" />
                  <span className="text-gray-700">{feature}</span>
                </div>
              ))}
            </div>

            <Button
              disabled
              className="w-full bg-gray-200 text-gray-500 cursor-not-allowed"
            >
              Current Plan
            </Button>
          </div>
        </div>

        {/* Paid Plans Grid */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {plans.map((plan) => {
            const Icon = getPlanIcon(plan.id);
            const gradient = getPlanGradient(plan.id);
            const isPopular = plan.id === 'starter';

            return (
              <div
                key={plan.id}
                className={`relative bg-white rounded-2xl shadow-lg p-8 hover:shadow-2xl transition-all duration-300 ${
                  isPopular ? 'border-4 border-purple-500 scale-105' : 'border-2 border-gray-200'
                }`}
              >
                {isPopular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="inline-flex items-center gap-1 px-4 py-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full text-sm font-semibold shadow-lg">
                      <TrendingUp className="w-4 h-4" />
                      Most Popular
                    </span>
                  </div>
                )}

                <div className="flex items-center gap-3 mb-4">
                  <div className={`p-3 bg-gradient-to-br ${gradient} rounded-xl shadow-lg`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">{plan.name}</h3>
                    <p className="text-gray-600">
                      {plan.interval === 'month' ? 'Monthly subscription' : 'One-time payment'}
                    </p>
                  </div>
                </div>

                <div className="mb-6">
                  <div className="flex items-baseline gap-2">
                    <span className="text-4xl font-bold text-gray-900">₹{plan.price}</span>
                    <span className="text-gray-600">
                      {plan.interval === 'month' ? '/month' : 'one-time'}
                    </span>
                  </div>
                </div>

                <div className="space-y-3 mb-6">
                  {plan.features.map((feature, idx) => (
                    <div key={idx} className="flex items-center gap-2">
                      <Check className="w-5 h-5 text-green-500 flex-shrink-0" />
                      <span className="text-gray-700">{feature}</span>
                    </div>
                  ))}
                </div>

                <Button
                  onClick={() => handleCheckout(plan.id)}
                  disabled={checkingOut !== null}
                  className={`w-full bg-gradient-to-r ${gradient} text-white hover:opacity-90 transition-all duration-300 shadow-lg hover:shadow-xl group`}
                >
                  {checkingOut === plan.id ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin mr-2" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <CreditCard className="w-4 h-4 mr-2" />
                      Subscribe Now
                      <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                    </>
                  )}
                </Button>
              </div>
            );
          })}
        </div>

        {/* Info Section */}
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
