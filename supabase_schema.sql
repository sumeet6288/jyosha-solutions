-- ============================================
-- BotSmith Supabase Schema Migration
-- From MongoDB to PostgreSQL
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. PLANS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS plans (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0,
    description TEXT,
    limits JSONB NOT NULL DEFAULT '{}',
    features JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 2. USERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Basic Info
    role VARCHAR(50) DEFAULT 'user',
    status VARCHAR(50) DEFAULT 'active',
    suspension_reason TEXT,
    suspension_until TIMESTAMP WITH TIME ZONE,
    
    -- Contact & Profile
    phone VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    zip_code VARCHAR(20),
    bio TEXT,
    avatar_url TEXT,
    company VARCHAR(255),
    job_title VARCHAR(255),
    website VARCHAR(255),
    
    -- Custom Limits (legacy)
    custom_max_chatbots INTEGER,
    custom_max_messages INTEGER,
    custom_max_file_uploads INTEGER,
    
    -- Activity Tracking
    last_login TIMESTAMP WITH TIME ZONE,
    login_count INTEGER DEFAULT 0,
    last_ip VARCHAR(50),
    last_active TIMESTAMP WITH TIME ZONE,
    
    -- Lifecycle
    lifecycle_stage VARCHAR(50) DEFAULT 'new',
    onboarding_completed BOOLEAN DEFAULT false,
    onboarding_progress INTEGER DEFAULT 0,
    onboarding_step INTEGER DEFAULT 0,
    churn_risk_score INTEGER DEFAULT 0,
    total_spent DECIMAL(10, 2) DEFAULT 0,
    lifetime_value DECIMAL(10, 2) DEFAULT 0,
    
    -- Plan Info
    current_plan VARCHAR(50),
    plan_start_date TIMESTAMP WITH TIME ZONE,
    plan_id VARCHAR(50) REFERENCES plans(id),
    
    -- Arrays and Objects
    tags TEXT[] DEFAULT '{}',
    segments TEXT[] DEFAULT '{}',
    custom_fields JSONB DEFAULT '{}',
    admin_notes TEXT,
    internal_notes JSONB DEFAULT '[]',
    
    -- Notifications
    email_notifications BOOLEAN DEFAULT true,
    marketing_emails BOOLEAN DEFAULT true,
    timezone VARCHAR(50),
    language VARCHAR(10) DEFAULT 'en',
    notification_preferences JSONB DEFAULT '{}',
    
    -- Permissions
    permissions JSONB DEFAULT '{}',
    
    -- Security
    email_verified BOOLEAN DEFAULT false,
    two_factor_enabled BOOLEAN DEFAULT false,
    password_expires_at TIMESTAMP WITH TIME ZONE,
    force_password_change BOOLEAN DEFAULT false,
    allowed_ips TEXT[] DEFAULT '{}',
    blocked_ips TEXT[] DEFAULT '{}',
    max_sessions INTEGER DEFAULT 5,
    session_timeout INTEGER DEFAULT 3600,
    
    -- Billing
    stripe_customer_id VARCHAR(255),
    billing_email VARCHAR(255),
    payment_method VARCHAR(50),
    trial_ends_at TIMESTAMP WITH TIME ZONE,
    subscription_ends_at TIMESTAMP WITH TIME ZONE,
    lifetime_access BOOLEAN DEFAULT false,
    discount_code VARCHAR(100),
    custom_pricing DECIMAL(10, 2),
    
    -- Custom Limits (new)
    custom_limits JSONB DEFAULT '{}',
    
    -- Feature Flags
    feature_flags JSONB DEFAULT '{}',
    
    -- API Rate Limits
    api_rate_limits JSONB DEFAULT '{}',
    
    -- Appearance
    theme VARCHAR(20) DEFAULT 'light',
    custom_css TEXT,
    branding JSONB DEFAULT '{}',
    
    -- Tracking
    tracking_enabled BOOLEAN DEFAULT true,
    analytics_enabled BOOLEAN DEFAULT true,
    last_activity_at TIMESTAMP WITH TIME ZONE,
    
    -- API & Integrations
    api_key VARCHAR(255),
    webhook_url TEXT,
    webhook_events TEXT[] DEFAULT '{}',
    oauth_tokens JSONB DEFAULT '{}',
    integration_preferences JSONB DEFAULT '{}'
);

