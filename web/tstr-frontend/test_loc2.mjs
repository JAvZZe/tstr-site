import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://haimjeaetrsaauitrhfy.supabase.co',
  'sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO'
)

const { data: listings, error } = await supabase
  .from('listings')
  .select(`
    *,
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
  .limit(3)

if (error) {
  console.error('Error:', error)
} else {
  console.log('Sample listings:')
  listings.forEach(l => {
    console.log('\n---')
    console.log(`ID: ${l.id}`)
    console.log(`Title: ${l.title}`)
    console.log(`Location data:`, JSON.stringify(l.location, null, 2))
  })
}
