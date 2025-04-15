# app/services/scraper/whitepages.py
import requests
from bs4 import BeautifulSoup
import time
import random
import requests_cache

requests_cache.install_cache("scraper_cache", expire_after=7200)

def scrape_whitepages(keywords, location=""):
    results = []

    # Normalize inputs
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    if isinstance(location, list):
        location = " ".join(location)
    if not location:
        location = "usa"

    headers = {"User-Agent": "Mozilla/5.0"}

    for keyword in keywords:
        search_term = keyword.replace(" ", "-").lower()
        loc_term = location.replace(" ", "-").lower()
        url = f"https://www.whitepages.com/business/{search_term}/{loc_term}"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select(".business-card")
            
            for card in cards:
                name_tag = card.select_one(".business-name")
                phone_tag = card.select_one(".phone-number")
                address_tag = card.select_one(".address")
                
                results.append({
                    "name": name_tag.text.strip() if name_tag else "N/A",
                    "phone": phone_tag.text.strip() if phone_tag else "N/A",
                    "address": address_tag.text.strip() if address_tag else "N/A"
                })
            
            time.sleep(random.uniform(1, 2.5))
        except Exception as e:
            print(f"[WHITEPAGES ERROR] {e}")

    return results
