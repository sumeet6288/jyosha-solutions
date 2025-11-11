// Fix Admin Subscription in subscriptions collection
db = db.getSiblingDB('chatbase_db');

// Update or create the subscription for admin user
const result = db.subscriptions.updateOne(
  { user_id: 'admin-001' },
  {
    $set: {
      plan_id: 'enterprise',
      status: 'active',
      started_at: new Date(),
      expires_at: null, // Never expires
      auto_renew: false,
      billing_cycle: 'lifetime', // Permanent
      usage: {
        chatbots_count: 0,
        messages_this_month: 0,
        file_uploads_count: 0,
        website_sources_count: 0,
        text_sources_count: 0,
        last_reset: new Date()
      }
    }
  },
  { upsert: true }
);

print('\n✅ Admin Subscription Updated!');
print('═══════════════════════════════════════════════════');
print('Matched:', result.matchedCount);
print('Modified:', result.modifiedCount);
print('Upserted:', result.upsertedCount);
print('═══════════════════════════════════════════════════');

// Verify the update
const subscription = db.subscriptions.findOne({ user_id: 'admin-001' });
print('\nUpdated Subscription:');
print('User ID:', subscription.user_id);
print('Plan ID:', subscription.plan_id);
print('Status:', subscription.status);
print('Expires At:', subscription.expires_at || 'Never (Permanent)');
print('Billing Cycle:', subscription.billing_cycle);
