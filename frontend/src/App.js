import { useEffect } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LandingPage from './pages/LandingPage';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Dashboard from './pages/Dashboard';
import ChatbotBuilder from './pages/ChatbotBuilder';
import Analytics from './pages/Analytics';
import Integrations from './pages/Integrations';
import AccountSettings from './pages/AccountSettings';
import Subscription from './pages/Subscription';
import EmbedChat from './pages/EmbedChat';
import ChatPage from './pages/ChatPage';
import PublicChat from './pages/PublicChat';
import Pricing from './pages/Pricing';
import Enterprise from './pages/Enterprise';
import Resources from './pages/Resources';
import NotFound from './pages/NotFound';
import { Toaster } from './components/ui/toaster';

const ProtectedRoute = ({ children }) => {
  // Bypass authentication for now - direct access to all routes
  return children;
};

// Scroll to top on route change
function ScrollToTop() {
  const location = useLocation();
  
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location.pathname]);
  
  return null;
}

function AppContent() {
  return (
    <div className="App">
      <BrowserRouter>
        <ScrollToTop />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/enterprise" element={<Enterprise />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/signin" element={<Navigate to="/dashboard" replace />} />
          <Route path="/signup" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/integrations" element={<Integrations />} />
          <Route path="/subscription" element={<Subscription />} />
          <Route path="/account-settings" element={<AccountSettings />} />
          <Route path="/chatbot/:id" element={<ChatbotBuilder />} />
          <Route path="/embed/:id" element={<EmbedChat />} />
          <Route path="/chat/:id" element={<ChatPage />} />
          <Route path="/public-chat/:chatbotId" element={<PublicChat />} />
          <Route path="*" element={<NotFound />} />
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
