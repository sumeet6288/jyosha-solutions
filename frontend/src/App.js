import { useEffect } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { NotificationProvider } from './context/NotificationContext';
import { Toaster as HotToaster } from 'react-hot-toast';
import LandingPage from './pages/LandingPage';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Dashboard from './pages/Dashboard';
import ChatbotBuilder from './pages/ChatbotBuilder';
import Analytics from './pages/Analytics';
import AccountSettings from './pages/AccountSettings';
import Subscription from './pages/Subscription';
import NotificationPreferences from './pages/NotificationPreferences';
import EmbedChat from './pages/EmbedChat';
import ChatPage from './pages/ChatPage';
import PublicChat from './pages/PublicChat';
import Pricing from './pages/Pricing';
import Enterprise from './pages/Enterprise';
import Resources from './pages/Resources';
import Documentation from './pages/resources/Documentation';
import APIReference from './pages/resources/APIReference';
import HelpCenter from './pages/resources/HelpCenter';
import Community from './pages/resources/Community';
import QuickStartGuide from './pages/resources/articles/QuickStartGuide';
import Installation from './pages/resources/articles/Installation';
import YourFirstChatbot from './pages/resources/articles/YourFirstChatbot';
import AddingKnowledgeBase from './pages/resources/articles/AddingKnowledgeBase';
import CustomizationOptions from './pages/resources/articles/CustomizationOptions';
import AnalyticsInsights from './pages/resources/articles/AnalyticsInsights';
import SharingDeployment from './pages/resources/articles/SharingDeployment';
import ChatbotManagement from './pages/resources/articles/ChatbotManagement';
import NotFound from './pages/NotFound';
import AdminDashboard from './pages/admin/AdminDashboard';
import { Toaster } from './components/ui/toaster';
import { Toaster as SonnerToaster } from 'sonner';

const ProtectedRoute = ({ children }) => {
  // Bypass authentication for now - direct access to all routes
  return children;
};

// Smooth scroll to top on route change
function ScrollToTop() {
  const location = useLocation();
  
  useEffect(() => {
    // Smooth scroll to top with animation
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth'
    });
  }, [location.pathname]);
  
  return null;
}

function AppContent() {
  const { user } = useAuth();
  
  return (
    <div className="App">
      <BrowserRouter>
        <ScrollToTop />
        <NotificationProvider user={user}>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/pricing" element={<Pricing />} />
            <Route path="/enterprise" element={<Enterprise />} />
            <Route path="/resources" element={<Resources />} />
            <Route path="/resources/documentation" element={<Documentation />} />
            <Route path="/resources/articles/quick-start-guide" element={<QuickStartGuide />} />
            <Route path="/resources/articles/installation" element={<Installation />} />
            <Route path="/resources/articles/your-first-chatbot" element={<YourFirstChatbot />} />
            <Route path="/resources/articles/adding-knowledge-base" element={<AddingKnowledgeBase />} />
            <Route path="/resources/articles/customization-options" element={<CustomizationOptions />} />
            <Route path="/resources/articles/analytics-insights" element={<AnalyticsInsights />} />
            <Route path="/resources/articles/sharing-deployment" element={<SharingDeployment />} />
            <Route path="/resources/articles/chatbot-management" element={<ChatbotManagement />} />
            <Route path="/resources/api-reference" element={<APIReference />} />
            <Route path="/resources/help-center" element={<HelpCenter />} />
            <Route path="/resources/community" element={<Community />} />
            <Route path="/signin" element={<Navigate to="/dashboard" replace />} />
            <Route path="/signup" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/subscription" element={<Subscription />} />
            <Route path="/integrations" element={<Integrations />} />
            <Route path="/account-settings" element={<AccountSettings />} />
            <Route path="/notification-preferences" element={<NotificationPreferences />} />
            <Route path="/chatbot/:id" element={<ChatbotBuilder />} />
            <Route path="/embed/:id" element={<EmbedChat />} />
            <Route path="/chat/:id" element={<ChatPage />} />
            <Route path="/public-chat/:chatbotId" element={<PublicChat />} />
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </NotificationProvider>
      </BrowserRouter>
      <Toaster />
      <SonnerToaster position="top-right" richColors />
      <HotToaster position="top-right" />
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
