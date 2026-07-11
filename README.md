# AI News Agent: Autonomous Daily AI & Tech News Agent

Easy-to-understand daily tech briefings delivered directly to your phone.

Unlike generic chatbots that create false information or summarize old trends, **AI News Agent** uses a strict time filter and organized data streams to ensure you only get verified, real-time news published within the last 24 hours.

## Key Features

* **Hallucination-Proof Engineering:** Swapped raw, messy HTML web-scraping with structured XML RSS feed processing (TechCrunch, Hacker News) to cut out webpage UI noise and layout issues.
* **Programmatic Time Shield:** Used a backend Python datetime filter (`timedelta(hours=24)`) that removes stale or historical content before it reaches the LLM's context window.
* **Local Intelligence:** Powered by `qwen2.5-coder:1.5b` running locally via **Ollama**, ensuring privacy and removing dependence on external cloud API quotas.
* **Self-Healing Error Handling:** Includes a custom fallback system; if the local AI service is unavailable, the agent catches the exception and sends a clean distress signal to the host via Telegram.
* **Local Automation Platform:** Set up with Windows Task Scheduler to run quietly in a dedicated Python virtual environment (`venv`) every morning, acting as a lightweight, low-maintenance local server.

## Tech Stack

* **Language:** Python 3.11+
* **LLM Brain:** `qwen2.5-coder:1.5b` via Local Ollama
* **Data Aggregation:** `BeautifulSoup4` & `xml.etree.ElementTree`
* **Delivery Integration:** Telegram Bot API (`requests`)
* **Environment & Security:** `python-dotenv` (Zero hardcoded secrets)
