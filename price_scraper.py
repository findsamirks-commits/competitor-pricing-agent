import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from playwright.sync_api import sync_playwright
import time

load_dotenv()

class CompetitorPrice(BaseModel):
    product_name: str = Field(description="The full name of the competitor's product")
    price: float = Field(description="The numeric selling price")
    currency: str = Field(description="The currency code, e.g., INR or USD")
    in_stock: bool = Field(description="True if the item is available for purchase")

def scrape_competitor_page(url: str) -> str:
    print(f"🕵️‍♂️ Launching headless browser to scrape: {url}")
    
    with sync_playwright() as p:
        # Launch Chromium in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Navigate to the target URL and wait for the network to idle
            page.goto(url, wait_until="networkidle")
            
            # Briefly sleep to allow any lazy-loaded pricing grids to render
            time.sleep(3)
            
            # Extract the fully rendered HTML
            html_content = page.content()
            return html_content
            
        except Exception as e:
            print(f"❌ Failed to scrape page: {e}")
            return ""
            
        finally:
            browser.close()

def parse_competitor_price(raw_html: str):
    print("🧹 Cleaning HTML DOM to save tokens...")
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # Strip heavy, invisible elements like JavaScript and CSS
    for element in soup(["script", "style", "header", "footer"]):
        element.extract()
        
    clean_text = soup.get_text(separator=" ", strip=True)
    
    print("🧠 Extracting market data with Gemini...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    structured_llm = llm.with_structured_output(CompetitorPrice)
    
    # Pass the compressed text to the LLM
    prompt = f"Extract the primary product pricing details from this webpage text:\n{clean_text[:40000]}"
    return structured_llm.invoke(prompt)

if __name__ == "__main__":
    # Test the scraper on a sample URL
    test_url = "https://www.indiamart.com/proddetail/turtle-wax-pro-t30-fine-car-polish-compound-1l-2850841938888.html"
    raw_html = scrape_competitor_page(test_url)
    
    if raw_html:
        market_data = parse_competitor_price(raw_html)
        print("\n✅ Competitor Extraction Complete:")
        print(f"Product: {market_data.product_name}")
        print(f"Market Price: {market_data.price} {market_data.currency}")
        print(f"In Stock: {market_data.in_stock}")