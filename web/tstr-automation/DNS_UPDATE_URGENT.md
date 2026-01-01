# DNS UPDATE GUIDE - URGENT ACTION REQUIRED

## CRITICAL: Domain DNS Configuration Needed

**Current Situation:**
- Domain: tstr.directory
- Current setup: Direct IP routing (not using Cloudflare)
- Should be: Configured with Cloudflare nameservers for CDN and security

**Impact:** Website may not be properly routed through Cloudflare's CDN and security until DNS is updated.

---

## STEP 1: Update DNS Nameservers (15 minutes)

### Find Your Domain Registrar

Where did you buy tstr.directory? Common registrars:
- GoDaddy
- Namecheap  
- Google Domains (now Squarespace)
- Cloudflare
- Name.com

**Don't know?** Check your email for "tstr.directory" - you'll have a registration confirmation.

### Update DNS Records

1. **Login to your domain registrar**
   - Go to their website
   - Login with your credentials

2. **Navigate to DNS Settings**
   - Look for: "DNS", "DNS Management", "DNS Settings", or "Advanced DNS"
   - Find: "Manage Domains" → Click "tstr.directory" → "DNS"

3. **Update Nameservers (Instead of A Record)**
   - Find the nameserver (NS) records
   - Replace current nameservers with Cloudflare's nameservers
   - Cloudflare will provide the correct nameservers to use
   - This will route traffic through Cloudflare's CDN and security

### Example Screenshots (Generic)

**GoDaddy:**
My Products → Domains → tstr.directory → Nameservers → Change Nameservers

**Namecheap:**
Domain List → Manage → Nameservers → Change Nameservers

**Cloudflare:**
Add Site → Enter tstr.directory → Follow DNS setup wizard

---

## STEP 2: Verify DNS Propagation (Wait 15-30 mins)

After updating, wait 15-30 minutes, then test:

### Option A: Online Tool
Go to: https://www.whatsmydns.net
- Enter: tstr.directory
- Select: NS (Nameserver)
- Click: Search

**Success = All servers show: Cloudflare nameservers (e.g., *.ns.cloudflare.com)**

### Option B: Command Line (Windows)
```bash
nslookup tstr.directory
```

**Success = You see: Cloudflare IP addresses (e.g., 104.21.x.x, 172.67.x.x, 173.245.x.x)**

---

## STEP 3: Set Up Email Forwarding (While You're There)

### In Your Domain Registrar:

1. **Find Email Forwarding Section**
   - Usually under: "Email", "Email Forwarding", or "Email Settings"

2. **Create New Forward**
   - Forward from: `listing@tstr.directory`
   - Forward to: `tstr.site1@gmail.com`
   - Save

3. **Add More Aliases** (Optional but Recommended)
   - `sales@tstr.directory` → `tstr.site1@gmail.com`
   - `support@tstr.directory` → `tstr.site1@gmail.com`
   - `info@tstr.directory` → `tstr.site1@gmail.com`

### Example: GoDaddy Email Forwarding
Products → Email & Office → Forwarding → Add Address → Save

### Example: Namecheap Email Forwarding  
Domain List → Manage → Mail Settings → Email Forwarding → Add Forwarder

---

## STEP 4: Configure Gmail "Send As" (10 minutes)

This lets you SEND emails from listing@tstr.directory

1. **Open Gmail** (tstr.site1@gmail.com)

2. **Go to Settings**
   - Click gear icon (top right)
   - Click "See all settings"

3. **Accounts and Import Tab**
   - Find: "Send mail as:"
   - Click: "Add another email address"

4. **Add Email Address**
   - Name: "TSTR.DIRECTORY Listings"
   - Email: listing@tstr.directory
   - Uncheck: "Treat as an alias"
   - Click: "Next Step"

5. **SMTP Settings**
   - SMTP Server: smtp.gmail.com
   - Port: 587
   - Username: tstr.site1@gmail.com
   - Password: (your Gmail password or App Password)
   - Click: "Add Account"

6. **Verify**
   - Gmail sends verification email to listing@tstr.directory
   - Check tstr.site1@gmail.com inbox (forwarded)
   - Click verification link
   - Done!

### Alternative: Use App Password (More Secure)

If you have 2-factor authentication:
1. Go to: https://myaccount.google.com/apppasswords
2. Select app: Mail
3. Select device: Windows Computer
4. Generate
5. Use this 16-character password instead

---

## TEMPORARY SOLUTION (Use Immediately)

While waiting for DNS update and email forwarding:

### Email: Use Plus Addressing
**Instead of:** listing@tstr.directory
**Use:** tstr.site1+listing@gmail.com

This works IMMEDIATELY and all emails arrive at tstr.site1@gmail.com

### Website: Use Live URL
**Access the site at:** https://tstr.directory

---

## ONCE DNS IS UPDATED (After 30 mins)

### Test Domain Access
Open browser: https://tstr.directory
**Should load:** Astro frontend site

### SSL Certificate Status

SSL is already configured with Cloudflare Pages:
- https://tstr.directory works with SSL
- Browser shows green padlock
- Certificate managed automatically by Cloudflare
- No manual SSL installation needed

---

## CHECKLIST

- [ ] Login to domain registrar
- [ ] Update DNS to point to Cloudflare nameservers (provided by Cloudflare)
- [ ] Set up email forwarding: listing@tstr.directory → tstr.site1@gmail.com
- [ ] Wait 30 minutes for DNS propagation
- [ ] Test: nslookup tstr.directory (should show Cloudflare IPs)
- [ ] Test: https://tstr.directory (should load Astro frontend)
- [ ] Send test email to: listing@tstr.directory
- [ ] Check tstr.site1@gmail.com receives it
- [ ] Configure Gmail "Send As"
- [ ] Verify site is working properly with new DNS settings

---

## COMMON ISSUES

**Q: Can't find DNS settings in registrar?**
A: Look for "Advanced", "Technical", "Name Servers", or contact their support

**Q: Do I need to change Name Servers?**
A: NO - only update the A record value

**Q: What if I have Cloudflare?**
A: Update A record in Cloudflare dashboard, orange cloud can stay ON

**Q: Email forwarding not available?**
A: Use tstr.site1+listing@gmail.com temporarily (works immediately)

**Q: How long does DNS take?**
A: Usually 15-30 minutes, maximum 48 hours (rare)

---

## URGENT: Do This NOW

The DNS update is the ONLY thing blocking:
1. Domain access (https://tstr.site)
2. SSL certificate installation
3. Professional email (listing@tstr.site)
4. Going live to customers

**Time required:** 15 minutes
**Impact:** Unlocks everything else

---

**Once completed, reply with: "DNS UPDATED" and I'll immediately install SSL and update all WordPress URLs.**
