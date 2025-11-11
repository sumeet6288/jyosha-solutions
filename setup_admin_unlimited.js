// Setup Admin User with Unlimited Features and Permanent Subscription
db = db.getSiblingDB('chatbase_db');

const adminUpdate = {
  $set: {
    // Set Enterprise plan with permanent access
    plan_id: 'enterprise',
    lifetime_access: true,
    subscription_ends_at: null,
    plan_start_date: new Date().toISOString(),
    
    // Set unlimited custom limits
    custom_limits: {
      max_chatbots: 999999,
      max_messages_per_month: 999999999,
      max_file_uploads: 999999,
      max_website_sources: 999999,
      max_text_sources: 999999,
      max_storage_mb: 999999,
      max_ai_models: 999,
      max_integrations: 999
    },
    
    // Enable all feature flags
    feature_flags: {
      betaFeatures: true,
      advancedAnalytics: true,
      customBranding: true,
      apiAccess: true,
      prioritySupport: true,
      customDomain: true,
      whiteLabel: true,
      ssoEnabled: true
    },
    
    // Enable all permissions
    permissions: {
      canCreateChatbots: true,
      canDeleteChatbots: true,
      canViewAnalytics: true,
      canExportData: true,
      canManageIntegrations: true,
      canAccessAPI: true,
      canUploadFiles: true,
      canScrapeWebsites: true,
      canUseAdvancedFeatures: true,
      canInviteTeamMembers: true,
      canManageBilling: true
    },
    
    // Unlimited API rate limits
    api_rate_limits: {
      requests_per_minute: 999999,
      requests_per_hour: 999999,
      requests_per_day: 999999,
      burst_limit: 999999
    },
    
    // Verify email and enable all features
    email_verified: true,
    onboarding_completed: true,
    onboarding_progress: 100,
    lifecycle_stage: 'champion',
    
    // Update other important fields
    updated_at: new Date().toISOString(),
    admin_notes: 'Super Admin - Unlimited access to all features permanently'
  }
};

// Update the admin user
const result = db.users.updateOne(
  { email: 'admin@botsmith.com' },
  adminUpdate
);

print('\n✅ Admin User Updated Successfully!');
print('═══════════════════════════════════════════════════');
print('Email: admin@botsmith.com');
print('Password: admin123');
print('Plan: Enterprise (Permanent/Lifetime)');
print('Custom Limits: Unlimited Everything');
print('Feature Flags: All Enabled');
print('Permissions: Full Admin Access');
print('API Rate Limits: Unlimited');
print('═══════════════════════════════════════════════════');
print(`\nMatched: ${result.matchedCount} | Modified: ${result.modifiedCount}\n`);

// Verify the update
const admin = db.users.findOne({ email: 'admin@botsmith.com' });
print('Current Admin Plan:', admin.plan_id);
print('Lifetime Access:', admin.lifetime_access);
print('Max Chatbots:', admin.custom_limits.max_chatbots);
print('Max Messages:', admin.custom_limits.max_messages_per_month);
print('All Feature Flags Enabled:', Object.values(admin.feature_flags).every(v => v === true));
print('All Permissions Enabled:', Object.values(admin.permissions).every(v => v === true));
