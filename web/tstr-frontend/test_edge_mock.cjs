#!/usr/bin/env node
/**
 * Test Edge Function with mock authentication
 */

const https = require('https');

const url = 'https://haimjeaetrsaauitrhfy.supabase.co/functions/v1/paypal-create-subscription';

// Mock JWT token (this won't work for real auth, but let's see what error we get)
const mockAuthToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';

const postData = JSON.stringify({
  tier: 'professional',
  return_url: 'https://tstr.directory/checkout/success',
  cancel_url: 'https://tstr.directory/checkout/cancel'
});

const options = {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData),
    'Authorization': `Bearer ${mockAuthToken}`,
    'apikey': 'sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO'
  }
};

console.log('=== Testing Edge Function with Mock Auth ===\n');

const req = https.request(url, options, (res) => {
  console.log(`Status: ${res.statusCode}`);
  console.log(`Headers:`, res.headers);

  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    console.log('Response body:');
    try {
      const json = JSON.parse(data);
      console.log(JSON.stringify(json, null, 2));
    } catch (e) {
      console.log(data);
    }
  });
});

req.on('error', (e) => {
  console.error('Request failed:', e.message);
});

req.write(postData);
req.end();