import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_bbb(keywords, location=""):
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
            kw = keyword.replace(" ", "+")
            loc = location.replace(" ", "+")
            url = f"https://www.bbb.org/search?find_country=USA&find_text={kw}&find_loc={loc}"

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            listings = soup.select("div.SearchResults__sc-j6tvzb-0")

            for listing in listings[:15]:
                name = listing.select_one("a[data-testid='business-title-link']")
                phone = listing.select_one("p[data-testid='business-phone']")
                address = listing.select_one("p[data-testid='business-address']")

                results.append({
                    "name": name.text.strip() if name else "N/A",
                    "phone": phone.text.strip() if phone else "N/A",
                    "address": address.text.strip() if address else "N/A"
                })

            time.sleep(random.uniform(1.2, 2.0))

        except Exception as e:
            print(f"[BBB ERROR] {e}")

    return results
