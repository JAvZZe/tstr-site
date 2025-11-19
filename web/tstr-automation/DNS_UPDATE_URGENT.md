# DNS UPDATE GUIDE - URGENT ACTION REQUIRED

## CRITICAL: Domain Currently Points to Wrong IP

**Current Situation:**
- Domain: tstr.site
- Points to: 34.55.31.102 (OLD, non-existent)
- Should point to: 34.100.223.247 (NEW static IP)

**Impact:** Website is NOT accessible via domain name until DNS is updated.

---

## STEP 1: Update DNS A Record (15 minutes)

### Find Your Domain Registrar

Where did you buy tstr.site? Common registrars:
- GoDaddy
- Namecheap  
- Google Domains (now Squarespace)
- Cloudflare
- Name.com

**Don't know?** Check your email for "tstr.site" - you'll have a registration confirmation.

### Update DNS Records

1. **Login to your domain registrar**
   - Go to their website
   - Login with your credentials

2. **Navigate to DNS Settings**
   - Look for: "DNS", "DNS Management", "DNS Settings", or "Advanced DNS"
   - Find: "Manage Domains" → Click "tstr.site" → "DNS"

3. **Find the A Record**
   - Look for a record with:
     - Type: A
     - Name: @ (or blank, or tstr.site)
     - Value/Points to: 34.55.31.102 (OLD IP)

4. **Update the A Record**
   - Change: 34.55.31.102
   - To: **34.100.223.247**
   - TTL: 300 (5 minutes) or 3600 (1 hour)
   - Save changes

### Example Screenshots (Generic)

**GoDaddy:**
My Products → Domains → tstr.site → DNS → Edit A Record

**Namecheap:**
Domain List → Manage → Advanced DNS → Host Records → Edit A Record

**Cloudflare:**
Websites → tstr.site → DNS Records → Edit A Record

---

## STEP 2: Verify DNS Propagation (Wait 15-30 mins)

After updating, wait 15-30 minutes, then test:

### Option A: Online Tool
Go to: https://www.whatsmydns.net
- Enter: tstr.site
- Select: A
- Click: Search

**Success = All servers show: 34.100.223.247**

### Option B: Command Line (Windows)
```bash
nslookup tstr.site
```

**Success = You see: 34.100.223.247**

---

## STEP 3: Set Up Email Forwarding (While You're There)

### In Your Domain Registrar:

1. **Find Email Forwarding Section**
   - Usually under: "Email", "Email Forwarding", or "Email Settings"

2. **Create New Forward**
   - Forward from: `listing@tstr.site`
   - Forward to: `tstr.site1@gmail.com`
   - Save

3. **Add More Aliases** (Optional but Recommended)
   - `sales@tstr.site` → `tstr.site1@gmail.com`
   - `support@tstr.site` → `tstr.site1@gmail.com`
   - `info@tstr.site` → `tstr.site1@gmail.com`

### Example: GoDaddy Email Forwarding
Products → Email & Office → Forwarding → Add Address → Save

### Example: Namecheap Email Forwarding  
Domain List → Manage → Mail Settings → Email Forwarding → Add Forwarder

---

## STEP 4: Configure Gmail "Send As" (10 minutes)

This lets you SEND emails from listing@tstr.site

1. **Open Gmail** (tstr.site1@gmail.com)

2. **Go to Settings**
   - Click gear icon (top right)
   - Click "See all settings"

3. **Accounts and Import Tab**
   - Find: "Send mail as:"
   - Click: "Add another email address"

4. **Add Email Address**
   - Name: "TSTR.SITE Listings"
   - Email: listing@tstr.site
   - Uncheck: "Treat as an alias"
   - Click: "Next Step"

5. **SMTP Settings**
   - SMTP Server: smtp.gmail.com
   - Port: 587
   - Username: tstr.site1@gmail.com
   - Password: (your Gmail password or App Password)
   - Click: "Add Account"

6. **Verify**
   - Gmail sends verification email to listing@tstr.site
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
**Instead of:** listing@tstr.site
**Use:** tstr.site1+listing@gmail.com

This works IMMEDIATELY and all emails arrive at tstr.site1@gmail.com

### Website: Use IP Address
**Instead of:** https://tstr.site
**Use:** http://34.100.223.247

---

## ONCE DNS IS UPDATED (After 30 mins)

### Test Domain Access
Open browser: http://tstr.site
**Should load:** WordPress site

### Then I'll Install SSL Certificate

Once domain resolves to correct IP, message me and I'll run:

```bash
# This will be automated
sudo certbot --apache -d tstr.site -d www.tstr.site --agree-tos --email tstr.site1@gmail.com --non-interactive
```

**Result:** 
- https://tstr.site will work
- Free SSL certificate (Let's Encrypt)
- Auto-renewal every 90 days
- Browser shows green padlock

---

## CHECKLIST

- [ ] Login to domain registrar
- [ ] Update A record: 34.55.31.102 → 34.100.223.247
- [ ] Set up email forwarding: listing@tstr.site → tstr.site1@gmail.com
- [ ] Wait 30 minutes for DNS propagation
- [ ] Test: nslookup tstr.site (should show 34.100.223.247)
- [ ] Test: http://tstr.site (should load WordPress)
- [ ] Send test email to: listing@tstr.site
- [ ] Check tstr.site1@gmail.com receives it
- [ ] Configure Gmail "Send As"
- [ ] Notify Claude: DNS updated (so I can install SSL)

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
