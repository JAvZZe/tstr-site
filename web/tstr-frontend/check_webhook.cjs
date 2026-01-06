#!/usr/bin/env node
/**
 * Simple webhook verification
 */

const https = require('https');
require('dotenv').config({ path: '.env' });

const CLIENT_ID = process.env.PAYPAL_CLIENT_ID;
const SECRET = process.env.PAYPAL_CLIENT_SECRET;
const WEBHOOK_ID = process.env.PAYPAL_WEBHOOK_ID;

console.log('Checking webhook:', WEBHOOK_ID);

const auth = Buffer.from(`${CLIENT_ID}:${SECRET}`).toString('base64');

const req = https.request({
    hostname: 'api-m.sandbox.paypal.com',
    path: `/v1/notifications/webhooks/${WEBHOOK_ID}`,
    method: 'GET',
    headers: {
        'Authorization': `Basic ${auth}`,
        'Content-Type': 'application/json'
    }
}, (res) => {
    console.log(`Status: ${res.statusCode}`);
    if (res.statusCode === 200) {
        console.log('✅ Webhook verified');
    } else {
        console.log('❌ Webhook not found');
    }
});

req.end();