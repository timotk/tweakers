from pathlib import Path

from tweakers.utils import get

URLS = {
    "topic": "https://gathering.tweakers.net/forum/list_messages/1908208",
    "frontpage": "https://tweakers.net/",
    "article": "https://tweakers.net/nieuws/212172/whatsapp-introduceert-functie-voor-korte-videoberichten.html",
    "user": "https://tweakers.net/gallery/1/",
    "active_topics": "https://gathering.tweakers.net/forum/list_activetopics",
    "find": "https://tweakers.net/forum/find?keyword=playstation",
}


for name, url in URLS.items():
    print("Downloading", name)
    html = get(url).text
    if "Sorry, je gaat even iets te snel" in html:
        raise Exception("Still rate limited???")
    path = Path(f"tests/pages/{name}.html")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        f.write(html)
