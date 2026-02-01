const { createClient } = require('@supabase/supabase-js');

// Configuration
const SUPABASE_URL = 'https://haimjeaetrsaauitrhfy.supabase.co';
const SUPABASE_SERVICE_KEY = 'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2'; // From previous context

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY, {
    auth: {
        autoRefreshToken: false,
        persistSession: false
    }
});

const TARGET_USERS = [
    { email: 'al@tstr.directory', role: 'super_admin' },
    { email: 'tstr1.site@gmail.com', role: 'super_admin' },
    { email: 'tstr.site1@gmail.com', role: 'super_admin' }
];

const TARGET_PASSWORD = '@Pkpz#F5*J%j8v';

async function initAdmins() {
    console.log('Starting Admin Initialization...');

    for (const target of TARGET_USERS) {
        console.log(`Processing ${target.email}...`);

        // 1. Check if user exists (by listing, as getUser requires ID/JWT, list is Admin-only)
        // Actually, listUsers can filter? Not easily by email in one go, but we can iterate or try create.
        // Easiest is to try to create, if catch error "already registered", then update.

        let userId = null;

        try {
            const { data: { users }, error } = await supabase.auth.admin.listUsers();
            if (error) throw error;

            const existing = users.find(u => u.email === target.email);
            if (existing) {
                userId = existing.id;
                console.log(`User exists: ${userId}`);
            }
        } catch (e) {
            console.error('Error listing users:', e);
        }

        if (!userId) {
            // Create User
            try {
                const { data, error } = await supabase.auth.admin.createUser({
                    email: target.email,
                    password: TARGET_PASSWORD,
                    email_confirm: true,
                    user_metadata: { role: target.role }
                });
                if (error) throw error;
                console.log(`Created user: ${data.user.id}`);
            } catch (e) {
                console.error(`Failed to create ${target.email}:`, e.message);
            }
        } else {
            // Update User
            try {
                const { data, error } = await supabase.auth.admin.updateUserById(userId, {
                    password: TARGET_PASSWORD,
                    email_confirm: true,
                    user_metadata: { role: target.role }
                });
                if (error) throw error;
                console.log(`Updated user: ${userId} (Password & Role set)`);
            } catch (e) {
                console.error(`Failed to update ${target.email}:`, e.message);
            }
        }
    }

    console.log('Initialization Complete.');
}

initAdmins();
