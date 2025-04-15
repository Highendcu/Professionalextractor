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
            search = keyword.replace(" ", "+")
            url = f"https://www.manta.com/search?search_source=nav&search={search}"

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            listings = soup.select("div.card")

            for entry in listings:
                name = entry.select_one("a.business-name")
                phone = entry.select_one("span.card-phone")
                address = entry.select_one("div.card-location")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone.text.strip() if phone else "N/A",
                    "address": address.text.strip() if address else "N/A"
                })

            time.sleep(random.uniform(1, 2.5))

        except Exception as e:
            print(f"[MANTA ERROR] {e}")

    return results
