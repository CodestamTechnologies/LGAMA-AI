from playwright.sync_api import sync_playwright

def run_google_scraper(query, max_scrolls=10):
    filename = None
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("\033[94mLaunching Chromium browser...\033[0m")  # Blue color
        
        page.goto("https://www.google.com/", timeout=60000)
        page.get_by_label("Search", exact=True).click()
        
        print("\033[94mNavigating to Google search page...\033[0m")  # Blue color
        
        # Update the search query
        page.get_by_label("Search", exact=True).fill(query)
        page.keyboard.press("Enter")
        
        print("\033[94mPerforming Google search...\033[0m")  # Blue color
        
        # Wait for navigation to complete
        page.wait_for_load_state("networkidle")
        
        try:
            # Keep track of previous scroll height
            prev_scroll_height = 0
            scroll_count = 0
            
            while scroll_count < max_scrolls:
                # Get current scroll height
                scroll_height = page.evaluate("document.documentElement.scrollHeight")
                
                # Scroll to the bottom of the page
                page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
                
                print(f"\033[94mScrolling... {scroll_count}/{max_scrolls}\033[0m")  # Blue color
                
                # Wait for a short period to allow new content to load
                page.wait_for_timeout(1000)
                
                # Check if scroll height has changed (indicating new content)
                if scroll_height > prev_scroll_height:
                    prev_scroll_height = scroll_height
                else:
                    # If no new content is loaded, break the loop
                    break
                
                scroll_count += 1
        
        except Exception as e:
            if "Target page, context or browser has been closed" in str(e):
                print("\033[91mTarget page, context, or browser has been closed. Exiting loop.\033[0m")  # Red color
            else:
                print(f"\033[91mError occurred: {str(e)}\033[0m")  # Red color
        
        finally:
            # Get the text content of the page
            page_text = page.inner_text("body")
            # Write the page text content to a text file
            filename = "scraped_content.txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(page_text)
            
            print("\033[94mScraping complete. Content saved to file.\033[0m")  # Blue color
            
            # Wait for additional 3 seconds after loading all content
            page.wait_for_timeout(3000)
    
    return filename
