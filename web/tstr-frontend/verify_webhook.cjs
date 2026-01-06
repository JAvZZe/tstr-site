#!/usr/bin/env node
/**
 * Verify PayPal webhook configuration
 */

const https = require('https');
require('dotenv').config({ path: '.env' });

const CLIENT_ID = process.env.PAYPAL_CLIENT_ID;
const SECRET = process.env.PAYPAL_CLIENT_SECRET;
const WEBHOOK_ID = process.env.PAYPAL_WEBHOOK_ID;
const MODE = process.env.PAYPAL_MODE || 'sandbox';

console.log('=== Verifying PayPal Webhook Configuration ===\n');
console.log(`Mode: ${MODE}`);
console.log(`Webhook ID: ${WEBHOOK_ID}`);

if (!CLIENT_ID || !SECRET || !WEBHOOK_ID) {
    console.error('Missing PayPal configuration');
    process.exit(1);
}

const auth = Buffer.from(`${CLIENT_ID}:${SECRET}`).toString('base64');
const hostname = MODE === 'live' ? 'api-m.paypal.com' : 'api-m.sandbox.paypal.com';

function request(path, method = 'GET', headers = {}, body = null) {
    return new Promise((resolve, reject) => {
        const req = https.request({
            hostname,
            path,
            method,
            headers: {
                'Authorization': `Basic ${auth}`,
                'Content-Type': 'application/json',
                ...headers
            }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    resolve({ status: res.statusCode, data: json });
                } catch (e) {
                    resolve({ status: res.statusCode, data });
                }
            });
        });

        req.on('error', reject);
        if (body) req.write(JSON.stringify(body));
        req.end();
    });
}

async function main() {
    // Get access token
    console.log('\n1. Getting access token...');
    const tokenRes = await new Promise((resolve, reject) => {
        const req = https.request({
            hostname,
            path: '/v1/oauth2/token',
            method: 'POST',
            headers: {
                'Authorization': `Basic ${auth}`,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve(JSON.parse(data)));
        });
        req.write('grant_type=client_credentials');
        req.end();
    });

    if (!tokenRes.access_token) {
        console.error('Failed to get access token:', tokenRes);
        return;
    }
    console.log('✅ Access token received');

    // Verify webhook exists
    console.log('\n2. Verifying webhook configuration...');
    const webhookRes = await request(`/v1/notifications/webhooks/${WEBHOOK_ID}`, 'GET', {
        'Authorization': `Bearer ${tokenRes.access_token}`
    });

    console.log(`Status: ${webhookRes.status}`);

    if (webhookRes.status === 200) {
        console.log('✅ Webhook exists and is configured');
        console.log(`URL: ${webhookRes.data.url}`);
        console.log(`Status: ${webhookRes.data.status}`);
        console.log(`Events: ${webhookRes.data.event_types.map(e => e.name).join(', ')}`);
    } else {
        console.log('❌ Webhook verification failed:');
        console.log(JSON.stringify(webhookRes.data, null, 2));
    }

    // List all webhooks
    console.log('\n3. Listing all webhooks...');
    const listRes = await request('/v1/notifications/webhooks', 'GET', {
        'Authorization': `Bearer ${tokenRes.access_token}`
    });

    if (listRes.status === 200) {
        console.log(`Found ${listRes.data.webhooks.length} webhook(s):`);
        listRes.data.webhooks.forEach((hook, i) => {
            console.log(`${i + 1}. ${hook.url} (ID: ${hook.id})`);
        });
    } else {
        console.log('❌ Failed to list webhooks');
    }

    console.log('\n=== Webhook Verification Summary ===');
    if (webhookRes.status === 200) {
        console.log('✅ Webhook is properly configured in PayPal');
        console.log('✅ Ready to receive subscription events');
        console.log('✅ Edge Function will process events (auth handled internally)');
    } else {
        console.log('❌ Webhook configuration issue');
    }

    console.log('\n📋 Webhook Processing:');
    console.log('- PayPal sends events to Supabase Edge Function');
    console.log('- Function verifies signature (live mode only)');
    console.log('- Updates user subscription status in database');
    console.log('- Logs payment events');
}