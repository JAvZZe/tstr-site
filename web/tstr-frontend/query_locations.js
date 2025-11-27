import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://haimjeaetrsaauitrhfy.supabase.co'
const supabaseKey = 'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2'

const supabase = createClient(supabaseUrl, supabaseKey)

async function queryLocations() {
  console.log('Querying locations table...')

  const { data, error } = await supabase
    .from('locations')
    .select('*')
    .order('level', { ascending: true })
    .order('name', { ascending: true })

  if (error) {
    console.error('Error querying locations:', error)
    return
  }

  console.log(`Found ${data.length} locations:`)
  console.log('Global level:')
  data.filter(loc => loc.level === 'global').forEach(loc => {
    console.log(`  - ${loc.name} (${loc.level})`)
  })

  console.log('Continent level:')
  data.filter(loc => loc.level === 'continent').forEach(loc => {
    console.log(`  - ${loc.name} (${loc.level})`)
  })

  console.log('Country level:')
  data.filter(loc => loc.level === 'country').forEach(loc => {
    console.log(`  - ${loc.name} (${loc.level})`)
  })

  console.log('Region level:')
  data.filter(loc => loc.level === 'region').forEach(loc => {
    console.log(`  - ${loc.name} (${loc.level})`)
  })

  console.log('City level:')
  data.filter(loc => loc.level === 'city').forEach(loc => {
    console.log(`  - ${loc.name} (${loc.level})`)
  })
}

queryLocations()