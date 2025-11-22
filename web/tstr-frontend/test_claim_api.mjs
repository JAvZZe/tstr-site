#!/usr/bin/env node
/**
 * Test script for claim submission API endpoint
 * Tests both local dev server and direct Supabase connection
 * 
 * Usage:
 *   node test_claim_api.mjs
 *   node test_claim_api.mjs --live  (test against production)
 */

import { createClient } from '@supabase/supabase-js';

const isLive = process.argv.includes('--live');
const API_URL = isLive 
  ? 'https://tstr.site/api/claim_submission'
  : 'http://localhost:4321/api/claim_submission';

// Supabase credentials (for direct DB verification)
const SUPABASE_URL = 'https://haimjeaetrsaauitrhfy.supabase.co';
const SUPABASE_KEY = 'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';

console.log('=== TSTR.site Claims API Test ===\n');
console.log(`Testing: ${isLive ? 'PRODUCTION' : 'LOCAL DEV'}`);
console.log(`Endpoint: ${API_URL}\n`);

// Test payload
const testClaim = {
  provider_name: 'Test Laboratory Inc.',
  contact_name: 'John Smith',
  business_email: `test-${Date.now()}@example.com`,
  phone: '+1 (555) 123-4567'
};

console.log('Test Claim Data:');
console.log(JSON.stringify(testClaim, null, 2));
console.log('\n--- Step 1: Testing API Endpoint ---');

try {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(testClaim)
  });

  const data = await response.json();
  
  console.log(`\nStatus: ${response.status} ${response.statusText}`);
  console.log('Response:', JSON.stringify(data, null, 2));

  if (!response.ok) {
    console.error('\n❌ API request failed!');
    console.error('Details:', data);
    process.exit(1);
  }

  console.log('\n✅ API request successful!');
  
  if (data.id) {
    console.log(`\nClaim ID: ${data.id}`);
    
    // Step 2: Verify in database
    console.log('\n--- Step 2: Verifying in Database ---');
    
    const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
    
    const { data: claim, error } = await supabase
      .from('claims')
      .select('*')
      .eq('id', data.id)
      .single();
    
    if (error) {
      console.error('❌ Database verification failed:', error.message);
      process.exit(1);
    }
    
    console.log('\n✅ Claim found in database:');
    console.log(JSON.stringify(claim, null, 2));
    
    // Step 3: Test validation
    console.log('\n--- Step 3: Testing Validation ---');
    
    // Test missing required field
    console.log('\n3a. Testing missing email field...');
    const invalidResponse1 = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        provider_name: 'Test Lab',
        contact_name: 'John Doe'
        // business_email missing
      })
    });
    const invalidData1 = await invalidResponse1.json();
    
    if (invalidResponse1.status === 400) {
      console.log('✅ Correctly rejected missing email:', invalidData1.error);
    } else {
      console.log('⚠️  Expected 400 error, got:', invalidResponse1.status);
    }
    
    // Test invalid email format
    console.log('\n3b. Testing invalid email format...');
    const invalidResponse2 = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        provider_name: 'Test Lab',
        contact_name: 'John Doe',
        business_email: 'not-an-email'
      })
    });
    const invalidData2 = await invalidResponse2.json();
    
    if (invalidResponse2.status === 400) {
      console.log('✅ Correctly rejected invalid email:', invalidData2.error);
    } else {
      console.log('⚠️  Expected 400 error, got:', invalidResponse2.status);
    }
    
    console.log('\n=== All Tests Passed! ===\n');
    console.log(`View claim in Supabase dashboard:`);
    console.log(`https://haimjeaetrsaauitrhfy.supabase.co/project/_/editor/${claim.id}\n`);
    
  } else {
    console.warn('⚠️  No claim ID in response');
  }
  
} catch (error) {
  console.error('\n❌ Test failed with error:');
  console.error(error.message);
  
  if (error.code === 'ECONNREFUSED') {
    console.error('\n💡 Make sure dev server is running:');
    console.error('   cd web/tstr-frontend && npm run dev');
  }
  
  process.exit(1);
}
