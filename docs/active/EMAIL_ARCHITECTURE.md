# TSTR.directory Email Architecture

## Email Providers Overview

| Type | Provider | Domain/Subdomain | Free Tier | Status |
|------|----------|------------------|-----------|--------|
| **Transactional** | Resend | `adminfin.tstr.directory` | 3,000/mo | ✅ Active |
| **Sales/Marketing** | SendPulse | *Separate domain (TBD)* | 15,000/mo | ⏳ Pending Setup |
| **Receiving** | Cloudflare | `tstr.directory` | Unlimited | ✅ Active |

---

## Transactional Emails (Resend)

**Use Cases:**

- Claim verification codes
- Payment confirmations (EFT, Bitcoin, PayPal)
- Sign-up confirmations
- Draft save/resume links
- Contact form submissions

**Configuration:**

- API Key: `re_eYDmQ352_...` (in `.env`)
- From Address: `noreply@adminfin.tstr.directory` (Verified)
- Login: `tstr.directory1@gmail.com`
- Subdomain: `adminfin.tstr.directory`

**Code Location:**

- Service: `src/lib/email.ts`
- Templates: Same file (inline HTML templates)

---

## Sales/Marketing Emails (SendPulse - Future)

**Use Cases:**

- Welcome emails for new users
- Promotional campaigns
- Newsletter/updates
- Re-engagement emails

**Why Separate Domain:**

- Protects main domain reputation
- Marketing emails have higher spam risk
- Separate analytics and deliverability tracking

**SendPulse API Capabilities:**

- REST API with JSON responses
- Email sending via API or SMTP
- Mailing list management
- Template management with variables
- Campaign scheduling and analytics
- Webhooks for delivery events
- Automation flows (Automation360)

---

## Receiving (Cloudflare Email Routing)

**Configured Addresses:**

- `sales@tstr.directory` → Sales inquiries
- `support@tstr.directory` → General support
- `admin@tstr.directory` → Administrative

**Code Location:**

- Configuration: `src/lib/contacts.ts`

---

## Integration Recommendations

### When SendPulse is Ready

1. **Create separate module**: `src/lib/marketing-email.ts`
2. **Keep providers isolated**: Don't mix transactional and marketing
3. **Use environment variables**:

   ```
   SENDPULSE_API_USER_ID=xxx
   SENDPULSE_API_SECRET=xxx
   SENDPULSE_FROM_EMAIL=hello@[marketing-domain].com
   ```

4. **Template structure**:
   - Welcome email
   - Newsletter template
   - Promotional template
   - Re-engagement template

---

**Last Updated**: 2026-01-26
**Updated By**: Gemini (Antigravity)
