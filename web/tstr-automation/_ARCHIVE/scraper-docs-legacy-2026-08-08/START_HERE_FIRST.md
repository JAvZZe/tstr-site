# 🚨 CRITICAL: DNS & SSL SETUP REQUIRED

## IMMEDIATE ACTION NEEDED (Before Anything Else)

Your domain **tstr.directory** currently points to the wrong IP address. This must be fixed before the site can go live.

---

## STEP 1: UPDATE DNS (DO THIS NOW)

**Full instructions in:** `DNS_UPDATE_URGENT.md`

### Quick Summary:
1. Login to your domain registrar (where you bought tstr.directory)
2. Find DNS settings
3. Update A record from `34.55.31.102` → `34.100.223.247`
4. Save changes
5. Wait 15-30 minutes

### Test DNS Updated:
```bash
nslookup tstr.directory
```
**Should show:** 34.100.223.247

---

## STEP 2: SET UP EMAIL FORWARDING

While in your registrar DNS settings:

1. Add email forwarding: `listing@tstr.directory` → `tstr.directory1@gmail.com`
2. (Optional) Add more: `sales@`, `support@`, `info@`

### Temporary Solution (Works Immediately):
Use: `tstr.directory1+listing@gmail.com`
- All emails arrive at tstr.directory1@gmail.com
- You can filter by "+listing" in Gmail
- No setup required

---

## STEP 3: INSTALL SSL CERTIFICATE (After DNS Updated)

**Once DNS is updated, message Claude and I'll run:**

```bash
# I'll execute this via gcloud SSH
sudo certbot --apache -d tstr.directory -d www.tstr.directory \
  --agree-tos --email tstr.directory1@gmail.com --non-interactive
```

**This will:**
- Install free SSL certificate (Let's Encrypt)
- Enable HTTPS (green padlock)
- Auto-redirect HTTP → HTTPS
- Auto-renew every 90 days

---

## CURRENT STATUS

### ❌ NOT WORKING:
- https://tstr.directory (DNS points to wrong IP)
- listing@tstr.directory (email forwarding not set up)

### ✅ WORKING NOW:
- http://34.100.223.247 (WordPress accessible via IP)
- tstr.directory1@gmail.com (main email)
- tstr.directory1+listing@gmail.com (temporary listing email)

---

## PRIORITY ORDER

**1. FIX DNS** ← Do this FIRST (15 mins)
2. Set up email forwarding (5 mins)
3. Wait for DNS propagation (15-30 mins)
4. Install SSL certificate (I'll do this - 5 mins)
5. Test https://tstr.directory works (1 min)
6. THEN proceed with business launch

---

## WHY THIS MATTERS

**Without HTTPS:**
- ❌ Browsers show "Not Secure" warning
- ❌ Looks unprofessional
- ❌ Customers won't trust site
- ❌ Google ranks you lower
- ❌ Can't process payments securely

**With HTTPS:**
- ✅ Green padlock = Trust
- ✅ Professional appearance
- ✅ Better SEO rankings
- ✅ Payment processing enabled
- ✅ Customer confidence

---

## FILES YOU NEED

**DNS Update Guide:**
`C:\Users\alber\OneDrive\Documents\.WORK\tstr-automation\DNS_UPDATE_URGENT.md`

**SSL Installation Script (for Claude to run):**
`C:\Users\alber\OneDrive\Documents\.WORK\tstr-automation\install_ssl.sh`

---

## TIMELINE

**Today (You):** Update DNS + Set up email forwarding (20 minutes)
**Today (Wait):** DNS propagation (15-30 minutes)
**Today (Claude):** Install SSL certificate (5 minutes)
**Today (Done):** Site live with HTTPS ✅

**Total time:** ~1 hour

---

## AFTER SSL IS INSTALLED

Then proceed with launch checklist:
1. ✅ Run scraper (generate 100 listings)
2. ✅ Import to WordPress
3. ✅ Create pricing plans
4. ✅ Send first outreach emails
5. ✅ Submit to Google Search Console

---

**READ: DNS_UPDATE_URGENT.md NOW**
**DO: Update DNS immediately**
**REPLY: "DNS UPDATED" when complete**

Then I'll install SSL and you'll be live with https://tstr.directory ✅
