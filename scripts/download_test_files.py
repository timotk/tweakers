from pathlib import Path
import time
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from tweakers.exceptions import RateLimitException

from tweakers.utils import get

URLS = {
    "topic": "https://gathering.tweakers.net/forum/list_messages/1908208",
    "frontpage": "https://tweakers.net/", 
    "article": "https://tweakers.net/nieuws/212172/whatsapp-introduceert-functie-voor-korte-videoberichten.html",
    "user": "https://tweakers.net/gallery/1/",
    "active_topics": "https://gathering.tweakers.net/forum/list_activetopics",
}

# @retry(
#     retry=retry_if_exception_type(),
#     wait=wait_exponential(multiplier=1, min=5, max=10),
#     stop=stop_after_attempt(3),
# )
# def get(url):
#     # TODO: Implement cookie?
#     response = httpx.get(url)
#     if response.status_code == 429:
#         raise RateLimitException()
    
#     html = response.text
    
#     if "Sorry, je gaat even iets te snel" in html:
#         raise Exception("Rate limited")
    



for name, url in URLS.items():
    print("Downloading", name)
    html = get(url).text
    if "Sorry, je gaat even iets te snel" in html:
        raise Exception("Still rate limited???")
    path = Path(f"tests/pages/{name}.html")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        f.write(html)
    time.sleep(10)

