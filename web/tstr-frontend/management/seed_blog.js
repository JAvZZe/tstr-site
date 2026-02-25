import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://haimjeaetrsaauitrhfy.supabase.co';
const supabaseKey = 'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';
const supabase = createClient(supabaseUrl, supabaseKey);

const posts = [
  {
    slug: 'welcome-to-tstr-directory', 
    title: 'Welcome to the TSTR.directory Blog', 
    excerpt: 'Discover why we built the world\'s most comprehensive directory for specialist testing services.', 
    body: '# Welcome to TSTR.directory\n\nWe are excited to launch our new blog where we will share insights into the testing industry...\n\n## Why TSTR?\n\nFinding the right lab often takes weeks of manual searching. Our platform changes that.', 
    category: 'Lab Spotlight', 
    author: 'TSTR Team', 
    is_published: true, 
    reading_time_mins: 2
  },
  {
    slug: 'future-of-hydrogen-testing', 
    title: 'The Future of Hydrogen Infrastructure Testing', 
    excerpt: 'As the world pivots to clean energy, the demand for specialized hydrogen testing grows exponentially.', 
    body: '# The Future of Hydrogen Testing\n\nHydrogen represents a critical pillar of the global energy transition. However, ensuring safety and efficiency requires rigorous testing...\n\n### Challenges\n\n1. Material compatibility\n2. High-pressure sensors\n3. Leak detection', 
    category: 'Industry Trends', 
    author: 'Alex Vance', 
    is_published: true, 
    reading_time_mins: 5
  },
  {
    slug: 'official-launch-announcement', 
    title: 'TSTR Hub Official Launch Announcement', 
    excerpt: 'TSTR Hub officially enters the market to revolutionize how engineering firms find testing partners.', 
    body: '# Official Launch\n\nToday marks a significant milestone for the testing and certification industry. TSTR Hub is now live with over 150 verified laboratories...', 
    category: 'Press', 
    author: 'TSTR Press Office', 
    is_published: true, 
    reading_time_mins: 3
  }
];

async function seed() {
  console.log('🌱 Seeding blog posts...');
  for (const post of posts) {
    const { error } = await supabase.from('blog_posts').upsert(post, { onConflict: 'slug' });
    if (error) {
      console.error(`Error seeding ${post.slug}:`, error.message);
    } else {
      console.log(`✅ Seeded: ${post.slug}`);
    }
  }
  console.log('✨ Seeding complete!');
}

seed().catch(console.error);
