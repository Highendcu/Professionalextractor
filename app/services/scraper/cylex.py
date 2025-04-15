# app/services/scraper/cylex.py
import requests
from bs4 import BeautifulSoup
import time
import random
import requests_cache

requests_cache.install_cache("scraper_cache", expire_after=7200)

def scrape_cylex(keywords, location=""):
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
            url = f"https://www.cylex.us.com/search?term={search}&location={location}"

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            items = soup.select(".searchResultsItem")

            for item in items:
                name = item.select_one(".title")
                phone = item.select_one(".phone")
                address = item.select_one(".address")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone.text.strip() if phone else "N/A",
                    "address": address.text.strip() if address else "N/A"
                })

            time.sleep(random.uniform(1, 2.5))
        except Exception as e:
            print(f"[CYLEX ERROR] {e}")

    return results
