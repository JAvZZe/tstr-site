import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://haimjeaetrsaauitrhfy.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjkxODc3ODcsImV4cCI6MjA0NDc2Mzc4N30.H3iEFSlg4kPRIvAYExPmyUJyA_7_BiJnHO4GD6QmtHc';

const supabase = createClient(supabaseUrl, supabaseKey);

console.log('Querying TSTR database...\n');

// Get all listings with addresses
const { data: listings, error } = await supabase
  .from('listings')
  .select('id, business_name, address, location_id, category_id, status')
  .eq('status', 'active')
  .limit(50);

if (error) {
  console.error('Error:', error);
  process.exit(1);
}

console.log(`Total active listings: ${listings.length}\n`);

// Show sample addresses
console.log('=== SAMPLE ADDRESSES ===');
listings.slice(0, 10).forEach((listing, i) => {
  console.log(`${i + 1}. ${listing.business_name}`);
  console.log(`   Address: ${listing.address}`);
  console.log(`   location_id: ${listing.location_id}`);
  console.log('');
});

// Extract countries using the same logic as frontend
const extractCountry = (address) => {
  if (!address) return null;
  const parts = address.split(',').map(p => p.trim()).filter(p => p.length > 0);
  if (parts.length === 0) return null;

  let country = parts[parts.length - 1];
  if (/^\d+$/.test(country) && parts.length > 1) {
    country = parts[parts.length - 2];
  }
  country = country.replace(/\s+\d{4,}$/g, '').trim();
  return country;
};

const countries = [...new Set(listings.map(l => extractCountry(l.address)))].filter(Boolean);
console.log('\n=== EXTRACTED COUNTRIES ===');
countries.forEach((c, i) => console.log(`${i + 1}. ${c}`));
console.log(`\nTotal unique countries: ${countries.length}`);

// Check locations table
const { data: locations } = await supabase
  .from('locations')
  .select('*')
  .order('level', { ascending: true });

if (locations) {
  console.log('\n=== LOCATIONS TABLE ===');
  console.log(`Total locations in database: ${locations.length}`);
  const byLevel = locations.reduce((acc, loc) => {
    acc[loc.level] = (acc[loc.level] || 0) + 1;
    return acc;
  }, {});
  console.log('By level:', JSON.stringify(byLevel, null, 2));
}

// Check how many listings actually have location_id set
const withLocation = listings.filter(l => l.location_id !== null).length;
console.log(`\nListings with location_id set: ${withLocation}/${listings.length}`);
