# import os
# import random
# import time
# from playwright.sync_api import sync_playwright
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# analyzer = SentimentIntensityAnalyzer()

# FB_EMAIL = "ramadevimalina38@gmail.com"
# FB_PASSWORD = "#fY2W>N9Cc5a"
# STATE_PATH = "./fb_auth_state.json" 

# def evaluate_sentiment(comments):
#     if not comments:
#         return "neutral"
        
#     total_compound = 0.0
#     laugh_indicators = ["😂", "💀", "😭", "lmao", "lmfao", "hahaha", "haha"]
#     laugh_count = 0

#     for comment in comments:
#         text_lower = comment.lower()
#         if any(token in text_lower for token in laugh_indicators):
#             laugh_count += 1
#         score = analyzer.polarity_scores(comment)
#         total_compound += score['compound']

#     avg_compound = total_compound / len(comments)
#     laugh_ratio = laugh_count / len(comments)

#     print(f"Metrics -> Avg Compound: {avg_compound:.2f} | Laugh Ratio: {laugh_ratio * 100:.1f}%")

#     if laugh_ratio > 0.30 or avg_compound > 0.4:
#         return "positive_funny"
#     elif avg_compound < -0.3:
#         return "negative_rage"
#     return "neutral"

# def run_facebook_pipeline(reel_urls):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        
#         if os.path.exists(STATE_PATH):
#             context = browser.new_context(storage_state=STATE_PATH)
#             print("Loaded Facebook session from cache.")
#         else:
#             context = browser.new_context()
#             print("No session found. Initializing login flow...")

#         page = context.new_page()

#        # Handle Authentication
#         if not os.path.exists(STATE_PATH):
#             print("Navigating to Facebook landing page...")
#             page.goto("https://www.facebook.com")
#             page.wait_for_timeout(3000)
            
#             # 1. Handle any Cookie Banner overlays instantly
#             try: 
#                 page.click('button[data-cookiebanner="accept_button"]', timeout=4000)
#                 print("Cookie banner cleared.")
#             except: 
#                 pass
            
#             # 2. Check if Facebook redirected you straight to a checkpoint/login gate
#             current_url = page.url
#             if "checkpoint" in current_url or "login" in current_url:
#                 print("\n⚠️ SECURITY CHECKPOINT DETECTED! ⚠️")
#                 print("Facebook is asking for validation or manual authentication.")
#                 print("Please look at the open Chromium window, complete the login manually,")
#                 print("and pass any 2FA/security checks right now.")
                
#                 # Give yourself 60 full seconds to type credentials and pass the check manually in the window
#                 print("Waiting 60 seconds for manual login completion...")
#                 page.wait_for_url("https://www.facebook.com/**", timeout=60000)
#             else:
#                 # No proactive checkpoint triggered; execute standard automated injection
#                 try:
#                     page.fill('input[id="email"]', FB_EMAIL, timeout=5000)
#                     page.fill('input[id="pass"]', FB_PASSWORD, timeout=5000)
#                     page.click('button[name="login"]')
#                     print("Automated credentials submitted. Waiting for dashboard...")
#                     page.wait_for_url("https://www.facebook.com/**", timeout=15000)
#                 except Exception as login_err:
#                     print(f"Automated inputs failed, switching to manual fallback: {login_err}")
#                     print("Please log in manually inside the open browser window now...")
#                     page.wait_for_timeout(30000) # Give 30 seconds for manual rescue
            
#             # Save the state once you are safely inside the dashboard
#             context.storage_state(path=STATE_PATH)  
#             print("🎉 Login successful! Session state saved to storage.")

# # Process URL Queue
#         for url in reel_urls:
#             print(f"\nTargeting Reel: {url}")
#             page.goto(url)
#             page.wait_for_timeout(6000) # Give the interface full time to settle

#             # CRITICAL FIX 1: Smash any cookie overlays blocking the Reel viewport
#             try:
#                 # Look for standard cookie acceptance buttons specifically on the Reel layout
#                 cookie_selectors = [
#                     'button[data-cookiebanner="accept_button"]',
#                     'div[aria-label="Allow all cookies"]',
#                     'div[role="dialog"] div[aria-label="Decline optional cookies"]'
#                 ]
#                 for selector in cookie_selectors:
#                     if page.locator(selector).is_visible():
#                         page.locator(selector).click()
#                         print("Cleared overlay dialog blocking the Reel.")
#                         page.wait_for_timeout(1000)
#                         break
#             except:
#                 pass

#             # TARGETED EXTRACTION (Comments drawer verification)
#             comment_elements = page.locator('div[dir="auto"] div[style*="text-align: start"]').all_text_contents()
#             raw_comments = [c.strip() for c in comment_elements if len(c.strip()) > 3]
#             print(f"Extracted {len(raw_comments)} comments for evaluation.")

#             vibe = evaluate_sentiment(raw_comments[:20]) 

#             # CRITICAL FIX 2: Target the exact interactive BUTTON element structure, not just a label
#             # We use an XPATH that strictly hunts for a clickable role element containing the Like label
#             like_btn = page.locator('div[role="button"][aria-label="Like"]').first
            
