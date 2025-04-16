import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_houzz(keywords, location=""):
    results = []

    headers = {"User-Agent": "Mozilla/5.0"}
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    loc = location.strip().replace(" ", "-").lower() or "united-states"

    for keyword in keywords:
        try:
            kw = keyword.replace(" ", "-").lower()
            url = f"https://www.houzz.com/professionals/{kw}/service--{loc}"

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            listings = soup.select("div.hz-pro-search-results__listing")

            for listing in listings[:15]:
                name = listing.select_one(".hz-pro-search-results__name")
                phone = listing.select_one(".hz-pro-search-results__phone-number")
                address = listing.select_one(".hz-pro-search-results__location")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone.text.strip() if phone else "N/A",
                    "address": address.text.strip() if address else "N/A"
                })

            time.sleep(random.uniform(1.5, 2.5))

        except Exception as e:
            print(f"[HOUZZ ERROR] {e}")

    return results
