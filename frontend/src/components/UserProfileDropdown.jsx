import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MessageSquare, Settings, Users, LogOut, Bell, ChevronDown } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './ui/dropdown-menu';

const UserProfileDropdown = ({ user, onLogout }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    if (onLogout) {
      onLogout();
    }
  };

  if (!user) return null;

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button className="flex items-center gap-3 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 rounded-xl px-4 py-2.5 transition-all duration-200 cursor-pointer border border-transparent hover:border-purple-200 hover:shadow-sm group">
          <div className="text-right">
            <p className="text-sm font-semibold text-gray-800 group-hover:text-purple-700 transition-colors">{user.name}</p>
            <p className="text-xs text-gray-500 group-hover:text-purple-600 transition-colors">{user.email}</p>
          </div>
          <div className="relative">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 via-pink-500 to-rose-500 rounded-full flex items-center justify-center text-white font-bold shadow-md group-hover:shadow-lg transition-shadow ring-2 ring-white">
              {user.name?.charAt(0).toUpperCase()}
            </div>
            <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
          </div>
          <ChevronDown className="w-4 h-4 text-gray-400 group-hover:text-purple-600 transition-colors" />
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-72 p-2 bg-white shadow-2xl border-0 rounded-2xl">
        {/* User Info Header */}
        <DropdownMenuLabel className="font-normal p-0 mb-2">
          <div className="bg-gradient-to-br from-purple-50 via-pink-50 to-rose-50 rounded-xl p-4 border border-purple-100">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500 via-pink-500 to-rose-500 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-md ring-4 ring-purple-100">
                {user.name?.charAt(0).toUpperCase()}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-base font-bold text-gray-800 truncate">{user.name}</p>
                <p className="text-xs text-gray-600 truncate">{user.email}</p>
              </div>
            </div>
            <div className="flex items-center gap-2 mt-2">
              <div className="flex-1 bg-white/80 backdrop-blur-sm rounded-lg px-3 py-2 border border-purple-200/50">
                <p className="text-xs font-semibold text-purple-700">Free Plan</p>
              </div>
              <button 
                onClick={() => navigate('/subscription')}
                className="px-3 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white text-xs font-semibold rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all shadow-sm hover:shadow-md"
              >
                Upgrade
              </button>
            </div>
          </div>
        </DropdownMenuLabel>
        
        <DropdownMenuSeparator className="my-2 bg-gray-100" />
        
        {/* Menu Items */}
        <DropdownMenuItem 
          onClick={() => navigate('/dashboard')} 
          className="cursor-pointer rounded-lg px-3 py-2.5 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 transition-all duration-200 group mb-1"
        >
          <div className="flex items-center gap-3 w-full">
            <div className="w-8 h-8 rounded-lg bg-purple-100 group-hover:bg-purple-200 flex items-center justify-center transition-colors">
              <MessageSquare className="h-4 w-4 text-purple-600" />
            </div>
            <span className="font-medium text-gray-700 group-hover:text-purple-700 transition-colors">Dashboard</span>
          </div>
        </DropdownMenuItem>
        
        <DropdownMenuItem 
          onClick={() => navigate('/account-settings')} 
          className="cursor-pointer rounded-lg px-3 py-2.5 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 transition-all duration-200 group mb-1"
        >
          <div className="flex items-center gap-3 w-full">
            <div className="w-8 h-8 rounded-lg bg-blue-100 group-hover:bg-blue-200 flex items-center justify-center transition-colors">
              <Settings className="h-4 w-4 text-blue-600" />
            </div>
            <span className="font-medium text-gray-700 group-hover:text-blue-700 transition-colors">Account Settings</span>
          </div>
        </DropdownMenuItem>
        
        <DropdownMenuItem 
          onClick={() => navigate('/notification-preferences')} 
          className="cursor-pointer rounded-lg px-3 py-2.5 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 transition-all duration-200 group mb-1"
        >
          <div className="flex items-center gap-3 w-full">
            <div className="w-8 h-8 rounded-lg bg-amber-100 group-hover:bg-amber-200 flex items-center justify-center transition-colors">
              <Bell className="h-4 w-4 text-amber-600" />
            </div>
            <span className="font-medium text-gray-700 group-hover:text-amber-700 transition-colors">Notifications</span>
          </div>
        </DropdownMenuItem>
        
        <DropdownMenuItem 
          onClick={() => navigate('/workspace')} 
          className="cursor-pointer rounded-lg px-3 py-2.5 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 transition-all duration-200 group mb-1"
        >
          <div className="flex items-center gap-3 w-full">
            <div className="w-8 h-8 rounded-lg bg-emerald-100 group-hover:bg-emerald-200 flex items-center justify-center transition-colors">
              <Users className="h-4 w-4 text-emerald-600" />
            </div>
            <span className="font-medium text-gray-700 group-hover:text-emerald-700 transition-colors">Workspace</span>
          </div>
        </DropdownMenuItem>
        
        <DropdownMenuSeparator className="my-2 bg-gray-100" />
        
        <DropdownMenuItem 
          onClick={handleLogout} 
          className="cursor-pointer rounded-lg px-3 py-2.5 hover:bg-red-50 transition-all duration-200 group"
        >
          <div className="flex items-center gap-3 w-full">
            <div className="w-8 h-8 rounded-lg bg-red-100 group-hover:bg-red-200 flex items-center justify-center transition-colors">
              <LogOut className="h-4 w-4 text-red-600" />
            </div>
            <span className="font-medium text-red-600 group-hover:text-red-700 transition-colors">Sign Out</span>
          </div>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

export default UserProfileDropdown;
