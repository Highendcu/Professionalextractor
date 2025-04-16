# app/services/scraper/manta.py
import requests
from bs4 import BeautifulSoup
import time
import random
import requests_cache

requests_cache.install_cache("scraper_cache", expire_after=7200)

def scrape_manta(keywords, location=""):
    results = []

    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    if isinstance(location, list):
        location = " ".join(location)
    if not location:
        location = "usa"

    headers = {"User-Agent": "Mozilla/5.0"}

    for keyword in keywords:
        try:
            query = keyword.replace(" ", "-")
            url = f"https://www.manta.com/search?search_source=nav&pt=business&search={query}"

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            listings = soup.select(".search-listing")

            for listing in listings:
                name = listing.select_one(".business-name a")
                phone = listing.select_one(".phone")
                address = listing.select_one(".address")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone.text.strip() if phone else "N/A",
                    "address": address.text.strip() if address else "N/A"
                })

                time.sleep(random.uniform(1.5, 2.5))
        except Exception as e:
            print("[MANTA ERROR]", e)

    return results
