import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { useToast } from '../hooks/use-toast';
import { useAuth } from '../contexts/AuthContext';

const SignIn = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      await login(formData.email, formData.password);
      toast({
        title: 'Welcome back!',
        description: 'Successfully signed in'
      });
      navigate('/dashboard');
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.detail || 'Failed to sign in',
        variant: 'destructive'
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex">
      {/* Left Side - Form */}
      <div className="w-full md:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <div className="flex items-center gap-3 mb-8 group">
            {/* Premium 3D Logo - Compact Version */}
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity duration-500"></div>
              
              <div className="relative w-10 h-10 bg-gradient-to-br from-purple-600 via-fuchsia-500 to-pink-600 rounded-xl flex items-center justify-center transform group-hover:scale-105 transition-all duration-300 shadow-lg border border-white/20">
                <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-white/30 to-transparent opacity-50"></div>
                
                <svg className="w-6 h-6 text-white relative z-10 drop-shadow-md" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C11.45 2 11 2.45 11 3V4H7C5.89 4 5 4.89 5 6V18C5 19.11 5.89 20 7 20H17C18.11 20 19 19.11 19 18V6C19 4.89 18.11 4 17 4H13V3C13 2.45 12.55 2 12 2M7 6H17V18H7V6Z"/>
                  <circle cx="9" cy="10" r="1.5"/>
                  <circle cx="15" cy="10" r="1.5"/>
                  <path d="M9 14C9 14 10 15.5 12 15.5S15 14 15 14" strokeWidth="1.5" stroke="currentColor" fill="none" strokeLinecap="round"/>
                  <circle cx="12" cy="3" r="1"/>
                </svg>
              </div>
            </div>
            
            <div className="flex flex-col -space-y-0.5">
              <div className="flex items-baseline gap-1">
                <span className="text-2xl font-black tracking-tight bg-gradient-to-r from-purple-700 via-fuchsia-600 to-pink-600 bg-clip-text text-transparent">
                  BotSmith
                </span>
                <span className="text-[8px] font-bold text-purple-600 bg-purple-100 px-1.5 py-0.5 rounded">AI</span>
              </div>
            </div>
          </div>
          
          <h1 className="text-3xl font-bold mb-2">Welcome back</h1>
          <p className="text-gray-600 mb-8">Sign in to your account to continue</p>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="your@email.com"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="mt-2"
                required
              />
            </div>
            
            <div>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                className="mt-2"
                required
              />
            </div>
            
            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 text-sm">
                <input type="checkbox" className="rounded" />
                <span>Remember me</span>
              </label>
              <button type="button" className="text-sm text-black hover:underline">
                Forgot password?
              </button>
            </div>
            
            <Button type="submit" className="w-full bg-black hover:bg-gray-800 text-white py-6" disabled={isLoading}>
              {isLoading ? 'Signing in...' : 'Sign in'}
            </Button>
          </form>
          
          <p className="mt-6 text-center text-gray-600">
            Don't have an account?{' '}
            <button onClick={() => navigate('/signup')} className="text-black font-semibold hover:underline">
              Sign up
            </button>
          </p>
        </div>
      </div>
      
      {/* Right Side - Gradient */}
      <div className="hidden md:block md:w-1/2 bg-gradient-to-br from-pink-400 via-purple-400 to-orange-400"></div>
    </div>
  );
};

export default SignIn;
