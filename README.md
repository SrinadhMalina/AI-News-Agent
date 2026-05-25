# AI News Agent: Autonomous Daily AI & Tech News Agent

easy-to-understand daily tech briefings directly to your phone. 

Unlike generic chatbots that create false information or summarize old trends, **AI News Agent** uses a strict time filter and organized data streams to ensure you only get verified, real-time news published within the last 48 hours.

## Key Features

* **Hallucination-Proof Engineering:** Swapped raw, messy HTML web-scraping with structured XML RSS feed processing (TechCrunch, Hacker News) to cut out webpage UI noise and layout issues.
* **Programmatic Time Shield:** Used a backend Python datetime filter (`timedelta(hours=48)`) that removes stale or historical content before it reaches the LLM's context window.
* **Intuitive Journalism Prompting:** Powered by `Qwen/Qwen2.5-Coder-32B-Instruct` via Hugging Face's Inference API, which is specifically instructed to explain why breaking news matters using bold highlights and clear markdown bullet points.
* **Self-Healing Error Handling:** Includes a custom fallback system; if cloud API token limits are reached, the agent catches the exception and sends a clean distress signal to the host via Telegram.
* **Local Automation Platform:** Set up with Windows Task Scheduler to run quietly in a dedicated Python virtual environment (`venv`) every morning, acting as a lightweight, low-maintenance local server.

## Tech Stack

* **Language:** Python 3.11+
* **Agent Framework:** `smolagents` (Hugging Face)
* **LLM Brain:** `Qwen/Qwen2.5-Coder-32B-Instruct` (InferenceClientModel)
* **Data Aggregation:** `BeautifulSoup4` & `xml.etree.ElementTree`
* **Delivery Integration:** Telegram Bot API (`requests`)
* **Environment & Security:** `python-dotenv` (Zero hardcoded secrets)