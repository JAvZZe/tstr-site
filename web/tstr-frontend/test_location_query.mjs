import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://haimjeaetrsaauitrhfy.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ1NDUzMTMsImV4cCI6MjA1MDEyMTMxM30.a4z9mqyKFiB-GgW_1sF5VcNlqjdMD-1h-RIu5WUwCos'
)

const { data: listings, error } = await supabase
  .from('listings')
  .select(`
    id,
    company_name,
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
  .limit(5)

if (error) {
  console.error('Error:', error)
} else {
  console.log('Sample listings:')
  listings.forEach(l => {
    console.log('\n---')
    console.log(`Company: ${l.company_name}`)
    console.log(`Location data:`, JSON.stringify(l.location, null, 2))
  })
}
