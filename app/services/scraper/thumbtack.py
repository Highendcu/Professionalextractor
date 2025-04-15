# app/services/scraper/thumbtack.py
import requests
from bs4 import BeautifulSoup
import time
import random
import requests_cache

requests_cache.install_cache("scraper_cache", expire_after=7200)

def scrape_thumbtack(keywords, location=""):
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
            search = keyword.replace(" ", "-").lower()
            url = f"https://www.thumbtack.com/k/{search}/"

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            profiles = soup.select(".JobCard")

            for prof in profiles:
                name = prof.select_one(".sc-dkzDqf")
                phone = "N/A"
                address = prof.select_one(".sc-bcXHqe")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone,
                    "address": address.text.strip() if address else "N/A"
                })

            time.sleep(random.uniform(1, 2.5))

        except Exception as e:
            print(f"[THUMBTACK ERROR] {e}")

    return results
