# app/services/scraper/houzz.py
import requests
from bs4 import BeautifulSoup
import time
import random
import requests_cache

requests_cache.install_cache("scraper_cache", expire_after=7200)

def scrape_houzz(keywords, location=""):
    results = []

    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]

    if isinstance(urls, str):
        urls = [u.strip() for u in urls.split(",") if u.strip()]

    # Ensure return format is like:
    return [{
       "number": phone,
        "name": name,
        "address": address
    } for ...]

    headers = {"User-Agent": "Mozilla/5.0"}

    for keyword in keywords:
        try:
            search = keyword.replace(" ", "-").lower()
            url = f"https://www.houzz.com/professionals/{search}"

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            listings = soup.select(".hz-pro-search-result")

            for listing in listings:
                name = listing.select_one("a.hz-pro-name")
                phone = "N/A"
                address = listing.select_one(".hz-pro-location")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone,
                    "address": address.text.strip() if address else "N/A"
                })

            time.sleep(random.uniform(1, 2.5))
        except Exception as e:
            print(f"[HOUZZ ERROR] {e}")

    return results
