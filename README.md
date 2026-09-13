# Competitor Pricing Agent 🕵️‍♂️

An automated market intelligence agent that scrapes dynamic e-commerce listings using headless browser automation and applies LLM-driven structured extraction to benchmark live market prices against internal target margins.

## 🛠️ Architecture

* **Headless Browser Automation:** Uses Playwright (`sync_api`) with Chromium to navigate JavaScript-heavy e-commerce pages, handle dynamic loading, and capture rendered DOM trees.
* **HTML Sanitization:** Cleans CSS, scripts, headers, and footers via BeautifulSoup to reduce token payload before passing text to the LLM.
* **Deterministic Pricing Extraction:** Utilizes Gemini 2.5 Flash with Pydantic structured outputs (`CompetitorPrice`) to extract product names, numeric pricing, currency codes, and availability flags.
* **Margin Benchmarking Engine:** Matches scraped market data against internal wholesale catalog economics (`marketplace_new_skus.csv`), normalizes currencies, and calculates the margin delta to identify pricing opportunities or risks.

## 💻 Tech Stack

* **Language:** Python
* **LLM Engine:** Google Gemini (`gemini-2.5-flash`)
* **Scraping & Parsing:** Playwright, BeautifulSoup4
* **Schema Validation:** Pydantic V2
* **Data Transformation:** Pandas, python-dotenv

## 🚀 Usage

1. Configure `.env` with your `GOOGLE_API_KEY`.
2. Run `python -m playwright install chromium`.
3. Execute `python benchmark_pipeline.py` to scrape competitor listings and generate `benchmarked_skus.csv`.