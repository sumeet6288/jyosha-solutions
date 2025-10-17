import { useEffect } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LandingPage from './pages/LandingPage';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Dashboard from './pages/Dashboard';
import ChatbotBuilder from './pages/ChatbotBuilder';
import Analytics from './pages/Analytics';
import Integrations from './pages/Integrations';
import AccountSettings from './pages/AccountSettings';
import EmbedChat from './pages/EmbedChat';
import ChatPage from './pages/ChatPage';
import { Toaster } from './components/ui/toaster';

const ProtectedRoute = ({ children }) => {
  // Bypass authentication for now - direct access to all routes
  return children;
};

function AppContent() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/signin" element={<Navigate to="/dashboard" replace />} />
          <Route path="/signup" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/integrations" element={<Integrations />} />
          <Route path="/account-settings" element={<AccountSettings />} />
          <Route path="/chatbot/:id" element={<ChatbotBuilder />} />
        </Routes>
      </BrowserRouter>
      <Toaster />
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
