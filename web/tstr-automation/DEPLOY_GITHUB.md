# DEPLOY TO GITHUB - STEP BY STEP

## Step 1: Create Repository on GitHub

1. **Go to:** https://github.com/new

2. **Fill in:**
   - Repository name: `tstr-site`
   - Description: `Global Testing Laboratory Directory`
   - Visibility: **Private** (keep your code private)
   - ❌ Do NOT check "Add README"
   - ❌ Do NOT add .gitignore
   - ❌ Do NOT add license

3. **Click:** "Create repository"

4. **You'll see a page with commands** - IGNORE IT for now, follow instructions below instead

---

## Step 2: Push Your Code from Command Prompt

### Open Command Prompt
- Make sure you're still in: `C:\Users\alber\OneDrive\Documents\.WORK\tstr-frontend`
- If not, navigate there with: `cd C:\Users\alber\OneDrive\Documents\.WORK\tstr-frontend`

### Run These Commands One by One

**Command 1: Initialize Git (if not already done)**
```bash
git init
```

**Command 2: Add all files**
```bash
git add .
```

**Command 3: Create first commit**
```bash
git commit -m "Initial commit - tstr.directory MVP"
```

**Command 4: Rename branch to main**
```bash
git branch -M main
```

**Command 5: Connect to GitHub**
**IMPORTANT:** Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username!

```bash
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/tstr-site.git
```

Example: If your GitHub username is "albertoinc", it would be:
```bash
git remote add origin https://github.com/albertoinc/tstr-site.git
```

**Command 6: Push to GitHub**
```bash
git push -u origin main
```

**You'll be asked for credentials:**
- Username: Your GitHub username
- Password: **Use a Personal Access Token (NOT your password)**

---

## Step 3: Create GitHub Personal Access Token

GitHub doesn't accept passwords anymore. You need a token.

1. **Go to:** https://github.com/settings/tokens

2. **Click:** "Generate new token" → "Generate new token (classic)"

3. **Fill in:**
   - Note: `TSTR Site Deployment`
   - Expiration: `No expiration`
   - Scopes: Check **only** these:
     - ✅ `repo` (all repo permissions)

4. **Click:** "Generate token"

5. **COPY THE TOKEN IMMEDIATELY** (you won't see it again)
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Paste it in Notepad temporarily

6. **Go back to Command Prompt**

7. **Run the push command again:**
   ```bash
   git push -u origin main
   ```

8. **When asked for password, paste your token** (not your GitHub password)

9. **Press Enter**

---

## Step 4: Verify Upload

1. **Go to:** https://github.com/YOUR_GITHUB_USERNAME/tstr-site

2. **You should see your files:**
   - src/
   - public/
   - package.json
   - astro.config.mjs
   - etc.

✅ **If you see these files, SUCCESS!** Your code is on GitHub.

---

## TROUBLESHOOTING

### Error: "fatal: not a git repository"
**Fix:** Run `git init` first

### Error: "remote origin already exists"
**Fix:** Run `git remote remove origin` then add it again

### Error: "authentication failed"
**Fix:** Make sure you're using the Personal Access Token, not your password

### Error: "permission denied"
**Fix:** Check your token has `repo` permissions

---

## NEXT: CLOUDFLARE PAGES

Once your code is on GitHub, come back and tell me:
**"Code is on GitHub!"**

Then I'll guide you through connecting Cloudflare Pages to deploy it live.
