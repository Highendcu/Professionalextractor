import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_angi(keywords, location=""):
    results = []

    headers = {"User-Agent": "Mozilla/5.0"}
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    if isinstance(location, list):
        location = " ".join(location)
    if not location:
        location = "usa"

    for keyword in keywords:
        try:
            kw = keyword.replace(" ", "-").lower()
            loc = location.replace(" ", "-").lower()
            url = f"https://www.angi.com/companylist/{loc}/{kw}.htm"

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            listings = soup.select(".listing")

            for listing in listings[:15]:
                name = listing.select_one("h2 a")
                phone = listing.select_one(".phone")
                address = listing.select_one(".listing-address")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone.text.strip() if phone else "N/A",
                    "address": address.text.strip() if address else "N/A"
                })

            time.sleep(random.uniform(1.5, 2.5))

        except Exception as e:
            print(f"[ANGI ERROR] {e}")

    return results
