import { createClient } from '@supabase/supabase-js'

// Use service role key to bypass RLS
const supabase = createClient(
  'https://haimjeaetrsaauitrhfy.supabase.co',
  'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2'
)

// Check locations table with service role
const { data: locations, error: locErr } = await supabase
  .from('locations')
  .select('id, name, slug, level')
  .limit(10)

if (locErr) {
  console.error('Locations error:', locErr)
} else {
  console.log(`Found ${locations.length} locations:`)
  locations?.forEach(l => {
    console.log(`  ${l.id}: ${l.name} (${l.level})`)
  })
}

// Check if the specific location_id exists
const { data: specificLoc, error: specErr } = await supabase
  .from('locations')
  .select('*')
  .eq('id', '0b7795f4-9ca1-4630-87d9-b94ce4d2a969')
  .single()

console.log('\nSpecific location (0b7795f4-9ca1-4630-87d9-b94ce4d2a969):')
console.log(specificLoc)
