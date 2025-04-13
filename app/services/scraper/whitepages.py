# app/services/scraper/whitepages.py
import requests
from bs4 import BeautifulSoup
import requests_cache
import time
import random

requests_cache.install_cache("scraper_cache", expire_after=7200)

def scrape_whitepages(keywords, location=""):
    results = []

    # Normalize input
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    if isinstance(location, list):
        location = " ".join(location)
    elif not location:
        location = "united-states"

    headers = {"User-Agent": "Mozilla/5.0"}

    for keyword in keywords:
        query = keyword.replace(" ", "-")
        loc = location.replace(" ", "-")
        url = f"https://www.whitepages.com/name/{query}/{loc}"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            people = soup.select("div.card.person")
            for p in people:
                name = p.select_one("a.name")
                address = p.select_one("div.address")
                phone = p.select_one("div.phone")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "address": address.text.strip() if address else "N/A",
                    "phone": phone.text.strip() if phone else "N/A"
                })

                time.sleep(random.uniform(1.5, 2.5))  # Throttle

        except Exception as e:
            print(f"[WHITEPAGES ERROR] {e}")

    return results
