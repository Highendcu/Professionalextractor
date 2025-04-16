import requests
import requests_cache
from bs4 import BeautifulSoup
import time
import random

requests_cache.install_cache("scraper_cache", expire_after=7200)

def scrape_yellowpages(urls, keywords, country="us", state=""):
    results = []

    if not keywords:
        keywords = ["plumber", "electrician", "restaurant"]

    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]

    location = state or country
    headers = {"User-Agent": "Mozilla/5.0"}

    for keyword in keywords:
        search_url = f"https://www.yellowpages.com/search?search_terms={keyword}&geo_location_terms={location}"
        print(f"[YELLOWPAGES] Scraping: {search_url}")

        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            listings = soup.select("div.result")

            print(f"[YELLOWPAGES] Found {len(listings)} listings")

            for listing in listings:
                info = listing.select_one("div.info")

                name = info.select_one("a.business-name") if info else None
                phone = info.select_one(".phones") if info else None
                address = info.select_one(".street-address") if info else None

                extracted = {
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone.text.strip() if phone else "N/A",
                    "address": address.text.strip() if address else "N/A"
                }

                print("[YELLOWPAGES EXTRACTED]", extracted)
                results.append(extracted)
                time.sleep(random.uniform(1.2, 1.8))

        except Exception as e:
            print("[YELLOWPAGES ERROR]", e)

    return results
