# app/services/scraper/yelp.py
import requests
from bs4 import BeautifulSoup
import time
import random
import requests_cache

requests_cache.install_cache("scraper_cache", expire_after=7200)

def scrape_yelp(keywords, location=""):
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
            search = keyword.replace(" ", "+")
            loc = location.replace(" ", "+")
            url = f"https://www.yelp.com/search?find_desc={search}&find_loc={loc}"

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            listings = soup.select("[data-testid='serp-ia-card']")

            for listing in listings:
                name = listing.select_one("[data-testid='serp-ia-card-header']")
                phone = listing.select_one("p.css-1p9ibgf")
                address = listing.select_one("address")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone.text.strip() if phone else "N/A",
                    "address": address.text.strip() if address else "N/A"
                })

            time.sleep(random.uniform(1, 2.5))
        except Exception as e:
            print(f"[YELP ERROR] {e}")

    return results
