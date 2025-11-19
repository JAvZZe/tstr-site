/**
 * Test script to verify form submission works with new RLS policy
 * Run this in browser console on /submit page
 */

async function testSubmission() {
  try {
    // Get the existing supabase client from the page
    const supabaseUrl = 'https://haimjeaetrsaauitrhfy.supabase.co';
    const supabaseKey = 'sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO'; // anon key
    
    const { createClient } = await import('https://esm.sh/@supabase/supabase-js@2');
    const supabase = createClient(supabaseUrl, supabaseKey);
    
    console.log('Supabase client created');
    
    // Test 1: Try to insert a test listing
    console.log('Test 1: Attempting to insert test listing...');
    
    const { data, error } = await supabase
      .from('listings')
      .insert([{
        business_name: 'Test Company ' + Date.now(),
        slug: 'test-company-' + Date.now(),
        category_id: 1,
        location_id: 1,
        website: 'https://test.example.com',
        email: 'test@example.com',
        address: 'Test City, Test Country',
        status: 'pending',
        verified: false,
        claimed: false,
        created_at: new Date().toISOString()
      }])
      .select();
    
    if (error) {
      console.error('INSERT failed:', error);
      console.error('Error details:', {
        code: error.code,
        message: error.message,
        details: error.details
      });
      return { success: false, error };
    }
    
    console.log('INSERT successful:', data);
    
    // Test 2: Verify we can't insert with wrong status
    console.log('\nTest 2: Attempting to insert with status=active (should fail)...');
    
    const { error: error2 } = await supabase
      .from('listings')
      .insert([{
        business_name: 'Should Fail ' + Date.now(),
        slug: 'should-fail-' + Date.now(),
        category_id: 1,
        location_id: 1,
        website: 'https://test.example.com',
        email: 'test@example.com',
        address: 'Test City, Test Country',
        status: 'active',  // Wrong status - should fail
        verified: false,
        claimed: false,
        created_at: new Date().toISOString()
      }]);
    
    if (error2) {
      console.log('Expected failure: Policy correctly blocked insert with status=active');
      console.error('Error:', error2.message);
    } else {
      console.error('WARNING: Policy did not block invalid status!');
    }
    
    return { success: true, message: 'RLS policy working correctly' };
    
  } catch (err) {
    console.error('Test error:', err);
    return { success: false, error: err.message };
  }
}

// Run the test
testSubmission().then(result => {
  console.log('\n=== TEST RESULT ===');
  console.log(JSON.stringify(result, null, 2));
});
