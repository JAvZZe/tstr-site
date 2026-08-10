# SUPABASE DATABASE SETUP - COMPLETE BEGINNER'S GUIDE
**For someone with ZERO technical experience**

---

## WHAT YOU'RE ABOUT TO DO

You're going to create the "brain" of your website - the database where all your testing lab information will be stored. Think of it like creating filing cabinets before you can start filing documents.

**Time needed:** 15 minutes  
**Difficulty:** Copy and paste (that's it!)

---

## STEP-BY-STEP INSTRUCTIONS

### STEP 1: Open Supabase Dashboard (2 minutes)

1. Open your web browser (Chrome, Edge, Firefox - any will work)

2. Go to this address:
   ```
   https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
   ```

3. You should see your Supabase dashboard. It looks like a website with a dark sidebar on the left.

4. **Look at the left sidebar** - you'll see menu items like "Table Editor", "SQL Editor", "Authentication", etc.

5. **Click on "SQL Editor"** - it should be about halfway down the sidebar

---

### STEP 2: Run Extension Setup (3 minutes)

1. In the SQL Editor screen, click the button that says **"New query"** (top left area)

2. A blank text box appears - this is where you'll paste SQL code

3. **Open this file on your computer:**
   ```
   C:\Users\alber\OneDrive\Documents\.WORK\tstr-automation\SUPABASE_STEP_1_EXTENSIONS.sql
   ```
   
4. **Double-click the file** - it should open in Notepad or your text editor

5. **Select all the text** (Ctrl+A), then **Copy** (Ctrl+C)

6. **Go back to your browser** (to the Supabase SQL Editor)

7. **Click in the blank text box**, then **Paste** (Ctrl+V)

8. You should now see this text in the box:
   ```sql
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
   ```

9. **Click the "RUN" button** (bottom right, or press Ctrl+Enter)

10. **Wait 2-3 seconds**

11. At the bottom of the screen, you should see a green message:
    ```
    Success. No rows returned
    ```
    ✅ **This means it worked!**

---

### STEP 3: Create Tables (4 minutes)

1. **Click "New query" again** (to start fresh)

2. **Open this file:**
   ```
   C:\Users\alber\OneDrive\Documents\.WORK\tstr-automation\SUPABASE_STEP_2_TABLES.sql
   ```

3. **Copy all the text** (Ctrl+A, then Ctrl+C)

4. **Paste into the SQL Editor** (Ctrl+V)

5. **Click "RUN"** (or Ctrl+Enter)

6. **Wait 5-10 seconds** (this one takes a bit longer)

7. You should see: `Success. No rows returned`
   ✅ **Tables created!**

8. **Now do the same with the continuation file:**
   - Open: `SUPABASE_STEP_2B_TABLES_CONTINUED.sql`
   - Click "New query"
   - Copy and paste the content
   - Click "RUN"
   - Wait for "Success"

---

### STEP 4: Add Indexes (2 minutes)

Indexes make your website search MUCH faster. It's like adding an index to a book.

1. **Click "New query"**

2. **Open this file:**
   ```
   C:\Users\alber\OneDrive\Documents\.WORK\tstr-automation\SUPABASE_STEP_3_INDEXES.sql
   ```

3. **Copy and paste** (you know the drill now!)

4. **Click "RUN"**

5. Wait for: `Success. No rows returned`
   ✅ **Indexes created!**

---

### STEP 5: Add Starting Data (3 minutes)

This adds your 5 initial testing categories and main cities.

1. **Click "New query"**

2. **Open this file:**
   ```
   C:\Users\alber\OneDrive\Documents\.WORK\tstr-automation\SUPABASE_STEP_4_SEED_DATA.sql
   ```

3. **Copy and paste**

4. **Click "RUN"**

5. **Wait 5-10 seconds** (this one also takes a bit)

6. You should see: `Success. No rows returned`
   ✅ **Your categories and locations are now in the database!**

---

### STEP 6: Verify It Worked (2 minutes)

Let's check that everything is actually in your database:

1. **In the left sidebar, click "Table Editor"** (near the top)

2. You should now see a list of tables on the left:
   - locations
   - categories
   - listings
   - payments
   - custom_fields
   - listing_custom_fields
   - listing_images
   - search_logs

3. **Click on "categories"**

4. You should see 5 rows showing your testing categories:
   - Oil & Gas Testing
   - Pharmaceutical Testing
   - Biotech Testing
   - Environmental Testing
   - Materials Testing

5. **Click on "locations"**

6. You should see multiple rows with cities like:
   - Houston
   - London
   - Singapore
   - etc.

✅ **If you see this data, CONGRATULATIONS! Your database is fully set up!**

---

## WHAT IF SOMETHING GOES WRONG?

### Error: "relation already exists"
**What it means:** The table was already created before  
**What to do:** This is actually fine! It just means you ran the script twice. Continue to the next step.

### Error: "column does not exist"
**What it means:** You might have skipped a step  
**What to do:** Go back and make sure you ran Steps 1-4 in order

### Error: "permission denied"
**What it means:** Your Supabase access might not be set up correctly  
**What to do:** Make sure you're logged into the correct Supabase project

### Nothing happens when you click RUN
**What it means:** The page might not have loaded properly  
**What to do:** Refresh the page (F5) and try again

---

## WHAT ABOUT THE WORDPRESS SITE?

Good question! Here's what to do:

**Short answer:** Leave it running for now. It costs £0 anyway.

**Why?**
- No harm in keeping it
- Good backup if something goes wrong
- You can compare the old vs new site
- Easy to shut down later

**When to shut it down:**
- After your new custom site is live and working
- After you've been using the new site for 2-4 weeks
- When you're confident you don't need the WordPress version

**How to shut it down (when ready):**
1. Go to Google Cloud Console
2. Find your VM: wordpress-1-vm
3. Click "DELETE"
4. Confirm

But don't do this yet! Wait until the new site proves itself.

---

## NEXT STEPS (After Database is Set Up)

Once you've completed all 6 steps above, you'll be ready to:

1. **Build the frontend** (the actual website visitors will see)
2. **Import your first listings** (testing laboratories)
3. **Deploy to tstr.directory** (make it live on the internet)
4. **Start accepting payments** (featured listings)

I'll guide you through each of these, one at a time, just as simply as this guide.

---

## READY TO START?

Take a deep breath. You've got this. It's literally just:
1. Copy
2. Paste  
3. Click RUN
4. Repeat 4 times

Go ahead and start with Step 1! 🚀

**Once you've completed Step 6 and verified your data is there, come back and tell me: "Database is set up!" and we'll move to building the website.**
