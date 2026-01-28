# HTTPS Verification & Final Steps

## Test if HTTPS is Working

Open your browser and try:
1. https://tstr.directory
2. https://www.tstr.directory

**Expected Result:**
- Green padlock appears
- Site loads correctly

**If you see "Not Secure" or connection error:**
We need one final configuration fix.

## Quick Manual Fix (If Needed)

If HTTPS doesn't work, run this command:

```bash
gcloud compute ssh bizdir-wp-vm-vm --zone=asia-south1-a --project=business-directory-app-8888888
```

Then once logged in:
```bash
sudo /opt/bitnami/bncert-tool
```

When prompted:
1. Enter domains: `tstr.directory www.tstr.directory`
2. Enable HTTPS redirect: Yes
3. Enable www to non-www redirect: Yes  
4. Enter email: `tstr.directory1@gmail.com`
5. Agree to terms: Yes

This will take 2 minutes and configure everything automatically.

---

## What You Have NOW

- ✅ VM Running: 34.100.223.247
- ✅ DNS Working: tstr.directory points to correct IP
- ✅ SSL Certificates: Obtained from Let's Encrypt
- ✅ WordPress Active: http://34.100.223.247 works
- ⚠️ HTTPS Configuration: May need final activation

## Next: Test in Browser

**Try these URLs in your browser RIGHT NOW:**
1. http://tstr.directory (should work)
2. https://tstr.directory (should work with green padlock)

**Tell me what happens and I'll proceed accordingly.**
