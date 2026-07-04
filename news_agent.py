import os
import requests
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# 1. Load hidden credentials
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- YOUR CUSTOM SOURCES ---
MY_SOURCES = [
    "https://news.ycombinator.com/rss",
    "https://techcrunch.com/category/artificial-intelligence/feed/"
]

def send_telegram_message(message: str):
    """Sends a formatted text message to the user via Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)
    return "Message sent successfully!" if response.status_code == 200 else f"Failed: {response.text}"

def read_rss_feeds():
    """Extracts headlines from RSS feeds, strictly filtering for articles from the last 24 hours."""
    all_news = []
    now = datetime.now(timezone.utc)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for url in MY_SOURCES:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            root = ET.fromstring(response.content)
            for item in root.findall('.//item'):
                title_elem = item.find('title')
                date_elem = item.find('pubDate')
                if title_elem is None or date_elem is None:
                    continue

                title = title_elem.text
                pub_date_str = date_elem.text
                try:
                    pub_date = parsedate_to_datetime(pub_date_str)
                    if now - pub_date <= timedelta(hours=24):
                        all_news.append(title)
                except Exception:
                    pass
                if len(all_news) >= 15: # Collect a few and let AI pick the best
                    break
        except Exception as e:
            print(f"Error reading {url}: {e}")

    return all_news

def get_ollama_summary(news_list):
    """Calls local Ollama to summarize the top 3 events."""
    if not news_list:
        return "No breaking news found in the last 24 hours."

    news_text = "\n".join([f"- {t}" for t in news_list])
    prompt = f"""Act as a world-class technology journalist.
From the following list of headlines, pick the TOP 3 most important news events and write a brief, engaging summary for each.

Headlines:
{news_text}

Format your response EXACTLY like this:
*Top AI News for Today*

1. *[Company/Product]* - [Engaging summary]

2. *[Company/Product]* - [Engaging summary]

3. *[Company/Product]* - [Engaging summary]

Do NOT include any other text, introductions, or explanations."""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5-coder:1.5b",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json().get("response", "Error: No response from Ollama").strip()
    except Exception as e:
        return f"Error calling Ollama: {str(e)}"

if __name__ == "__main__":
    print("Initiating research...")

    try:
        # 1. Get News
        headlines = read_rss_feeds()

        # 2. Get Summary from Local AI
        print(f"Found {len(headlines)} articles. Summarizing...")
        summary = get_ollama_summary(headlines)

        # 3. Deliver
        send_telegram_message(summary)
        print("Success: Briefing delivered.")

    except Exception as e:
        error_message = f"🚨 *System Alert* 🚨\nAgent failed: {str(e)[:200]}"
        send_telegram_message(error_message)
        print(f"Failed. Error details: {str(e)}")
