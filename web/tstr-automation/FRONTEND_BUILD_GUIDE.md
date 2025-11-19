# TSTR.SITE FRONTEND BUILD - COMPLETE BEGINNER'S GUIDE
**Building Your Actual Website (Non-Technical Version)**

---

## WHAT YOU'RE ABOUT TO DO

You're going to:
1. Install some free software on your computer
2. Create a website project folder
3. Connect it to your Supabase database
4. Build some basic pages
5. Upload it to the internet (for free)

**Time needed:** 2-3 hours (can split across multiple sessions)  
**Cost:** £0

---

## PART 1: INSTALL REQUIRED SOFTWARE (20 minutes)

### Step 1.1: Install Node.js

**What is Node.js?** It's free software that lets you build modern websites.

1. **Go to:** https://nodejs.org

2. **Click the big green button** that says "Download Node.js (LTS)"
   - LTS means "Long Term Support" - the stable version

3. **Run the downloaded file** (probably called `node-v20.x.x-x64.msi`)

4. **Click through the installer:**
   - Accept the license agreement
   - Keep all default settings
   - Click "Next, Next, Next, Install"
   - Wait for it to finish
   - Click "Finish"

5. **Verify it worked:**
   - Press `Windows key + R`
   - Type: `cmd`
   - Press Enter (a black window opens - this is "Command Prompt")
   - Type: `node --version`
   - Press Enter
   - You should see something like: `v20.11.0`
   - ✅ If you see a version number, it worked!

### Step 1.2: Install Git (Optional but Recommended)

**What is Git?** It saves versions of your code (like "Track Changes" in Word).

1. **Go to:** https://git-scm.com/download/win

2. **Download will start automatically**

3. **Run the installer:**
   - Click through with default settings
   - When asked about editor, choose "Notepad" (simplest)
   - Keep clicking "Next" until it installs
   - Click "Finish"

4. **Verify it worked:**
   - Open Command Prompt again (Windows key + R, type `cmd`)
   - Type: `git --version`
   - Press Enter
   - You should see: `git version 2.x.x`
   - ✅ If you see a version number, it worked!

---

## PART 2: GET SUPABASE CREDENTIALS (5 minutes)

You need two "keys" from Supabase to connect your website to your database.

1. **Go to Supabase Dashboard:**
   ```
   https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
   ```

2. **Click on the "Settings" icon** (gear icon, bottom of left sidebar)

3. **Click "API"** in the settings menu

4. **You'll see two important pieces of information:**

   **A) Project URL**
   - Looks like: `https://haimjeaetrsaauitrhfy.supabase.co`
   - Copy this (Ctrl+C)
   - Open Notepad
   - Paste it
   - Label it: "PROJECT URL"

   **B) Anon/Public Key**
   - It's a long string of random letters/numbers
   - Looks like: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (very long)
   - Find the one labeled: "anon public"
   - Click the "Copy" button next to it
   - Paste in Notepad below your Project URL
   - Label it: "ANON KEY"

5. **Save this Notepad file** somewhere safe:
   ```
   C:\Users\alber\OneDrive\Documents\.WORK\tstr-automation\SUPABASE_KEYS.txt
   ```

⚠️ **IMPORTANT:** Keep these keys private! Don't share them with anyone.

---

## PART 3: CREATE YOUR WEBSITE PROJECT (30 minutes)

### Step 3.1: Open Command Prompt

1. Press `Windows key + R`
2. Type: `cmd`
3. Press Enter

You'll see a black window with white text. This is where you'll type commands.

### Step 3.2: Navigate to Your Work Folder

Type these commands **one at a time**, pressing Enter after each:

```bash
cd C:\Users\alber\OneDrive\Documents\.WORK
```

You should now see: `C:\Users\alber\OneDrive\Documents\.WORK>`

### Step 3.3: Create the Astro Project

**Copy and paste this ENTIRE command**, then press Enter:

```bash
npm create astro@latest tstr-frontend -- --template minimal --typescript strict --install --git
```

**What this does:** Creates a new website project called "tstr-frontend"

**You might see:**
- "Need to install the following packages..." - Type `y` and press Enter
- "How would you like to start your new project?" - It should auto-select "Empty" - just press Enter
- "Install dependencies?" - Type `y` and press Enter
- "Initialize a new git repository?" - Type `y` and press Enter

**Wait 1-2 minutes** for it to download and install everything.

When it finishes, you should see: `✔ Project created!` or similar success message.

### Step 3.4: Move Into Your Project Folder

Type:
```bash
cd tstr-frontend
```

Now your prompt shows: `C:\Users\alber\OneDrive\Documents\.WORK\tstr-frontend>`

### Step 3.5: Install Additional Libraries

These are the tools needed to connect to Supabase and make your site look good.

**Copy each line, press Enter, wait for it to finish, then do the next one:**

```bash
npm install @supabase/supabase-js
```
(Wait for "added X packages")

```bash
npm install @astrojs/react @astrojs/tailwind
```
(Wait for "added X packages")

