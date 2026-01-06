#!/usr/bin/env node
/**
 * Test Edge Function with proper authentication
 */

const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://haimjeaetrsaauitrhfy.supabase.co';
const supabaseKey = 'sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO'; // anon key

const supabase = createClient(supabaseUrl, supabaseKey);

console.log('=== Testing PayPal Edge Function with Auth ===\n');

// Test without authentication first
console.log('1. Testing without authentication (should fail)...');
supabase.functions.invoke('paypal-create-subscription', {
  body: {
    tier: 'professional',
    return_url: 'https://tstr.directory/checkout/success',
    cancel_url: 'https://tstr.directory/checkout/cancel'
  }
}).then(({ data, error }) => {
  console.log('Response (no auth):');
  if (error) {
    console.log('❌ Expected error:', error.message);
  } else {
    console.log('❌ Unexpected success:', data);
  }
}).catch(err => {
  console.log('❌ Function call failed:', err.message);
});

// Test with invalid tier
setTimeout(() => {
  console.log('\n2. Testing with invalid tier...');
  supabase.functions.invoke('paypal-create-subscription', {
    body: {
      tier: 'invalid',
      return_url: 'https://tstr.directory/checkout/success',
      cancel_url: 'https://tstr.directory/checkout/cancel'
    }
  }).then(({ data, error }) => {
    console.log('Response (invalid tier):');
    if (error) {
      console.log('❌ Error:', error);
    } else {
      console.log('Response:', JSON.stringify(data, null, 2));
    }
  }).catch(err => {
    console.log('❌ Function call failed:', err.message);
  });
}, 1000);