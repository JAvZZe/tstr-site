import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://haimjeaetrsaauitrhfy.supabase.co';
const supabaseKey = 'sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO';

const supabase = createClient(supabaseUrl, supabaseKey);

async function checkSubscribers() {
  console.log('Checking newsletter_subscribers table...\n');
  const { data, error } = await supabase
    .from('newsletter_subscribers')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(5);

  if (error) {
    console.error('Error fetching subscribers:', error.message);
    process.exit(1);
  }

  if (!data || data.length === 0) {
    console.log('No subscribers found yet.');
  } else {
    console.log(`Found ${data.length} recent subscribers:`);
    data.forEach((sub, i) => {
      console.log(`${i + 1}. ${sub.first_name} ${sub.last_name} (${sub.email}) - Joined: ${sub.created_at}`);
    });
  }
}

checkSubscribers();
