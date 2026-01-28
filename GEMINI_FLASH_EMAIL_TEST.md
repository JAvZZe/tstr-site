# Gemini Flash: Test Resend Email Sending

## Objective

Test that the Resend email service is working correctly from `noreply@tstr.directory`.

## Prerequisites

- Node.js installed
- Access to the project directory: `web/tstr-frontend/`

## Instructions

### Step 1: Navigate to Frontend Directory

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-frontend
```

### Step 2: Create Test Script

Create a file called `test_resend_now.mjs` with the following content:

```javascript
// test_resend_now.mjs - Test Resend Email Service
import { Resend } from 'resend';

const RESEND_API_KEY = 're_eYDmQ352_2mH5o58xtSEBRA6YSbt1od9s';
const FROM_EMAIL = 'noreply@tstr.directory';
const TEST_EMAIL = 'tstr.site1@gmail.com'; // Send to owner's email

const resend = new Resend(RESEND_API_KEY);

async function testEmail() {
  console.log('🧪 Testing Resend Email Service...');
  console.log(`📧 From: ${FROM_EMAIL}`);
  console.log(`📬 To: ${TEST_EMAIL}`);
  
  try {
    const { data, error } = await resend.emails.send({
      from: FROM_EMAIL,
      to: [TEST_EMAIL],
      subject: `✅ TSTR Email Test - ${new Date().toISOString()}`,
      html: `
        <div style="font-family: Arial, sans-serif; padding: 20px; max-width: 600px;">
          <h1 style="color: #000080;">TSTR.directory Email Test</h1>
          <p>This is a test email sent from the Resend API.</p>
          <hr style="border: 1px solid #eee;">
          <p><strong>Timestamp:</strong> ${new Date().toISOString()}</p>
          <p><strong>From Address:</strong> ${FROM_EMAIL}</p>
          <p><strong>API Status:</strong> ✅ Working</p>
          <hr style="border: 1px solid #eee;">
          <p style="color: #666; font-size: 12px;">
            This is an automated test from TSTR.directory email system.
          </p>
        </div>
      `,
      text: `TSTR.directory Email Test\n\nTimestamp: ${new Date().toISOString()}\nFrom: ${FROM_EMAIL}\nStatus: Working`
    });

    if (error) {
      console.error('❌ Error:', error);
      process.exit(1);
    }

    console.log('✅ Email sent successfully!');
    console.log('📨 Message ID:', data?.id);
    console.log('\n💡 Check inbox at tstr.site1@gmail.com to confirm receipt.');
  } catch (err) {
    console.error('❌ Exception:', err.message);
    process.exit(1);
  }
}

testEmail();
```

### Step 3: Run the Test

```bash
node test_resend_now.mjs
```

### Step 4: Expected Output

```
🧪 Testing Resend Email Service...
📧 From: noreply@tstr.directory
📬 To: tstr.site1@gmail.com
✅ Email sent successfully!
📨 Message ID: <some-uuid>

💡 Check inbox at tstr.site1@gmail.com to confirm receipt.
```

### Step 5: Verify Receipt

1. Check the inbox at `tstr.site1@gmail.com`
2. Look for email with subject starting with "✅ TSTR Email Test"
3. Confirm the email was delivered (check spam folder if not in inbox)

### Step 6: Report Results

Report back with:

- Did the script run without errors? (Yes/No)
- Was the email received? (Yes/No)
- Any error messages if it failed

## Cleanup

After testing, you can delete the test script:

```bash
rm test_resend_now.mjs
```

---
**Created**: 2026-01-26
**Purpose**: Validate Resend transactional email service
