import os
import requests
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel, tool

# 1. Load hidden credentials
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HF_TOKEN = os.getenv("HF_TOKEN")

# --- YOUR CUSTOM SOURCES ---
MY_SOURCES = [
    "https://news.ycombinator.com/rss", 
    "https://techcrunch.com/category/artificial-intelligence/feed/"
]

# 2. Telegram Delivery Tool
@tool
def send_telegram_message(message: str) -> str:
    """
    Sends a formatted text message to the user via Telegram.
    Args:
        message: The news summary string to send.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)
    return "Message sent successfully!" if response.status_code == 200 else f"Failed: {response.text}"

# 3. UPGRADED TOOL: Bulletproof RSS Filter
@tool
def read_rss_feed(url: str) -> str:
    """
    Extracts the exact headlines and dates from an RSS feed, strictly filtering for articles from the last 48 hours.
    Args:
        url: The RSS feed URL to read.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        root = ET.fromstring(response.content)
        
        news_items = []
        now = datetime.now(timezone.utc)
        
        for item in root.findall('.//item'):
            title = item.find('title').text
            pub_date_str = item.find('pubDate').text
            
            if pub_date_str:
                try:
                    # Convert RSS string to actual Python time object
                    pub_date = parsedate_to_datetime(pub_date_str)
                    
                    # THE SHIELD: Discard the article if it is older than 48 hours
                    if now - pub_date <= timedelta(hours=48):
                        news_items.append(f"Date: {pub_date_str} | Title: {title}")
                except Exception:
                    pass
            
            # Cap at 10 recent items so we don't overload the AI's memory
            if len(news_items) >= 10:
                break
                
        if not news_items:
            return f"No breaking news found in the last 48 hours for {url}."
            
        return "\n".join(news_items)
    except Exception as e:
        return f"Failed to read feed {url}. Error: {str(e)}"

# 4. Give the Agent a Brain (LLM)
model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=HF_TOKEN
)

# 5. Initialize the Agent
agent = CodeAgent(
    tools=[read_rss_feed, send_telegram_message], 
    model=model,
    add_base_tools=True
)

today_date = datetime.now().strftime("%B %d, %Y")

# 6. The Bulletproof Mission Directive
mission = f"""
Act as a world-class technology journalist. Today's date is {today_date}.
1. You MUST use the `read_rss_feed` tool to look at the latest articles from: {MY_SOURCES}
2. Find UP TO 3 most important news events. STRICT RULE: If the tool returns fewer than 3 recent articles, do NOT make up news to fill the gap. Just report what you found. It is 100% okay to only report 1 or 2 items if that is all the tool gives you.
3. Write a highly engaging summary. You MUST include the actual name of the product, company, or specific event.
4. Use the `send_telegram_message` tool to deliver the final text.
"""

if __name__ == "__main__":
    print("Initiating custom source research...")
    
    try:
        agent.run(mission)
        print("Success: Briefing delivered.")
    except Exception as e:
        exhausted_message = "🚨 *System Alert* 🚨\nAPI Tokens Exhausted or connection failed."
        send_telegram_message(exhausted_message)
        print(f"Failed. Exhaustion signal sent. Error details: {str(e)[:150]}")