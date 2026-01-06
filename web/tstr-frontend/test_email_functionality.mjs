#!/usr/bin/env node
/**
 * Test script for email functionality in claim system
 * Tests draft save emails and verification emails
 *
 * Usage:
 *   node test_email_functionality.mjs
 */

const API_BASE = 'http://localhost:4321';

console.log('=== TSTR.directory Email Functionality Test ===\n');

// Test 1: Draft Save Email
console.log('--- Test 1: Draft Save Email ---');

const draftClaim = {
  mode: 'save_draft',
  provider_name: 'Test Laboratory Inc.',
  contact_name: 'John Smith',
  business_email: 'test@example.com', // Use a real email you can check
  phone: '+1 (555) 123-4567'
};

console.log('Sending draft save request...');
console.log('Payload:', JSON.stringify(draftClaim, null, 2));

try {
  const draftResponse = await fetch(`${API_BASE}/api/claim`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(draftClaim)
  });

  const draftData = await draftResponse.json();

  console.log(`\nStatus: ${draftResponse.status} ${draftResponse.statusText}`);
  console.log('Response:', JSON.stringify(draftData, null, 2));

  if (draftResponse.ok && draftData.success) {
    console.log('\n✅ Draft save successful!');
    console.log('📧 Check your email for the resume link');
    console.log(`Resume token: ${draftData.resume_token}`);
  } else {
    console.log('\n❌ Draft save failed!');
  }

} catch (error) {
  console.error('\n❌ Draft save test failed:', error.message);
}

// Test 2: Verification Email (Anonymous Claim)
console.log('\n--- Test 2: Verification Email (Anonymous Claim) ---');

const verifyClaim = {
  provider_name: 'Another Test Lab',
  contact_name: 'Jane Doe',
  business_email: 'test2@example.com', // Use a real email you can check
  phone: '+1 (555) 987-6543',
  website: 'https://testlab.com'
};

console.log('Sending verification claim request...');
console.log('Payload:', JSON.stringify(verifyClaim, null, 2));

try {
  const verifyResponse = await fetch(`${API_BASE}/api/claim`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(verifyClaim)
  });

  const verifyData = await verifyResponse.json();

  console.log(`\nStatus: ${verifyResponse.status} ${verifyResponse.statusText}`);
  console.log('Response:', JSON.stringify(verifyData, null, 2));

  if (verifyResponse.ok && verifyData.success) {
    console.log('\n✅ Verification claim submitted!');
    console.log('📧 Check your email for the verification code');
    if (verifyData.claim?.token) {
      console.log(`Verification token: ${verifyData.claim.token}`);
    }
  } else {
    console.log('\n❌ Verification claim failed!');
  }

} catch (error) {
  console.error('\n❌ Verification test failed:', error.message);
}

console.log('\n=== Email Tests Complete ===');
console.log('📧 Check your email inbox for the test messages');
console.log('💡 If emails don\'t arrive, check the console logs for errors');