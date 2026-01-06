const https = require('https');
require('dotenv').config({ path: '.env' });

const CLIENT_ID = process.env.PAYPAL_CLIENT_ID;
const SECRET = process.env.PAYPAL_CLIENT_SECRET;
const PLAN_ID = process.env.PAYPAL_PLAN_PROFESSIONAL;
const MODE = process.env.PAYPAL_MODE || 'sandbox';

console.log('Testing PayPal Configuration...');
console.log(`Mode: ${MODE}`);
console.log(`Client ID: ${CLIENT_ID ? 'Set' : 'Missing'}`);
console.log(`Secret: ${SECRET ? 'Set' : 'Missing'}`);
console.log(`Plan ID: ${PLAN_ID}`);

if (!CLIENT_ID || !SECRET) {
    console.error('Missing credentials');
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
        if (body) req.write(body);
        req.end();
    });
}

async function test() {
    // 1. Get Token
    console.log('\n1. Fetching Access Token...');
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
        console.error('Failed to get token:', tokenRes);
        return;
    }
    console.log('✅ Access Token received');
    const accessToken = tokenRes.access_token;

    // 2. Verify Plan
    if (PLAN_ID) {
        console.log(`\n2. Verifying Plan: ${PLAN_ID}...`);
        const planPath = `/v1/billing/plans/${PLAN_ID}`;
        console.log(`Requesting: ${hostname}${planPath}`);

        const planRes = await new Promise((resolve, reject) => {
            const req = https.request({
                hostname,
                path: planPath,
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                }
            }, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    if (res.statusCode >= 200 && res.statusCode < 300) {
                        resolve({ ok: true, data: JSON.parse(data) });
                    } else {
                        resolve({ ok: false, status: res.statusCode, data: data });
                    }
                });
            });
            req.end();
        });

        if (planRes.ok && planRes.data.status === 'ACTIVE') {
            console.log('✅ Plan is ACTIVE and valid.');
            console.log(`Plan Name: ${planRes.data.name}`);
        } else {
            console.error('❌ Plan issue:', planRes);
        }
    } else {
        console.log('Skipping plan check (no plan ID in env)');
    }
}

test().catch(console.error);
