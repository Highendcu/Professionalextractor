import threading
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

EXTRACTION_DATA = []
EXTRACTION_ACTIVE = False
DATA_LOCK = threading.Lock()

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

socketio = None  # Placeholder for socketio instance


def set_socketio(sio):
    global socketio
    socketio = sio


def start_extraction(urls, keywords, platforms, country, state):
    global EXTRACTION_ACTIVE
    EXTRACTION_ACTIVE = True

    with DATA_LOCK:
        EXTRACTION_DATA.clear()

    # Normalize inputs
    if isinstance(urls, str):
        urls = [u.strip() for u in urls.split(",") if u.strip()]
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]

    def process():
        total_count = 0
        for platform in platforms:
            if not EXTRACTION_ACTIVE:
                break
            scraper = SCRAPER_MAP.get(platform)
            if scraper:
                try:
                    results = scraper(urls, keywords, country, state)
                    with DATA_LOCK:
                        EXTRACTION_DATA.extend(results)
                        total_count += len(results)

                    if socketio:
                        socketio.emit(
                            "update",
                            {
                                "new_count": len(results),
                                "total_count": total_count
                            },
                            broadcast=True
                        )
                    else:
                        print("[WARN] SocketIO not initialized.")
                except Exception as e:
                    print(f"[ERROR] Scraper failed for {platform}: {e}")
        EXTRACTION_ACTIVE = False

    # Start async task properly
    if socketio:
        socketio.start_background_task(target=process)
    else:
        print("[ERROR] Cannot start background task: socketio is not set.")


def stop_extraction():
    global EXTRACTION_ACTIVE
    EXTRACTION_ACTIVE = False


def get_extracted_data():
    with DATA_LOCK:
        return list(EXTRACTION_DATA)
