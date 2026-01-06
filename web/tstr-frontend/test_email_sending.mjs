#!/usr/bin/env node
/**
 * Test email sending functionality by simulating API calls
 */

import { sendEmail, createDraftSaveEmail, createVerificationEmail } from './src/lib/email.ts';

// Set environment variables for testing
process.env.RESEND_API_KEY = 're_eYDmQ352_2mH5o58xtSEBRA6YSbt1od9s';
process.env.RESEND_FROM_EMAIL = 'noreply@tstr.directory';

console.log('=== Testing Email Sending Functionality ===\n');

// Test 1: Draft Save Email
console.log('--- Test 1: Sending Draft Save Email ---');

const draftEmail = createDraftSaveEmail('test-resume-token-123', '2026-01-15T10:00:00Z');
console.log('Subject:', draftEmail.subject);
console.log('To: test@example.com');

try {
  const draftResult = await sendEmail('test@example.com', draftEmail);
  console.log('Result:', draftResult.success ? '✅ SUCCESS' : '❌ FAILED');
  if (!draftResult.success) {
    console.log('Error:', draftResult.error);
  }
} catch (error) {
  console.log('Exception:', error.message);
}

console.log('\n--- Test 2: Sending Verification Email ---');

const verifyEmail = createVerificationEmail('Test Laboratory Inc.', 'ABC123', '2026-01-15T10:00:00Z');
console.log('Subject:', verifyEmail.subject);
console.log('To: test2@example.com');

try {
  const verifyResult = await sendEmail('test2@example.com', verifyEmail);
  console.log('Result:', verifyResult.success ? '✅ SUCCESS' : '❌ FAILED');
  if (!verifyResult.success) {
    console.log('Error:', verifyResult.error);
  }
} catch (error) {
  console.log('Exception:', error.message);
}

console.log('\n=== Email Sending Tests Complete ===');
console.log('📧 Check your email inbox for test messages');
console.log('💡 If emails fail, check Resend dashboard at https://resend.com');