#             try:
#                 # Verify element state before firing click engine
#                 if like_btn.is_visible():
#                     if vibe == "positive_funny":
#                         print("Action: Funny vibe caught. Hovering for dynamic tray...")
#                         like_btn.scroll_into_view_if_needed()
#                         like_btn.hover() 
                        
#                         page.wait_for_selector('div[aria-label="Haha"]', state="visible", timeout=3000)
#                         page.click('div[aria-label="Haha"]')
#                         print("Reaction 'Haha' successfully registered!")
                        
#                     elif vibe == "neutral":
#                         print("Action: Neutral vibe. Instantiating precise hardware click.")
#                         like_btn.scroll_into_view_if_needed()
                        
#                         # Force a hardware-level click to ensure it pierces any layer
#                         like_btn.click(force=True)
#                         print("Reaction 'Like' successfully registered!")
                        
#                     else:
#                         print("Action: Negative vibe. Skipping profile footprint interaction.")
#                 else:
#                     print("⚠️ Could not execute action: The interactive Like button element is hidden or not rendered.")
                    
#             except Exception as e:
#                 print(f"Action execution workflow broken on current selector: {str(e)}")

#             # Strategic randomized anti-bot throttling cooldown
#             cooldown = random.uniform(12.0, 25.0)
#             print(f"Cooling down for {cooldown:.1f} seconds...")
#             # page.wait_for_timeout(cooldown * 1000)
#             cooldown = random.uniform(12.0, 25.0)
#             print(f"Cooling down for {cooldown:.1f} seconds safely in terminal...")
#             time.sleep(cooldown)

#         browser.close()

# if __name__ == "__main__":
#     target_fb_reels = [
#         "https://www.facebook.com/reel/2307852066411253"
        
#     ]
#     run_facebook_pipeline(target_fb_reels)

import os
import random
import time
from playwright.sync_api import sync_playwright

# Configuration
FB_EMAIL = "ramadevimalina38@gmail.com"
FB_PASSWORD = "#fY2W>N9Cc5a"
STATE_PATH = "./fb_auth_state.json" 

def run_facebook_pipeline(reel_urls):
    with sync_playwright() as p:
        # Launch window in non-headless mode for tracking verification
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        
        if os.path.exists(STATE_PATH):
            context = browser.new_context(storage_state=STATE_PATH, no_viewport=True)
            print("Loaded session state from cache.")
        else:
            context = browser.new_context(no_viewport=True)
            print("No session cache found. Building fresh state profile...")

        page = context.new_page()

        # Step 1: Force baseline landing page verification
        print("Navigating to baseline feed to confirm account session state...")
        page.goto("https://www.facebook.com")
        page.wait_for_timeout(5000) # Give session cookies time to shake hands

        # Handle Initial Authentication if cache is blank or rejected
        if not os.path.exists(STATE_PATH) or "login" in page.url or "checkpoint" in page.url:
            print("\n🔒 PLEASE LOG IN MANUALLY NOW!")
            print("The script is pausing for 90 seconds. Go to the open Chrome window,")
            print("type your email/password, handle any 2FA codes, and press Log In.")
            
            # Changed to 90000ms (1.5 minutes) to give you breathing room
            page.wait_for_url("https://www.facebook.com/**", timeout=90000)
            
            # Give the browser 5 seconds to fully settle and write cookies before saving
            page.wait_for_timeout(5000)
            context.storage_state(path=STATE_PATH)
            print("Session tokens captured and written to local file state.")

        # Step 2: Loop Target Queue
        for url in reel_urls:
            print(f"\nJumping to Target Reel: {url}")
            page.goto(url)
            page.wait_for_timeout(7000) # Give video assets and layout frames ample time to paint

            # Dismiss any cookie blocking dialog modals
            try:
                if page.locator('button[data-cookiebanner="accept_button"]').is_visible():
                    page.locator('button[data-cookiebanner="accept_button"]').click()
                    print("Cleared privacy shield overlay.")
            except:
                pass

            print("Locating interactive sidebar elements...")

            # Target strictly the visible button component on the right-hand panel
            like_btn = page.locator('div[role="button"][aria-label="Like"]').locator('visible=true').first

            try:
                if like_btn.is_visible():
                    print("Active Like button located in current viewport. Aligning hardware cursor...")
                    like_btn.scroll_into_view_if_needed()
                    page.wait_for_timeout(1000)
                    
                    # Fire hardware action link
                    like_btn.click(force=True)
                    print("🚀 Hardware click interaction dispatched successfully!")
                else:
                    print("⚠️ Execution error: The visible Like element failed to render in the DOM tree.")
            except Exception as ex:
                print(f"Interaction engine failure: {str(ex)}")

            # Console throttling cooldown
            cooldown = random.uniform(10.0, 15.0)
            print(f"Holding thread connection active for {cooldown:.1f} seconds to allow pipeline synchronization...")
            time.sleep(cooldown)

        browser.close()

if __name__ == "__main__":
    target_fb_reels = [
        "https://www.facebook.com/reel/2307852066411253"
    ]
    run_facebook_pipeline(target_fb_reels)