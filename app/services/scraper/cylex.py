import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_cylex(keywords, location=""):
    results = []

    headers = {"User-Agent": "Mozilla/5.0"}
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    loc = location.strip().replace(" ", "+") or "united+states"

    for keyword in keywords:
        try:
            kw = keyword.replace(" ", "+")
            url = f"https://www.cylex.us.com/search/{kw}/{loc}.htm"

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            listings = soup.select(".entry")

            for listing in listings[:15]:
                name = listing.select_one("h3 > a")
                phone = listing.select_one(".entry-phones span")
                address = listing.select_one(".address")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone.text.strip() if phone else "N/A",
                    "address": address.text.strip() if address else "N/A"
                })

            time.sleep(random.uniform(1.5, 2.5))

        except Exception as e:
            print(f"[CYLEX ERROR] {e}")

    return results
