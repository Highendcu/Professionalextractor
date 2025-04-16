# app/services/scraper/yellowpages.py
import requests
import requests_cache
from bs4 import BeautifulSoup
import time
import random

requests_cache.install_cache("scraper_cache", expire_after=7200)

def scrape_yellowpages(urls, keywords, country="us", state=""):
    results = []

    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    location = state or country  # <- FIXED
    headers = {"User-Agent": "Mozilla/5.0"}

    for keyword in keywords:
        search_url = f"https://www.yellowpages.com/search?search_terms={keyword}&geo_location_terms={location}"

        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            listings = soup.select(".result")

            for listing in listings:
                name = listing.select_one(".business-name span")
                phone = listing.select_one(".phones")
                address = listing.select_one(".street-address")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone.text.strip() if phone else "N/A",
                    "address": address.text.strip() if address else "N/A"
                })

                time.sleep(random.uniform(1.5, 2.5))
        except Exception as e:
            print("[YELLOWPAGES ERROR]", e)

    return results
