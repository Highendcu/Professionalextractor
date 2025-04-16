import threading
import time
from datetime import datetime
from flask_socketio import emit
from app.services.scraper.yellowpages import scrape_yellowpages
from app.services.scraper.whitepages import scrape_whitepages
from app.services.scraper.manta import scrape_manta
from app.services.scraper.yelp import scrape_yelp
from app.services.scraper.bbb import scrape_bbb
from app.services.scraper.hotfrog import scrape_hotfrog
from app.services.scraper.cylex import scrape_cylex
from app.services.scraper.angi import scrape_angi
from app.services.scraper.houzz import scrape_houzz
from app.services.scraper.thumbtack import scrape_thumbtack

# Shared state
EXTRACTION_DATA = []
EXTRACTION_ACTIVE = False
DATA_LOCK = threading.Lock()

# Map of platform to scraper function
SCRAPER_MAP = {
    "yellowpages": scrape_yellowpages,
    "whitepages": scrape_whitepages,
    "manta": scrape_manta,
    "yelp": scrape_yelp,
    "bbb": scrape_bbb,
    "hotfrog": scrape_hotfrog,
    "cylex": scrape_cylex,
    "angi": scrape_angi,
    "houzz": scrape_houzz,
    "thumbtack": scrape_thumbtack
}

socketio = None  # Placeholder

def set_socketio(sio):
    global socketio
    socketio = sio
    print("[DEBUG] SocketIO instance has been set.")

def start_extraction(urls, keywords, platforms, country, state):
    global EXTRACTION_ACTIVE
    EXTRACTION_ACTIVE = True
    print("[DEBUG] Starting extraction thread...")

    with DATA_LOCK:
        EXTRACTION_DATA.clear()

    if isinstance(urls, str):
        urls = [u.strip() for u in urls.split(",") if u.strip()]
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    if not keywords:
        keywords = ["plumber"]

    print(f"[DEBUG] Platforms: {platforms}")
    print(f"[DEBUG] URLs: {urls}")
    print(f"[DEBUG] Keywords: {keywords}")
    print(f"[DEBUG] Country: {country}, State: {state}")

    def process():
        global EXTRACTION_ACTIVE
        total_count = 0

        for platform in platforms:
            if not EXTRACTION_ACTIVE:
                break

            scraper = SCRAPER_MAP.get(platform)
            if scraper:
                try:
                    print(f"[DEBUG] Running scraper for platform: {platform}")
                    results = scraper(urls, keywords, country, state)
                    print(f"[DEBUG] Scraper returned {len(results)} results")

                    with DATA_LOCK:
                        EXTRACTION_DATA.extend(results)
                        total_count += len(results)

                    if socketio:
                        socketio.emit("update", {
                            "new_count": len(results),
                            "total_count": total_count
                        })

                        socketio.emit("extraction_update", {
                            "data": results
                        })
                        print("[DEBUG] Emitted data to client")
                    else:
                        print("[WARN] socketio not initialized")

                except Exception as e:
                    print(f"[ERROR] {platform} failed: {e}")

        EXTRACTION_ACTIVE = False
        print("[DEBUG] Extraction completed.")

    thread = threading.Thread(target=process)
    thread.start()

def stop_extraction():
    global EXTRACTION_ACTIVE
    EXTRACTION_ACTIVE = False
    print("[DEBUG] Extraction has been stopped.")

def get_extracted_data():
    with DATA_LOCK:
        return list(EXTRACTION_DATA)