-- Create indexes for users
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);
CREATE INDEX IF NOT EXISTS idx_users_plan_id ON users(plan_id);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- ============================================
-- 3. SUBSCRIPTIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) REFERENCES users(id) ON DELETE CASCADE,
    plan_id VARCHAR(50) REFERENCES plans(id),
    status VARCHAR(50) DEFAULT 'active',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    auto_renew BOOLEAN DEFAULT false,
    billing_cycle VARCHAR(20) DEFAULT 'monthly',
    usage JSONB DEFAULT '{}'
);

-- Create indexes for subscriptions
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_plan_id ON subscriptions(plan_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);

-- ============================================
-- 4. ACTIVITY LOGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS activity_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    details TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address VARCHAR(50)
);

-- Create indexes for activity_logs
CREATE INDEX IF NOT EXISTS idx_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_timestamp ON activity_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_activity_logs_action ON activity_logs(action);

-- ============================================
-- 5. CHATBOTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS chatbots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    model VARCHAR(100) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    temperature DECIMAL(3, 2) DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 1000,
    system_prompt TEXT,
    welcome_message TEXT,
    placeholder TEXT,
    suggested_messages TEXT[] DEFAULT '{}',
    primary_color VARCHAR(20) DEFAULT '#7c3aed',
    secondary_color VARCHAR(20) DEFAULT '#ec4899',
    widget_position VARCHAR(20) DEFAULT 'bottom-right',
    widget_theme VARCHAR(20) DEFAULT 'light',
    widget_size VARCHAR(20) DEFAULT 'medium',
    auto_expand BOOLEAN DEFAULT false,
    is_public BOOLEAN DEFAULT false,
    rate_limit INTEGER DEFAULT 10,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for chatbots
CREATE INDEX IF NOT EXISTS idx_chatbots_user_id ON chatbots(user_id);
CREATE INDEX IF NOT EXISTS idx_chatbots_created_at ON chatbots(created_at);

-- ============================================
-- 6. SOURCES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chatbot_id UUID REFERENCES chatbots(id) ON DELETE CASCADE,
    user_id VARCHAR(100) REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    content TEXT,
    url TEXT,
    file_path TEXT,
    file_size INTEGER,
    status VARCHAR(50) DEFAULT 'pending',
    error_message TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for sources
CREATE INDEX IF NOT EXISTS idx_sources_chatbot_id ON sources(chatbot_id);
CREATE INDEX IF NOT EXISTS idx_sources_user_id ON sources(user_id);
CREATE INDEX IF NOT EXISTS idx_sources_status ON sources(status);

-- ============================================
-- 7. CHUNKS TABLE (for RAG)
-- ============================================
CREATE TABLE IF NOT EXISTS chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    chatbot_id UUID REFERENCES chatbots(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    keywords TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for chunks
CREATE INDEX IF NOT EXISTS idx_chunks_source_id ON chunks(source_id);
CREATE INDEX IF NOT EXISTS idx_chunks_chatbot_id ON chunks(chatbot_id);
CREATE INDEX IF NOT EXISTS idx_chunks_keywords ON chunks USING GIN(keywords);

-- ============================================
-- 8. CONVERSATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chatbot_id UUID REFERENCES chatbots(id) ON DELETE CASCADE,
    session_id VARCHAR(255) NOT NULL,
    user_name VARCHAR(255),
    user_email VARCHAR(255),
    user_ip VARCHAR(50),
    status VARCHAR(50) DEFAULT 'active',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for conversations
CREATE INDEX IF NOT EXISTS idx_conversations_chatbot_id ON conversations(chatbot_id);
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at);

