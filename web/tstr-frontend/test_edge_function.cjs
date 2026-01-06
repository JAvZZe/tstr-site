#!/usr/bin/env node
/**
 * Test the paypal-create-subscription Edge Function directly
 */

const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://haimjeaetrsaauitrhfy.supabase.co';
const supabaseKey = 'sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO'; // anon key

const supabase = createClient(supabaseUrl, supabaseKey);

console.log('=== Testing PayPal Create Subscription Edge Function ===\n');

// First, let's check if we can authenticate
console.log('1. Testing authentication...');
supabase.auth.getSession().then(({ data: { session }, error }) => {
  if (error) {
    console.log('❌ Auth error:', error.message);
    return;
  }

  if (!session) {
    console.log('❌ No active session - user needs to be logged in');
    console.log('Please log in to TSTR.directory first, then run this test');
    return;
  }

  console.log('✅ User is authenticated');

  // Now test the Edge Function
  console.log('\n2. Testing Edge Function invocation...');
  supabase.functions.invoke('paypal-create-subscription', {
    body: {
      tier: 'professional',
      return_url: 'https://tstr.directory/checkout/success',
      cancel_url: 'https://tstr.directory/checkout/cancel'
    }
  }).then(({ data, error }) => {
    console.log('Edge Function Response:');

    if (error) {
      console.log('❌ Error:', error);
      console.log('Error details:', JSON.stringify(error, null, 2));
    } else {
      console.log('✅ Success!');
      console.log('Response:', JSON.stringify(data, null, 2));

      if (data?.approval_url) {
        console.log('✅ Approval URL received:', data.approval_url);
      } else {
        console.log('❌ No approval URL in response');
      }
    }
  }).catch(err => {
    console.log('❌ Function invocation failed:', err.message);
  });

}).catch(err => {
  console.log('❌ Session check failed:', err.message);
});