#!/usr/bin/env node
/**
 * Analyze listings and suggest standard assignments
 */

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://haimjeaetrsaauitrhfy.supabase.co';
const supabaseKey = 'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';

const supabase = createClient(supabaseUrl, supabaseKey);

async function main() {
  console.log('🔍 Analyzing TSTR.site listings...\n');

  // Get categories
  const { data: categories, error: catError } = await supabase
    .from('categories')
    .select('id, name, slug')
    .order('name');

  if (catError) {
    console.error('Error fetching categories:', catError);
    return;
  }

  console.log('📊 Categories:');
  categories.forEach(cat => {
    console.log(`  - ${cat.name} (${cat.slug})`);
  });
  console.log();

  // Get listings by category
  const { data: listings, error: listError } = await supabase
    .from('listings')
    .select('id, business_name, category:category_id(id, name, slug), address')
    .eq('status', 'active')
    .order('business_name');

  if (listError) {
    console.error('Error fetching listings:', listError);
    return;
  }

  console.log(`📋 Total Active Listings: ${listings.length}\n`);

  // Group by category
  const byCategory = {};
  listings.forEach(listing => {
    const catName = listing.category?.name || 'Uncategorized';
    if (!byCategory[catName]) byCategory[catName] = [];
    byCategory[catName].push(listing);
  });

  console.log('📈 Listings by Category:');
  Object.entries(byCategory).forEach(([catName, catListings]) => {
    console.log(`\n  ${catName}: ${catListings.length} listings`);
    console.log('  ' + '-'.repeat(50));
    catListings.slice(0, 5).forEach(l => {
      console.log(`    • ${l.business_name}`);
      console.log(`      ${l.address || 'No address'}`);
    });
    if (catListings.length > 5) {
      console.log(`    ... and ${catListings.length - 5} more`);
    }
  });

  // Get standards
  const { data: standards, error: stdError } = await supabase
    .from('standards')
    .select('id, code, name, issuing_body, category:category_id(name)')
    .eq('is_active', true)
    .order('code');

  if (stdError) {
    console.error('Error fetching standards:', stdError);
    return;
  }

  console.log(`\n\n🎯 Available Standards: ${standards.length}`);
  
  // Group standards by category
  const stdByCategory = {};
  standards.forEach(std => {
    const catName = std.category?.name || 'General';
    if (!stdByCategory[catName]) stdByCategory[catName] = [];
    stdByCategory[catName].push(std);
  });

  console.log('\n📋 Standards by Category:');
  Object.entries(stdByCategory).forEach(([catName, catStandards]) => {
    console.log(`\n  ${catName}: ${catStandards.length} standards`);
    catStandards.forEach(s => {
      console.log(`    • ${s.code} - ${s.name}`);
    });
  });

  // Check existing capabilities
  const { data: capabilities, error: capError } = await supabase
    .from('listing_capabilities')
    .select('count');

  console.log(`\n\n📊 Current Capabilities: ${capabilities?.[0]?.count || 0}`);

  console.log('\n✅ Analysis complete!\n');
}

main().catch(console.error);
