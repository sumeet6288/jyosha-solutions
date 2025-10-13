import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { useToast } from '../hooks/use-toast';

const SignUp = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // Mock registration
    localStorage.setItem('chatbase_user', JSON.stringify({ email: formData.email, name: formData.name }));
    toast({
      title: 'Account created!',
      description: 'Welcome to Chatbase'
    });
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-white flex">
      {/* Left Side - Gradient */}
      <div className="hidden md:block md:w-1/2 bg-gradient-to-br from-pink-400 via-purple-400 to-orange-400"></div>
      
      {/* Right Side - Form */}
      <div className="w-full md:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <div className="flex items-center gap-2 mb-8">
            <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">C</span>
            </div>
            <span className="text-xl font-semibold">Chatbase</span>
          </div>
          
          <h1 className="text-3xl font-bold mb-2">Create your account</h1>
          <p className="text-gray-600 mb-8">Start building your AI agents today</p>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <Label htmlFor="name">Full Name</Label>
              <Input
                id="name"
                type="text"
                placeholder="John Doe"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                className="mt-2"
                required
              />
            </div>
            
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
            
            <Button type="submit" className="w-full bg-black hover:bg-gray-800 text-white py-6">
              Create account
            </Button>
          </form>
          
          <p className="mt-6 text-center text-gray-600">
            Already have an account?{' '}
            <button onClick={() => navigate('/signin')} className="text-black font-semibold hover:underline">
              Sign in
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignUp;
