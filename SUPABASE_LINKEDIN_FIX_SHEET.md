# Fix Sheet: LinkedIn OAuth Domain Configuration

**Issue**: LinkedIn login redirects to the old `tstr.site` instead of `tstr.directory`.
**Resolution**: Update redirect configurations in the Supabase Dashboard and LinkedIn Developer Portal.

---

### Step 1: Update Supabase Authentication Settings

1.  **Login** to the [Supabase Dashboard](https://supabase.com/dashboard).
2.  Navigate to your project: **TSTR.directory**.
3.  Go to **Authentication** -> **URL Configuration**.
4.  **Site URL**:
    - Change from `https://tstr.site` to `https://tstr.directory`.
5.  **Redirect Allow List**:
    - Add `https://tstr.directory/**` to the list if not already present.
    - Remove any references to `tstr.site` from the allow list.
6.  Go to **Authentication** -> **Providers** -> **LinkedIn (OIDC)**.
7.  Copy the **Callback URL** (it should look like `https://haimjeaetrsaauitrhfy.supabase.co/auth/v1/callback`).

### Step 2: Update LinkedIn Developer Portal

1.  **Go to** your app in the [LinkedIn Developers Portal](https://www.linkedin.com/developers/apps).
2.  Select your app (e.g., **TSTR Hub**).
3.  Go to the **Auth** tab.
4.  Find **OAuth 2.0 settings** -> **Authorized Redirect URLs**.
5.  **Add** the Callback URL you copied from Supabase in Step 1.
6.  Ensure that **NO** `tstr.site` URLs remain in this list.
7.  Click **Update** or **Save** if required by the UI.

---

### Step 3: Verification

1.  Open `https://tstr.directory/login` in your browser.
2.  Open the developer console (**F12** or **Right-click -> Inspect -> Console**).
3.  Click **"Continue with LinkedIn"**.
4.  Observe the console log:
    - You should see: `[Auth] Redirect URL: https://tstr.directory/account`
5.  Complete the login sequence.
6.  **Expected Result**: You should land on `https://tstr.directory/account` after a successful login.
