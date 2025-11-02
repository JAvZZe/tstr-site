import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://haimjeaetrsaauitrhfy.supabase.co',
  'sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO'
)

// First check the actual location_id values in listings
const { data: listings, error: listErr } = await supabase
  .from('listings')
  .select('id, location_id')
  .eq('status', 'active')
  .limit(5)

console.log('Listings location_id values:')
listings?.forEach(l => {
  console.log(`  ${l.id}: location_id = ${l.location_id}`)
})

// Now check if those IDs exist in locations table
const { data: locations, error: locErr } = await supabase
  .from('locations')
  .select('id, name, level')
  .limit(5)

console.log('\nLocations table sample:')
locations?.forEach(l => {
  console.log(`  ${l.id}: ${l.name} (${l.level})`)
})
