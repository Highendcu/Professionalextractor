# app/services/scraper/yellowpages.py
import requests_cache
import requests
from bs4 import BeautifulSoup
import time
import random

requests_cache.install_cache("scraper_cache", expire_after=7200)

def scrape_yellowpages(urls, keywords, country="us", state=""):
    results = []

    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    if isinstance(location, list):
        location = " ".join(location)
    if not location:
        location = "usa"

    headers = {"User-Agent": "Mozilla/5.0"}

    for keyword in keywords:
        search_url = f"https://www.yellowpages.com/search?search_terms={keyword}&geo_location_terms={state or country}"

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

                time.sleep(random.uniform(1.5, 2.5))  # Throttle to avoid ban
        except Exception as e:
            print("Error scraping YellowPages:", e)

    return results
