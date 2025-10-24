import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Menu, X, CreditCard } from 'lucide-react';
import UserProfileDropdown from './UserProfileDropdown';

const ResponsiveNav = ({ user, onLogout }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  const navItems = [
    { path: '/dashboard', label: 'Chatbots' },
    { path: '/analytics', label: 'Analytics' },
    { path: '/subscription', label: 'Subscription', icon: CreditCard },
    { path: '/integrations', label: 'Integrations' },
  ];

  return (
    <nav className="bg-white/80 backdrop-blur-lg border-b border-gray-200/50 sticky top-0 z-50 shadow-sm">
      <div className="px-4 sm:px-6 py-4 flex items-center justify-between max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-3 cursor-pointer group" onClick={() => navigate('/dashboard')}>
            {/* Enhanced Logo */}
            <div className="relative">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-600 via-pink-500 to-purple-700 rounded-xl flex items-center justify-center transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg shadow-purple-500/40">
                <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
                  <circle cx="12" cy="11" r="1.5"/>
                  <circle cx="8" cy="11" r="1.5"/>
                  <circle cx="16" cy="11" r="1.5"/>
                </svg>
              </div>
              {/* Animated ring */}
              <div className="absolute inset-0 rounded-xl border-2 border-purple-400 opacity-0 group-hover:opacity-100 group-hover:scale-125 transition-all duration-500"></div>
            </div>
            
            {/* Enhanced Brand Name */}
            <div className="flex flex-col -space-y-1">
              <span className="text-xl sm:text-2xl font-bold bg-gradient-to-r from-purple-600 via-pink-500 to-purple-700 bg-clip-text text-transparent group-hover:from-purple-700 group-hover:via-pink-600 group-hover:to-purple-800 transition-all duration-300">
                BotSmith
              </span>
              <span className="text-[10px] font-medium text-gray-500 tracking-wider uppercase">AI Platform</span>
            </div>
          </div>
        </div>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-6">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                className={`transition-colors font-medium relative group flex items-center gap-2 ${
                  isActive(item.path)
                    ? 'text-purple-600 font-semibold'
                    : 'text-gray-600 hover:text-purple-600'
                }`}
              >
                {Icon && <Icon className="w-4 h-4" />}
                {item.label}
                <span
                  className={`absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-purple-600 to-pink-600 transform transition-transform ${
                    isActive(item.path) ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'
                  }`}
                ></span>
              </button>
            );
          })}
        </div>

        <div className="flex items-center gap-2 sm:gap-4">
          <div className="hidden md:block">
            <UserProfileDropdown user={user} onLogout={onLogout} />
          </div>
          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-purple-100 transition-colors"
          >
            {mobileMenuOpen ? (
              <X className="w-6 h-6 text-gray-600" />
            ) : (
              <Menu className="w-6 h-6 text-gray-600" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-gray-200 bg-white/95 backdrop-blur-lg">
          <div className="px-4 py-3 space-y-3">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.path}
                  onClick={() => {
                    navigate(item.path);
                    setMobileMenuOpen(false);
                  }}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-colors flex items-center gap-2 ${
                    isActive(item.path)
                      ? 'text-purple-600 font-semibold bg-purple-50'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  {Icon && <Icon className="w-4 h-4" />}
                  {item.label}
                </button>
              );
            })}
            <div className="pt-3 border-t border-gray-200">
              <UserProfileDropdown user={user} onLogout={onLogout} />
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default ResponsiveNav;
