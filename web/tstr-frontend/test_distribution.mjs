import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://haimjeaetrsaauitrhfy.supabase.co',
  'sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO'
)

// Get all active listings with location joins
const { data: listings, error } = await supabase
  .from('listings')
  .select(`
    id,
    location:location_id (
      id,
      name,
      slug,
      level,
      parent:parent_id (
        id,
        name,
        slug,
        level,
        parent:parent_id (
          id,
          name,
          slug,
          level
        )
      )
    )
  `)
  .eq('status', 'active')

console.log(`Total listings: ${listings.length}`)

// Extract countries using the same logic as frontend
const getCountryFromLocation = (location) => {
  if (!location) return null
  if (location.level === 'country') {
    return { name: location.name, slug: location.slug }
  }
  let current = location
  while (current && current.level !== 'country') {
    current = current.parent
  }
  return current ? { name: current.name, slug: current.slug } : null
}

const countries = [...new Map(
  listings
    .map(l => getCountryFromLocation(l.location))
    .filter(Boolean)
    .map(c => [c.slug, c])
).values()]

console.log(`\nUnique countries found: ${countries.length}`)
countries.forEach(c => {
  const count = listings.filter(l => {
    const country = getCountryFromLocation(l.location)
    return country?.slug === c.slug
  }).length
  console.log(`  ${c.name}: ${count} listings`)
})
