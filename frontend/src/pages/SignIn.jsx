import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { useToast } from '../hooks/use-toast';

const SignIn = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // Mock authentication
    localStorage.setItem('chatbase_user', JSON.stringify({ email: formData.email, name: 'User' }));
    toast({
      title: 'Welcome back!',
      description: 'Successfully signed in'
    });
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-white flex">
      {/* Left Side - Form */}
      <div className="w-full md:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <div className="flex items-center gap-2 mb-8">
            <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">C</span>
            </div>
            <span className="text-xl font-semibold">Chatbase</span>
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
            
            <Button type="submit" className="w-full bg-black hover:bg-gray-800 text-white py-6">
              Sign in
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
