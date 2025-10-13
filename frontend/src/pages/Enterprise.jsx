import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Label } from '../components/ui/label';
import { Shield, Users, Zap, HeadphonesIcon } from 'lucide-react';
import { useToast } from '../hooks/use-toast';

const Enterprise = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    message: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    toast({
      title: 'Request Submitted!',
      description: 'Our team will contact you within 24 hours'
    });
    setFormData({ name: '', email: '', company: '', message: '' });
  };

  const features = [
    {
      icon: <Shield className="w-8 h-8" />,
      title: 'Enterprise Security',
      description: 'SOC 2 compliance, SSO, and advanced security features'
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: 'Dedicated Support',
      description: '24/7 support with dedicated account manager'
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: 'Custom Integration',
      description: 'Custom integrations and API development'
    },
    {
      icon: <HeadphonesIcon className="w-8 h-8" />,
      title: 'Priority Support',
      description: 'Fastest response times and priority bug fixes'
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      <nav className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate('/')}>
            <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">C</span>
            </div>
            <span className="text-xl font-semibold">Chatbase</span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <button onClick={() => navigate('/pricing')} className="text-gray-700 hover:text-black transition-colors">Pricing</button>
            <button onClick={() => navigate('/enterprise')} className="text-black font-medium">Enterprise</button>
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
            <h1 className="text-5xl font-bold mb-4">Enterprise Solutions</h1>
            <p className="text-xl text-gray-600">Powerful AI chatbots for large organizations</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-16">
            {features.map((feature, index) => (
              <div key={index} className="p-8 rounded-2xl border border-gray-200 hover:shadow-lg transition-all">
                <div className="w-16 h-16 bg-black rounded-xl flex items-center justify-center text-white mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>

          <div className="bg-gray-50 rounded-2xl p-8">
            <h2 className="text-3xl font-bold mb-2 text-center">Contact Sales</h2>
            <p className="text-gray-600 text-center mb-8">Get in touch with our team to discuss your needs</p>
            <form onSubmit={handleSubmit} className="max-w-xl mx-auto space-y-6">
              <div>
                <Label htmlFor="name">Name</Label>
                <Input
                  id="name"
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
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="mt-2"
                  required
                />
              </div>
              <div>
                <Label htmlFor="company">Company</Label>
                <Input
                  id="company"
                  value={formData.company}
                  onChange={(e) => setFormData({...formData, company: e.target.value})}
                  className="mt-2"
                  required
                />
              </div>
              <div>
                <Label htmlFor="message">Message</Label>
                <Textarea
                  id="message"
                  value={formData.message}
                  onChange={(e) => setFormData({...formData, message: e.target.value})}
                  className="mt-2 min-h-[120px]"
                  required
                />
              </div>
              <Button type="submit" className="w-full bg-black hover:bg-gray-800 text-white py-6">
                Submit Request
              </Button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Enterprise;