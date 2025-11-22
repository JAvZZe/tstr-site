#!/usr/bin/env node
/**
 * Quick test to verify Supabase connection with new API keys
 */

import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://haimjeaetrsaauitrhfy.supabase.co';
const SUPABASE_KEY = 'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';

console.log('Testing Supabase connection with new API key format...\n');
console.log(`URL: ${SUPABASE_URL}`);
console.log(`Key: ${SUPABASE_KEY.substring(0, 20)}...`);

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// Test 1: Check if claims table exists
console.log('\n--- Test 1: Check claims table ---');
try {
  const { data, error, count } = await supabase
    .from('claims')
    .select('*', { count: 'exact', head: true });
  
  if (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
  
  console.log(`✅ Claims table exists with ${count} rows`);
} catch (e) {
  console.error('❌ Failed:', e.message);
  process.exit(1);
}

// Test 2: Try to insert a test claim
console.log('\n--- Test 2: Insert test claim ---');
try {
  const testClaim = {
    provider_name: 'Test Lab Connection',
    contact_name: 'Test User',
    business_email: `test-${Date.now()}@example.com`,
    phone: '+1 555-0000'
  };
  
  const { data, error } = await supabase
    .from('claims')
    .insert([testClaim])
    .select();
  
  if (error) {
    console.error('❌ Insert failed:', error.message);
    console.error('Details:', error);
    process.exit(1);
  }
  
  console.log('✅ Insert successful!');
  console.log('Claim ID:', data[0].id);
  console.log('Data:', JSON.stringify(data[0], null, 2));
  
} catch (e) {
  console.error('❌ Failed:', e.message);
  process.exit(1);
}

console.log('\n✅ All connection tests passed!');
console.log('\nNew API key format is working correctly.');
