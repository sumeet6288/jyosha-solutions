import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Menu, X, CreditCard, FileText, Shield } from 'lucide-react';
import UserProfileDropdown from './UserProfileDropdown';
import NotificationBell from './NotificationBell';

const ResponsiveNav = ({ user, onLogout }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  // Base navigation items for all users
  const baseNavItems = [
    { path: '/dashboard', label: 'Chatbots' },
    { path: '/analytics', label: 'Analytics' },
    { path: '/subscription', label: 'Subscription', icon: CreditCard },
  ];

  // Add admin panel only for admin users
  const navItems = user?.role === 'admin' 
    ? [...baseNavItems, { path: '/admin', label: 'Admin Panel', icon: Shield }]
    : baseNavItems;

  return (
    <nav className="bg-white/80 backdrop-blur-lg border-b border-gray-200/50 sticky top-0 z-50 shadow-sm">
      <div className="px-4 sm:px-6 py-4 flex items-center justify-between max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-3 cursor-pointer group" onClick={() => navigate('/dashboard')}>
            {/* Premium 3D Logo */}
            <div className="relative">
              {/* Background glow effect */}
              <div className="absolute inset-0 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl blur-xl opacity-40 group-hover:opacity-60 transition-opacity duration-500"></div>
              
              {/* Main logo container */}
              <div className="relative w-12 h-12 bg-gradient-to-br from-purple-600 via-fuchsia-500 to-pink-600 rounded-2xl flex items-center justify-center transform group-hover:scale-105 group-hover:rotate-6 transition-all duration-500 shadow-2xl border border-white/20">
                {/* Inner gradient highlight */}
                <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-white/30 to-transparent opacity-50"></div>
                
                {/* Bot icon with 3D effect */}
                <svg className="w-7 h-7 text-white relative z-10 drop-shadow-lg" fill="currentColor" viewBox="0 0 24 24">
                  {/* Robot head */}
                  <path d="M12 2C11.45 2 11 2.45 11 3V4H7C5.89 4 5 4.89 5 6V18C5 19.11 5.89 20 7 20H17C18.11 20 19 19.11 19 18V6C19 4.89 18.11 4 17 4H13V3C13 2.45 12.55 2 12 2M7 6H17V18H7V6Z"/>
                  {/* Eyes */}
                  <circle cx="9" cy="10" r="1.5" className="animate-pulse"/>
                  <circle cx="15" cy="10" r="1.5" className="animate-pulse"/>
                  {/* Smile */}
                  <path d="M9 14C9 14 10 15.5 12 15.5S15 14 15 14" strokeWidth="1.5" stroke="currentColor" fill="none" strokeLinecap="round"/>
                  {/* Antenna */}
                  <circle cx="12" cy="3" r="1"/>
                </svg>
                
                {/* Sparkle effects */}
                <div className="absolute -top-1 -right-1 w-2 h-2 bg-yellow-300 rounded-full animate-ping"></div>
                <div className="absolute -bottom-1 -left-1 w-1.5 h-1.5 bg-cyan-300 rounded-full animate-ping" style={{animationDelay: '0.5s'}}></div>
              </div>
              
              {/* Animated orbital ring */}
              <div className="absolute inset-0 rounded-2xl border-2 border-purple-400/30 opacity-0 group-hover:opacity-100 group-hover:scale-125 transition-all duration-700 animate-pulse"></div>
            </div>
            
            {/* Premium Brand Typography */}
            <div className="flex flex-col -space-y-0.5">
              <div className="flex items-baseline gap-1">
                <span className="text-2xl sm:text-3xl font-black tracking-tight bg-gradient-to-r from-purple-700 via-fuchsia-600 to-pink-600 bg-clip-text text-transparent group-hover:from-purple-800 group-hover:via-fuchsia-700 group-hover:to-pink-700 transition-all duration-300 drop-shadow-sm">
                  BotSmith
                </span>
                <span className="text-[9px] font-bold text-purple-600 bg-purple-100 px-1.5 py-0.5 rounded-md">AI</span>
              </div>
              <span className="text-[10px] font-semibold text-gray-400 tracking-wider uppercase">
                Powered by Jyosha Solutions
              </span>
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
          {/* Notification Bell - Desktop */}
          <div className="hidden md:block">
            <NotificationBell />
          </div>
          
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
