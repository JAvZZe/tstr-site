const { createClient } = require('@supabase/supabase-js');

// Configuration
const SUPABASE_URL = 'https://haimjeaetrsaauitrhfy.supabase.co';
const SUPABASE_SERVICE_KEY = 'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

const EMAIL = 'tstr.site1@gmail.com';

async function verifyUser() {
    console.log(`Inspecting user: ${EMAIL}`);

    const { data: { users }, error } = await supabase.auth.admin.listUsers();

    if (error) {
        console.error('Error listing users:', error);
        return;
    }

    const user = users.find(u => u.email === EMAIL);

    if (!user) {
        console.error('User NOT FOUND in database.');
        return;
    }

    console.log('User Found:');
    console.log('ID:', user.id);
    console.log('Email Confirmed At:', user.email_confirmed_at);
    console.log('Last Sign In:', user.last_sign_in_at);
    console.log('User Metadata:', JSON.stringify(user.user_metadata, null, 2));
    console.log('App Metadata:', JSON.stringify(user.app_metadata, null, 2));
    console.log('Role:', user.role);
    console.log('Aud:', user.aud);

    // Verify Password
    console.log('Attempting login with provided password...');
    const { data: signinData, error: signinError } = await supabase.auth.signInWithPassword({
        email: EMAIL,
        password: '@Pkpz#F5*J%j8v'
    });

    if (signinError) {
        console.error('Login FAILED:', signinError.message);
    } else {
        console.log('Login SUCCEEDED!');
        console.log('Session User Metadata:', JSON.stringify(signinData.session.user.user_metadata, null, 2));
    }
}

verifyUser();