-- ============================================
-- 9. MESSAGES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    chatbot_id UUID REFERENCES chatbots(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for messages
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_chatbot_id ON messages(chatbot_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

-- ============================================
-- 10. INTEGRATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS integrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chatbot_id UUID REFERENCES chatbots(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    config JSONB NOT NULL DEFAULT '{}',
    enabled BOOLEAN DEFAULT true,
    webhook_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for integrations
CREATE INDEX IF NOT EXISTS idx_integrations_chatbot_id ON integrations(chatbot_id);
CREATE INDEX IF NOT EXISTS idx_integrations_type ON integrations(type);

-- ============================================
-- 11. INTEGRATION LOGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS integration_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chatbot_id UUID REFERENCES chatbots(id) ON DELETE CASCADE,
    integration_id UUID REFERENCES integrations(id) ON DELETE CASCADE,
    event VARCHAR(100) NOT NULL,
    details JSONB DEFAULT '{}',
    success BOOLEAN DEFAULT true,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for integration_logs
CREATE INDEX IF NOT EXISTS idx_integration_logs_chatbot_id ON integration_logs(chatbot_id);
CREATE INDEX IF NOT EXISTS idx_integration_logs_integration_id ON integration_logs(integration_id);
CREATE INDEX IF NOT EXISTS idx_integration_logs_timestamp ON integration_logs(timestamp);

-- ============================================
-- 12. NOTIFICATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'normal',
    read BOOLEAN DEFAULT false,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for notifications
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(read);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at);

-- ============================================
-- 13. LOGIN HISTORY TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS login_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) REFERENCES users(id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address VARCHAR(50),
    user_agent TEXT,
    location VARCHAR(255),
    success BOOLEAN DEFAULT true,
    failure_reason TEXT
);

-- Create indexes for login_history
CREATE INDEX IF NOT EXISTS idx_login_history_user_id ON login_history(user_id);
CREATE INDEX IF NOT EXISTS idx_login_history_timestamp ON login_history(timestamp);

-- ============================================
-- 14. API KEYS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    key_prefix VARCHAR(20) NOT NULL,
    user_id VARCHAR(100) REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    last_used_at TIMESTAMP WITH TIME ZONE,
    usage_count INTEGER DEFAULT 0,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

-- Create indexes for api_keys
CREATE INDEX IF NOT EXISTS idx_api_keys_key_hash ON api_keys(key_hash);
CREATE INDEX IF NOT EXISTS idx_api_keys_user_id ON api_keys(user_id);

-- ============================================
-- 15. WEBHOOKS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS webhooks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) REFERENCES users(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    events TEXT[] DEFAULT '{}',
    secret VARCHAR(255) NOT NULL,
    enabled BOOLEAN DEFAULT true,
    last_triggered_at TIMESTAMP WITH TIME ZONE,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for webhooks
CREATE INDEX IF NOT EXISTS idx_webhooks_user_id ON webhooks(user_id);

-- ============================================
-- 16. SYSTEM LOGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS system_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    details JSONB DEFAULT '{}',
    user_id VARCHAR(100),
    ip_address VARCHAR(50),
    endpoint VARCHAR(255),
    method VARCHAR(10),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for system_logs
CREATE INDEX IF NOT EXISTS idx_system_logs_level ON system_logs(level);
CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp ON system_logs(timestamp);

-- ============================================
-- 17. ERRORS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS errors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    error_type VARCHAR(255) NOT NULL,
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    endpoint VARCHAR(255),
    method VARCHAR(10),
    user_id VARCHAR(100),
    occurrence_count INTEGER DEFAULT 1,
    first_occurred_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_occurred_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved BOOLEAN DEFAULT false,
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for errors
CREATE INDEX IF NOT EXISTS idx_errors_error_type ON errors(error_type);
CREATE INDEX IF NOT EXISTS idx_errors_resolved ON errors(resolved);

-- ============================================
-- 18. PAYMENT GATEWAY SETTINGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS payment_gateway_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider VARCHAR(50) NOT NULL,
    api_key VARCHAR(255),
    store_id VARCHAR(255),
    test_mode BOOLEAN DEFAULT true,
    config JSONB DEFAULT '{}',
    enabled BOOLEAN DEFAULT false,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- FUNCTIONS & TRIGGERS
-- ============================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_chatbots_updated_at BEFORE UPDATE ON chatbots
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_integrations_updated_at BEFORE UPDATE ON integrations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- ROW LEVEL SECURITY (RLS) - Optional
-- ============================================

-- Enable RLS on tables (can be enabled later)
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE chatbots ENABLE ROW LEVEL SECURITY;
-- etc.

-- ============================================
-- END OF SCHEMA
-- ============================================
