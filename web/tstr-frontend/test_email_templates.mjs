#!/usr/bin/env node
/**
 * Test email utility functions directly
 */

import { createDraftSaveEmail, createVerificationEmail, generateVerificationToken } from './src/lib/email.ts';

console.log('=== Testing Email Utility Functions ===\n');

// Test 1: Generate verification token
console.log('--- Test 1: Verification Token Generation ---');
const token = generateVerificationToken();
console.log(`Generated token: ${token}`);
console.log(`Token length: ${token.length}`);
console.log(`Token format: ${/^[A-Z0-9]{6}$/.test(token) ? '✅ Valid' : '❌ Invalid'}`);

console.log('\n--- Test 2: Draft Save Email Template ---');
const draftEmail = createDraftSaveEmail('test-token-123', '2026-01-15T10:00:00Z');
console.log('Subject:', draftEmail.subject);
console.log('Contains token:', draftEmail.html.includes('test-token-123') ? '✅ Yes' : '❌ No');
console.log('Contains expiration:', draftEmail.html.includes('2026-01-15') ? '✅ Yes' : '❌ No');
console.log('HTML length:', draftEmail.html.length);

console.log('\n--- Test 3: Verification Email Template ---');
const verifyEmail = createVerificationEmail('Test Company Inc.', 'ABC123', '2026-01-15T10:00:00Z');
console.log('Subject:', verifyEmail.subject);
console.log('Contains company name:', verifyEmail.html.includes('Test Company Inc.') ? '✅ Yes' : '❌ No');
console.log('Contains token:', verifyEmail.html.includes('ABC123') ? '✅ Yes' : '❌ No');
console.log('HTML length:', verifyEmail.html.length);

console.log('\n=== Email Template Tests Complete ===');
console.log('✅ All email templates generated successfully');
console.log('📧 Templates are ready for Resend API integration');