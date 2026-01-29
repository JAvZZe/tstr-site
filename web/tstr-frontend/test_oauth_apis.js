#!/usr/bin/env node
// Test script for LinkedIn OAuth API endpoints
// Run with: node test_oauth_apis.js

const BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://tstr.directory'
  : 'http://localhost:4321';

async function testEndpoint(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  console.log(`\n🧪 Testing: ${endpoint}`);

  try {
    const response = await fetch(url, {
      method: options.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      body: options.body ? JSON.stringify(options.body) : undefined
    });

    console.log(`Status: ${response.status} ${response.statusText}`);

    if (response.ok) {
      const data = await response.json();
      console.log('✅ Response:', JSON.stringify(data, null, 2));
      return { success: true, data };
    } else {
      const error = await response.text();
      console.log('❌ Error:', error);
      return { success: false, error };
    }
  } catch (error) {
    console.log('❌ Network Error:', error.message);
    return { success: false, error: error.message };
  }
}

async function runTests() {
  console.log('🔗 LinkedIn OAuth API Tests');
  console.log('===========================\n');

  console.log('⚠️  Note: These tests require the Astro dev server to be running');
  console.log('   Run: npm run dev (in web/tstr-frontend/)');
  console.log('   Then visit: http://localhost:4321/login\n');

  try {
    // Test 1: Check if login page loads
    console.log('Test 1: Login page accessibility');
    const loginResponse = await fetch(`${BASE_URL}/login`);
    if (loginResponse.ok) {
      console.log('✅ Login page accessible');
    } else {
      console.log('❌ Login page not accessible');
    }

    // Test 2: Check if signup page loads
    console.log('\nTest 2: Signup page accessibility');
    const signupResponse = await fetch(`${BASE_URL}/signup`);
    if (signupResponse.ok) {
      console.log('✅ Signup page accessible');
    } else {
      console.log('❌ Signup page not accessible');
    }

    // Test 3: Test claim-listing endpoint (should require auth)
    await testEndpoint('/api/claim-listing', {
      method: 'POST',
      body: { listingId: 'test-id' }
    });

    // Test 4: Test verify-claim endpoint (should require auth)
    await testEndpoint('/api/verify-claim', {
      method: 'POST',
      body: { token: 'test-token', code: '123456' }
    });

  } catch (_error) {
    console.log('\n❌ Tests failed - Dev server not running?');
    console.log('To test manually:');
    console.log('1. Start dev server: cd web/tstr-frontend && npm run dev');
    console.log('2. Visit: http://localhost:4321/login');
    console.log('3. Check LinkedIn OAuth button is present');
    console.log('4. Test signup page: http://localhost:4321/signup');
  }

  console.log('\n📋 Manual Test Checklist:');
  console.log('□ Login page loads and shows LinkedIn button');
  console.log('□ Signup page loads and shows LinkedIn button');
  console.log('□ LinkedIn buttons have proper styling');
  console.log('□ Clicking buttons initiates OAuth flow (after config)');
  console.log('□ API endpoints return proper auth errors');
}

// Run tests if this script is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runTests().catch(console.error);
}

export { testEndpoint, runTests };