# app/services/scraper/bbb.py
import requests
from bs4 import BeautifulSoup
import time
import random
import requests_cache

requests_cache.install_cache("scraper_cache", expire_after=7200)

def scrape_bbb(keywords, location=""):
    results = []

    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    if isinstance(location, list):
        location = " ".join(location)

    headers = {"User-Agent": "Mozilla/5.0"}

    for keyword in keywords:
        try:
            search = keyword.replace(" ", "+")
            loc = location.replace(" ", "+")
            url = f"https://www.bbb.org/search?find_country=USA&find_text={search}&find_loc={loc}"

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            cards = soup.select(".SearchResults__resultItem")

            for card in cards:
                name = card.select_one(".ResultItem__BusinessTitle")
                phone = card.select_one(".Phone__PhoneNumber")
                address = card.select_one(".ResultItem__BusinessAddress")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone.text.strip() if phone else "N/A",
                    "address": address.text.strip() if address else "N/A"
                })

            time.sleep(random.uniform(1, 2.5))
        except Exception as e:
            print(f"[BBB ERROR] {e}")

    return results
