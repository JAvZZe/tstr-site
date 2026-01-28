// Debug script for submit form 500 error
// Run this in browser console on https://tstr.directory/submit

async function debugSubmitForm() {
  console.log('🔍 Submit Form Debug - Testing Database Queries');
  console.log('================================================');

  // Test 1: Check Supabase connection
  console.log('1. Testing Supabase connection...');
  try {
    const { data, error } = await window.supabase.from('categories').select('count').limit(1);
    if (error) {
      console.error('❌ Supabase connection failed:', error);
      return;
    }
    console.log('✅ Supabase connected');
  } catch (e) {
    console.error('❌ Supabase error:', e);
    return;
  }

  // Test 2: Check categories table access
  console.log('2. Testing categories table access...');
  try {
    const { data: categories, error } = await window.supabase
      .from('categories')
      .select('name')
      .limit(5);

    if (error) {
      console.error('❌ Categories query failed:', error);
      console.log('This is likely the cause of the 500 error!');
      return;
    }
    console.log('✅ Categories accessible:', categories);
  } catch (e) {
    console.error('❌ Categories error:', e);
    return;
  }

  // Test 3: Check specific category lookup (what submit form does)
  console.log('3. Testing category lookup (Environmental Testing)...');
  try {
    const { data: categoryData, error: categoryError } = await window.supabase
      .from('categories')
      .select('id, name')
      .eq('name', 'Environmental Testing')
      .single();

    if (categoryError) {
      console.error('❌ Category lookup failed:', categoryError);
      console.log('Available categories:');
      const { data: allCats } = await window.supabase.from('categories').select('name');
      console.log(allCats);
      return;
    }
    console.log('✅ Category found:', categoryData);
  } catch (e) {
    console.error('❌ Category lookup error:', e);
    return;
  }

  // Test 4: Check locations table access
  console.log('4. Testing locations table access...');
  try {
    const { data: locations, error } = await window.supabase
      .from('locations')
      .select('name, level')
      .limit(5);

    if (error) {
      console.error('❌ Locations query failed:', error);
      console.log('This could also cause the 500 error!');
      return;
    }
    console.log('✅ Locations accessible:', locations);
  } catch (e) {
    console.error('❌ Locations error:', e);
    return;
  }

  // Test 5: Test the full submit flow (without actually submitting)
  console.log('5. Testing submit flow simulation...');
  try {
    // Simulate form data
    const testData = {
      business_name: 'Debug Test Lab',
      category: 'Environmental Testing',
      address: 'Test City, Test Country',
      website: 'https://debug-test.com'
    };

    console.log('Form data:', testData);

    // Step 1: Category lookup
    const { data: categoryData, error: categoryError } = await window.supabase
      .from('categories')
      .select('id, name')
      .eq('name', testData.category)
      .single();

    if (categoryError) {
      console.error('❌ Submit flow failed at category lookup:', categoryError);
      return;
    }
    console.log('✅ Category ID found:', categoryData.id);

    // Step 2: Location lookup
    const addressParts = testData.address.split(',').map(s => s.trim());
    const country = addressParts[addressParts.length - 1] || 'Unknown';

    const { data: countryLocation } = await window.supabase
      .from('locations')
      .select('id')
      .eq('name', country)
      .eq('level', 'country')
      .single();

    if (!countryLocation) {
      console.error('❌ Submit flow failed at location lookup - country not found');
      return;
    }
    console.log('✅ Location ID found:', countryLocation.id);

    console.log('✅ Full submit flow simulation successful!');
    console.log('The 500 error is NOT from database access issues.');

  } catch (e) {
    console.error('❌ Submit flow simulation error:', e);
  }

  console.log('🎯 If all tests pass but submit still fails, check:');
  console.log('   - JavaScript errors in submit form code');
  console.log('   - Network issues');
  console.log('   - Browser console for other errors');
}

// Make it available globally
window.debugSubmitForm = debugSubmitForm;

console.log('🔧 Run debugSubmitForm() to start debugging');
console.log('This will test all database queries the submit form makes');