```bash
npm install react react-dom
```
(Wait for "added X packages")

```bash
npx astro add react tailwind
```
- When asked "Continue?", type `y` and press Enter
- When asked about Tailwind config, press Enter (accept default)
- Wait for "Setup complete"

✅ **All libraries installed!**

---

## PART 4: CONFIGURE YOUR PROJECT (15 minutes)

### Step 4.1: Create Environment Variables File

This stores your Supabase credentials securely.

1. **Open File Explorer**

2. **Navigate to:**
   ```
   C:\Users\alber\OneDrive\Documents\.WORK\tstr-frontend
   ```

3. **Right-click in empty space** → New → Text Document

4. **Name it:** `.env` (yes, starting with a dot, no ".txt")
   - Windows might warn you about changing extensions - click "Yes"

5. **Right-click the .env file** → Open With → Notepad

6. **Type this** (replace with your actual keys from earlier):
   ```
   PUBLIC_SUPABASE_URL=https://haimjeaetrsaauitrhfy.supabase.co
   PUBLIC_SUPABASE_ANON_KEY=your_actual_anon_key_here
   ```

7. **Save and close**

### Step 4.2: Create Supabase Connection File

1. **In File Explorer, navigate to:**
   ```
   C:\Users\alber\OneDrive\Documents\.WORK\tstr-frontend\src
   ```

2. **Create a new folder called:** `lib`

3. **Inside the `lib` folder, create a new file:**
   - Right-click → New → Text Document
   - Name it: `supabase.ts` (change extension from .txt to .ts)

4. **Open `supabase.ts` in Notepad**

5. **Paste this code:**
   ```typescript
   import { createClient } from '@supabase/supabase-js'

   const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL
   const supabaseKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY

   export const supabase = createClient(supabaseUrl, supabaseKey)
   ```

6. **Save and close**

---

## PART 5: BUILD YOUR FIRST PAGE (30 minutes)

### Step 5.1: Create a Simple Homepage

1. **Navigate to:**
   ```
   C:\Users\alber\OneDrive\Documents\.WORK\tstr-frontend\src\pages
   ```

2. **You should see a file called `index.astro`** - open it with Notepad

3. **Delete everything** and replace with this:

   ```astro
   ---
   import { supabase } from '../lib/supabase'

   // Fetch categories from database
   const { data: categories } = await supabase
     .from('categories')
     .select('*')
     .order('display_order')
   ---

   <!DOCTYPE html>
   <html lang="en">
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>TSTR.site - Global Testing Laboratory Directory</title>
   </head>
   <body>
     <header>
       <h1>TSTR.site</h1>
       <p>Global Testing Laboratory Directory</p>
     </header>

     <main>
       <h2>Browse by Industry</h2>
       <div>
         {categories?.map((category) => (
           <div key={category.id}>
             <h3>{category.name}</h3>
             <p>{category.description}</p>
           </div>
         ))}
       </div>
     </main>

     <footer>
       <p>© 2025 TSTR.site</p>
     </footer>
   </body>
   </html>
   ```

4. **Save the file**

### Step 5.2: Test Your Website Locally

1. **Go back to Command Prompt**

2. **Make sure you're in the project folder:**
   ```
   C:\Users\alber\OneDrive\Documents\.WORK\tstr-frontend>
   ```

3. **Type:**
   ```bash
   npm run dev
   ```

4. **Wait a few seconds**

5. **You should see:**
   ```
   🚀 astro v4.x.x started in XXms
   
   ┃ Local    http://localhost:4321/
   ```

6. **Open your web browser** (Chrome, Edge, Firefox)

7. **Go to:** `http://localhost:4321`

8. **You should see:**
   - "TSTR.site" heading
   - "Global Testing Laboratory Directory"
   - Your 5 testing categories listed:
     - Oil & Gas Testing
     - Pharmaceutical Testing
     - Biotech Testing
     - Environmental Testing
     - Materials Testing

✅ **If you see this, YOUR WEBSITE IS WORKING!**

---

## WHAT IF IT DOESN'T WORK?

### Error: "Cannot find module '@supabase/supabase-js'"
**Fix:** Run `npm install` again in Command Prompt

### Error: "PUBLIC_SUPABASE_URL is not defined"
**Fix:** Check your .env file - make sure it exists and has the correct keys

### Blank page or "No categories found"
**Fix:** Your Supabase keys might be wrong - double-check them

### Port 4321 already in use
**Fix:** Close any other Command Prompt windows and try again

---

## NEXT STEPS

Once your website is showing locally, come back and tell me:
**"Website is running locally!"**

Then I'll show you how to:
1. Make it look much better (add styling)
2. Add more pages (listing details, search, submit form)
3. Deploy it to the internet (make it live at tstr.site)

---

## TO STOP THE LOCAL SERVER

When you're done testing:
1. Go to Command Prompt
2. Press `Ctrl + C`
3. Type `y` when asked to terminate
4. The server stops

You can restart it anytime with `npm run dev`

---

**Ready to start? Begin with Part 1: Install Node.js!**
