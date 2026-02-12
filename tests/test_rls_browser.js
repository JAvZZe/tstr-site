// Test RLS Policy Functionality
// Run this in browser console on https://tstr.directory/submit page
// Tests if the RLS policies allow anonymous form submissions

function testRLSPolicies() {
  console.log('🧪 Testing RLS Policy Functionality...');

  // Test 1: Check if form exists
  const form = document.querySelector('form');
  if (!form) {
    console.error('❌ No form found on page');
    return;
  }
  console.log('✅ Form found');

  // Test 2: Fill form with test data
  const businessNameInput = document.querySelector('input[name="businessName"]');
  const emailInput = document.querySelector('input[name="email"]');
  const websiteInput = document.querySelector('input[name="website"]');
  const submitButton = document.querySelector('button[type="submit"]');

  if (!businessNameInput || !emailInput || !websiteInput || !submitButton) {
    console.error('❌ Required form fields not found');
    return;
  }

  // Fill with test data
  businessNameInput.value = 'Test RLS Policy Lab';
  emailInput.value = 'test@rls-policy-test.com';
  websiteInput.value = 'https://test-rls-policy.com';
  console.log('✅ Form filled with test data');

  // Test 3: Submit form (commented out to prevent actual submission)
  console.log('⚠️  To test submission: Click submit button manually');
  console.log('Expected result: Success message should appear');
  console.log('Database check: New listing should appear with status="pending"');

  console.log('✅ RLS Policy Test Setup Complete');
}

// Run the test
testRLSPolicies();