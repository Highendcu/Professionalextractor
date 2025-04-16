# app/services/scraper/whitepages.py
import requests
from bs4 import BeautifulSoup
import time
import random
import requests_cache

requests_cache.install_cache("scraper_cache", expire_after=7200)

def scrape_whitepages(keywords, location=""):
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
            query = keyword.replace(" ", "+")
            loc = location.replace(" ", "+")
            url = f"https://www.whitepages.com/business/search?utf8=✓&what={query}&where={loc}"

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            listings = soup.select("div.ListingCard")

            for listing in listings:
                name = listing.select_one("a.listing-name")
                phone = listing.select_one("span.PhoneNumber")
                address = listing.select_one("div.Address")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone.text.strip() if phone else "N/A",
                    "address": address.text.strip() if address else "N/A"
                })

                time.sleep(random.uniform(1.2, 2.0))
        except Exception as e:
            print("[WHITEPAGES ERROR]", e)

    return results
