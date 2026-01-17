# Gemini Flash Instructions: Create /contact Page

> **Priority**: HIGH - Critical for revenue generation
> **Estimated Time**: 30-45 minutes
> **Prerequisites**: Run `./bootstrap_global.sh` first

---

## Task Overview

Create a `/contact` page with a form that routes inquiries to different emails based on type.

## Routing Rules

| Inquiry Type | Destination Email |
|--------------|-------------------|
| Request Quotation | sales@tstr.directory |
| Sales Inquiry | sales@tstr.directory |
| Technical Support | support@tstr.directory |
| Partnership | admin@tstr.directory |
| General Inquiry | admin@tstr.directory |
| Other | admin@tstr.directory |

---

## Step 1: Update contacts.ts

**File**: `web/tstr-frontend/src/lib/contacts.ts`

Add `admin` email to the `CONTACTS` object:

```typescript
export const CONTACTS = {
  sales: 'sales@tstr.directory',
  support: 'support@tstr.directory',
  admin: 'admin@tstr.directory',  // ADD THIS LINE
  partnerships: 'support@tstr.directory',
  enquiries: 'support@tstr.directory',
  legal: 'support@tstr.directory',
} as const
```

---

## Step 2: Create API Endpoint

**File**: `web/tstr-frontend/src/pages/api/contact.ts` (NEW FILE)

```typescript
import type { APIRoute } from 'astro';
import { Resend } from 'resend';

const resend = new Resend(import.meta.env.RESEND_API_KEY);

// Routing map
const EMAIL_ROUTING: Record<string, string> = {
  'quotation': 'sales@tstr.directory',
  'sales': 'sales@tstr.directory',
  'support': 'support@tstr.directory',
  'partnership': 'admin@tstr.directory',
  'general': 'admin@tstr.directory',
  'other': 'admin@tstr.directory',
};

export const POST: APIRoute = async ({ request }) => {
  try {
    const formData = await request.formData();
    const name = formData.get('name')?.toString() || '';
    const email = formData.get('email')?.toString() || '';
    const company = formData.get('company')?.toString() || '';
    const inquiryType = formData.get('inquiryType')?.toString() || 'general';
    const message = formData.get('message')?.toString() || '';

    // Validation
    if (!name || !email || !message) {
      return new Response(JSON.stringify({ error: 'Name, email, and message are required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Get destination email
    const toEmail = EMAIL_ROUTING[inquiryType] || 'admin@tstr.directory';
    
    // Format inquiry type for display
    const typeLabels: Record<string, string> = {
      'quotation': 'Request Quotation',
      'sales': 'Sales Inquiry',
      'support': 'Technical Support',
      'partnership': 'Partnership Opportunity',
      'general': 'General Inquiry',
      'other': 'Other',
    };

    // Send email via Resend
    const { error } = await resend.emails.send({
      from: 'TSTR.directory <noreply@tstr.directory>',
      to: toEmail,
      replyTo: email,
      subject: `[TSTR Contact] ${typeLabels[inquiryType] || 'Inquiry'} from ${name}`,
      html: `
        <h2>New Contact Form Submission</h2>
        <p><strong>Type:</strong> ${typeLabels[inquiryType] || inquiryType}</p>
        <p><strong>Name:</strong> ${name}</p>
        <p><strong>Email:</strong> <a href="mailto:${email}">${email}</a></p>
        <p><strong>Company:</strong> ${company || 'Not provided'}</p>
        <hr>
        <p><strong>Message:</strong></p>
        <p>${message.replace(/\n/g, '<br>')}</p>
      `,
    });

    if (error) {
      console.error('Resend error:', error);
      return new Response(JSON.stringify({ error: 'Failed to send message' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (err) {
    console.error('Contact form error:', err);
    return new Response(JSON.stringify({ error: 'Server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
```

---

## Step 3: Create Contact Page

**File**: `web/tstr-frontend/src/pages/contact.astro` (NEW FILE)

Use the project's design system (navy blue #000080, lime green #32CD32 gradient). Copy header/footer style from `submit.astro`.

Form fields:
- Name (required)
- Email (required)
- Company (optional)
- Inquiry Type (dropdown, required):
  - Request Quotation
  - Sales Inquiry
  - Technical Support
  - Partnership Opportunity
  - General Inquiry
  - Other
- Message (textarea, required)
- Submit button

Include:
- Success message after submission
- Error handling
- Client-side validation
- Breadcrumb: Home / Contact

---

## Step 4: Add Footer Link

**File**: `web/tstr-frontend/src/lib/contacts.ts`

Add to `footerLinks` array:
```typescript
{ href: '/contact', label: 'Contact Us' },
```

---

## Step 5: Test & Deploy

```bash
cd web/tstr-frontend

# Test locally
npm run dev
# Visit http://localhost:4321/contact
# Submit test form

# Build
npm run build

# Commit
git add .
git commit -m "feat: Add /contact page with email routing"
git push origin main
```

---

## Verification Checklist

- [ ] Page loads at `/contact`
- [ ] All form fields render correctly
- [ ] Dropdown has all 6 inquiry types
- [ ] Form validates required fields
- [ ] Submission shows success message
- [ ] Email received at correct destination
- [ ] Mobile responsive
- [ ] Footer link works

---

## Reference Files

- [submit.astro](file:///media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-frontend/src/pages/submit.astro) - Copy design pattern
- [email.ts](file:///media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-frontend/src/lib/email.ts) - Existing email templates
- [contacts.ts](file:///media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-frontend/src/lib/contacts.ts) - Centralized config
