# 🛠️ Manual Steps for Completion: Niche Localization & Trust Architecture

Follow these steps in order to finalize the implementation and bring the new features live.

---

### Step 1: Apply Supabase Database Migration
I have created the SQL migration file, but it must be applied to your live Supabase instance.
1. Go to your [Supabase Dashboard](https://supabase.com/dashboard).
2. Open your project: `haimjeaetrsaauitrhfy`.
3. Go to the **SQL Editor**.
4. Create a new query and paste the contents of:
   `supabase/migrations/20260411000000_niche_localization_trust.sql`
5. Click **Run**.
   *This will secure the `verified` column and create the Group/Branch aggregation view.*

---

### Step 2: Fix Existing Database Hierarchy
We need to retroactively link your existing 194+ listings into Parent/Branch structures based on the brand names.
1. Open your terminal in the root directory.
2. Ensure your `.env` file has `SUPABASE_SERVICE_ROLE_KEY` (required for bulk updates).
3. Run the following command:
   ```bash
   python3 web/tstr-automation/fix_hierarchy.py
   ```
4. Verify the output logs to see listings being linked to their respective Groups (e.g., SGS, Intertek).

---

### Step 3: Deploy Frontend Changes
The new dynamic routes (`/company`, `/group`, and the specialized PSEO routes) need to be built and deployed to Cloudflare.
1. Navigate to the frontend directory:
   ```bash
   cd web/tstr-frontend
   ```
2. Run a production build to verify there are no TypeScript or Astro errors:
   ```bash
   npm run build
   ```
3. Deploy to Cloudflare Pages (usually automatic via Git push, or use `npx wrangler pages deploy dist`).

---

### Step 4: Verification Checklist
Once deployed, verify the following URLs on your live site:
1. **Group Page**: `https://tstr.directory/group/sgs` (Verify it shows branches).
2. **Company Page**: `https://tstr.directory/company/[any-slug]` (Verify the compliance matrix table).
3. **PSEO Intersection**: `https://tstr.directory/hydrogen-testing/ISO-17025/global` (Verify it filters correctly).
4. **Trust Badges**: Ensure the "🛡️ TSTR Verified" badge appears only on labs where you have manually set `verified = true` in the DB.

---

### Support
If any of the Python scripts fail due to missing dependencies, run:
`pip install -r web/tstr-automation/requirements.txt`
