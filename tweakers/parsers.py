from typing import Generator, Union

from requests_html import HTML
import dateparser


def get_comment_count(html: HTML) -> int:
    try:
        return int(html.find(".commentCount", first=True).text)
    except AttributeError:  # Also count the opening post
        return 1


def active_topics(html: HTML) -> Generator[dict, None, None]:
    for tr in html.find(".listing tr")[1:]:
        topic = {
            "title": tr.find(".topic a", first=True).text,
            "url": tr.find(".topic a", first=True).attrs["href"],
            "poster": tr.find(".poster", first=True).text,
            "last_reply": dateparser.parse(
                tr.find(".time a", first=True).text, languages=["nl"]
            ),
            "comment_count": get_comment_count(tr),
        }
        yield topic


def search_topics(html: HTML) -> Generator[dict, None, None]:
    for tr in html.find(".forumlisting tr")[2::2]:
        topic = {
            "title": tr.find(".title a", first=True).text,
            "url": tr.find(".title a", first=True).attrs["href"],
            "last_reply": dateparser.parse(
                tr.find(".time a", first=True).text, languages=["nl"]
            ),
        }
        yield topic


def get_rating(div):
    try:
        return int(div.find("span.ratingcount", first=True).text.replace("+", ""))
    except AttributeError:  # post too old for rating
        return 0


def topic_comments(html: Union[HTML, str]) -> Generator[dict, None, None]:
    if isinstance(html, str):
        html = HTML(html=html)

    for div in html.find(".message"):
        message = {
            "id": int(div.attrs["data-message-id"]),
            "username": div.find("a.user", first=True).text,
            "date": dateparser.parse(
                div.find("div.date", first=True).text, languages=["nl"]
            ),
            "url": div.find(".date p a", first=True).attrs["href"],
            "rating": get_rating(div),
            "text": div.find(".messagecontent", first=True).text,
            "html": div.html,
        }
        yield message
