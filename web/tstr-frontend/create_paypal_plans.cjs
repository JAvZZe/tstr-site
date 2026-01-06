#!/usr/bin/env node
/**
 * Create PayPal subscription plans via API
 */

const https = require('https');
require('dotenv').config({ path: '.env' });

const CLIENT_ID = process.env.PAYPAL_CLIENT_ID;
const SECRET = process.env.PAYPAL_CLIENT_SECRET;
const MODE = process.env.PAYPAL_MODE || 'sandbox';

console.log('Creating PayPal Subscription Plans...');
console.log(`Mode: ${MODE}`);
console.log(`Client ID: ${CLIENT_ID ? 'Set' : 'Missing'}`);
console.log(`Secret: ${SECRET ? 'Set' : 'Missing'}`);

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

async function createPlan(planData) {
    console.log(`\nCreating plan: ${planData.name}`);

    const response = await request('/v1/billing/plans', 'POST', {}, planData);
    console.log(`Status: ${response.status}`);

    if (response.status === 201) {
        console.log(`✅ Plan created successfully!`);
        console.log(`Plan ID: ${response.data.id}`);
        console.log(`Status: ${response.data.status}`);
        return response.data.id;
    } else {
        console.log(`❌ Failed to create plan:`);
        console.log(JSON.stringify(response.data, null, 2));
        return null;
    }
}

async function main() {
    // Get access token first
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

    // Update request function to use Bearer token
    const bearerRequest = (path, method = 'GET', headers = {}, body = null) => {
        return request(path, method, {
            'Authorization': `Bearer ${tokenRes.access_token}`,
            ...headers
        }, body);
    };

    // Create Professional Plan
    const professionalPlan = {
        product_id: "PROD-XXXXXXXXXXXXXXXXXXXXX", // We'll need to create a product first
        name: "TSTR Professional",
        description: "Professional listing management for TSTR.directory",
        status: "ACTIVE",
        billing_cycles: [
            {
                frequency: {
                    interval_unit: "MONTH",
                    interval_count: 1
                },
                tenure_type: "REGULAR",
                sequence: 1,
                total_cycles: 0, // 0 = indefinite
                pricing_scheme: {
                    fixed_price: {
                        value: "295.00",
                        currency_code: "USD"
                    }
                }
            }
        ],
        payment_preferences: {
            auto_bill_outstanding: true,
            setup_fee_failure_action: "CANCEL",
            payment_failure_threshold: 3
        },
        taxes: {
            percentage: "0",
            inclusive: false
        }
    };

    // First we need to create a product
    console.log('\n2. Creating product for Professional plan...');
    const productRes = await bearerRequest('/v1/catalogs/products', 'POST', {}, {
        name: "TSTR Professional Plan",
        description: "Professional listing management service",
        type: "SERVICE",
        category: "SOFTWARE",
        image_url: "https://tstr.directory/logo.png",
        home_url: "https://tstr.directory"
    });

    if (productRes.status !== 201) {
        console.error('Failed to create product:', productRes.data);
        return;
    }

    const productId = productRes.data.id;
    console.log(`✅ Product created: ${productId}`);

    // Update plan with product ID
    professionalPlan.product_id = productId;

    // Create Professional Plan
    const profPlanId = await createPlan(professionalPlan);
    if (!profPlanId) return;

    // Create Premium Plan
    console.log('\n3. Creating Premium plan...');
    const premiumPlan = {
        ...professionalPlan,
        product_id: productId, // Same product
        name: "TSTR Premium",
        description: "Premium listing management for TSTR.directory",
        billing_cycles: [
            {
                frequency: {
                    interval_unit: "MONTH",
                    interval_count: 1
                },
                tenure_type: "REGULAR",
                sequence: 1,
                total_cycles: 0,
                pricing_scheme: {
                    fixed_price: {
                        value: "795.00",
                        currency_code: "USD"
                    }
                }
            }
        ]
    };

    const premPlanId = await createPlan(premiumPlan);
    if (!premPlanId) return;

    console.log('\n🎉 All plans created successfully!');
    console.log(`Professional Plan ID: ${profPlanId}`);
    console.log(`Premium Plan ID: ${premPlanId}`);

    console.log('\n📋 Next steps:');
    console.log('1. Update .env with these Plan IDs');
    console.log('2. Create webhook in PayPal dashboard');
    console.log('3. Test the payment flow');
}

main().catch(console.error);