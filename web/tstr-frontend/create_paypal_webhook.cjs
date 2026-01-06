#!/usr/bin/env node
/**
 * Create PayPal webhook via API
 */

const https = require('https');
require('dotenv').config({ path: '.env' });

const CLIENT_ID = process.env.PAYPAL_CLIENT_ID;
const SECRET = process.env.PAYPAL_CLIENT_SECRET;
const MODE = process.env.PAYPAL_MODE || 'sandbox';

console.log('Creating PayPal Webhook...');
console.log(`Mode: ${MODE}`);

if (!CLIENT_ID || !SECRET) {
    console.error('Missing PayPal credentials');
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

    // Create webhook
    console.log('\n2. Creating webhook...');
    const webhookData = {
        url: "https://haimjeaetrsaauitrhfy.supabase.co/functions/v1/paypal-webhook",
        event_types: [
            { name: "BILLING.SUBSCRIPTION.ACTIVATED" },
            { name: "BILLING.SUBSCRIPTION.CANCELLED" },
            { name: "BILLING.SUBSCRIPTION.EXPIRED" },
            { name: "BILLING.SUBSCRIPTION.SUSPENDED" },
            { name: "PAYMENT.SALE.COMPLETED" },
            { name: "BILLING.SUBSCRIPTION.PAYMENT.FAILED" }
        ]
    };

    const response = await request('/v1/notifications/webhooks', 'POST', {
        'Authorization': `Bearer ${tokenRes.access_token}`
    }, webhookData);

    console.log(`Status: ${response.status}`);

    if (response.status === 201) {
        console.log('✅ Webhook created successfully!');
        console.log(`Webhook ID: ${response.data.id}`);
        console.log(`URL: ${response.data.url}`);
        console.log(`Events: ${response.data.event_types.map(e => e.name).join(', ')}`);
    } else {
        console.log('❌ Failed to create webhook:');
        console.log(JSON.stringify(response.data, null, 2));
    }
}

main().catch(console.error);