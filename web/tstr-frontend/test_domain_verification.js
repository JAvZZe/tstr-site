#!/usr/bin/env node
// Test script for domain verification logic
// Run with: node test_domain_verification.js

import { extractDomain, extractEmailDomain, canAutoClaim } from './src/lib/domain-verification.ts';

// Test cases for domain verification
const testCases = [
  {
    email: 'jane@supertestingservice.com',
    website: 'https://supertestingservice.com',
    expected: true,
    description: 'Exact domain match'
  },
  {
    email: 'user@supertestingservice.com',
    website: 'https://www.supertestingservice.com',
    expected: true,
    description: 'Match with www prefix'
  },
  {
    email: 'contact@testinglab.org',
    website: 'http://testinglab.org/about',
    expected: true,
    description: 'Match with path and http'
  },
  {
    email: 'user@gmail.com',
    website: 'https://supertestingservice.com',
    expected: false,
    description: 'Gmail vs corporate domain (should fail)'
  },
  {
    email: 'admin@subdomain.company.com',
    website: 'https://company.com',
    expected: false,
    description: 'Subdomain vs main domain (should fail for security)'
  }
];

console.log('🧪 Domain Verification Logic Tests');
console.log('==================================\n');

let passed = 0;
let total = testCases.length;

testCases.forEach((test, index) => {
  const result = canAutoClaim(test.email, test.website);
  const status = result === test.expected ? '✅ PASS' : '❌ FAIL';

  console.log(`Test ${index + 1}: ${test.description}`);
  console.log(`  Email: ${test.email}`);
  console.log(`  Website: ${test.website}`);
  console.log(`  Expected: ${test.expected}, Got: ${result}`);
  console.log(`  ${status}\n`);

  if (result === test.expected) passed++;
});

console.log(`📊 Results: ${passed}/${total} tests passed`);

if (passed === total) {
  console.log('🎉 All domain verification tests passed!');
} else {
  console.log('⚠️  Some tests failed. Please review the logic.');
}

// Test individual functions
console.log('\n🔍 Function Tests:');
console.log('extractEmailDomain("user@company.com"):', extractEmailDomain('user@company.com'));
console.log('extractDomain("https://www.company.com/path"):', extractDomain('https://www.company.com/path'));