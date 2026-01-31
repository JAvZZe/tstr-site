
import asyncio
from playwright.async_api import async_playwright

# TARGET URL
LINKEDIN_URL = "https://www.linkedin.com/company/110325576/admin/settings/"

async def main():
    async with async_playwright() as p:
        try:
            # Retry loop for connection
            browser = None
            for i in range(5):
                for addr in ["http://127.0.0.1:9222", "http://localhost:9222", "http://[::1]:9222"]:
                    try:
                        print(f"Attempting connect to {addr} (Try {i+1}/5)...")
                        browser = await p.chromium.connect_over_cdp(addr)
                        print("Connected!")
                        break
                    except Exception:
                        pass
                if browser:
                    break
                await asyncio.sleep(2)
            
            if not browser:
                print("Could not connect to Chrome debugging port after multiple attempts.")
                return

            # Get the active context
            context = browser.contexts[0]
            
            # Find the LinkedIn tab or open it
            page = None
            for p_obj in context.pages:
                if "linkedin.com" in p_obj.url:
                    page = p_obj
                    print(f"Found existing LinkedIn tab: {page.url}")
                    break
            
            if not page:
                print("Opening new tab for LinkedIn...")
                page = await context.new_page()
                await page.goto(LINKEDIN_URL)
            else:
                await page.goto(LINKEDIN_URL) # Refresh/Ensure correct page
            
            # Wait for content to load
            print("Waiting for page load...")
            await page.wait_for_load_state("networkidle")
            
            # EXTRACT DATA
            # NOTE: This selector might need adjustment based on the actual DOM of the "Following" page
            # We'll grab the whole body text first to be safe if specific selectors fail
            content = await page.content()
            
            # Simple text extraction for processing
            text_content = await page.evaluate("document.body.innerText")
            
            print("\n----- EXTRACTED CONTENT START -----")
            print(text_content[:2000] + "...") # Print first 2000 chars
            print("----- EXTRACTED CONTENT END -----\n")
            
            # Save raw HTML for offline parsing if needed
            with open("linkedin_dump.html", "w") as f:
                f.write(content)
            
            print("Dumped HTML to linkedin_dump.html")
            
            await browser.close()
            
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure Chrome is running with: google-chrome --remote-debugging-port=9222")

if __name__ == "__main__":
    asyncio.run(main())
