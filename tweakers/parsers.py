"""
HTML parsers.
"""

from typing import Dict, Generator, Union

from requests_html import HTML
import dateparser


def get_comment_count(html: HTML) -> int:
    comment_count: int
    try:
        comment_count = int(html.find(".commentCount", first=True).text)
    except AttributeError:  # Also count the opening post
        comment_count = 1
    return comment_count


def active_topics(html: HTML) -> Generator[dict, None, None]:
    for tr in html.find(".listing tr")[1:]:
        topic: Dict = {
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
        topic: Dict = {
            "title": tr.find(".title a", first=True).text,
            "url": tr.find(".title a", first=True).attrs["href"],
            "last_reply": dateparser.parse(
                tr.find(".time a", first=True).text, languages=["nl"]
            ),
        }
        yield topic


def bookmark_topics(html: HTML) -> Generator[dict, None, None]:
    for tr in html.find(".listing tr.alt")[1:]:
        topic: Dict = {
            "title": tr.find(".topic a")[1].text,
            "url": tr.find(".topic a")[1].attrs["href"],
            "last_reply": dateparser.parse(
                tr.find(".time a", first=True).text, languages=["nl"]
            ),
        }
        yield topic


def get_rating(div):
    rating: int
    try:
        rating = int(div.find("span.ratingcount", first=True).text.replace("+", ""))
    except AttributeError:  # post too old for rating
        rating = 0
    return rating


def topic_comments(html: Union[HTML, str]) -> Generator[dict, None, None]:
    if isinstance(html, str):
        html = HTML(html=html)

    for div in html.find(".message"):
        message: Dict = {
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


def frontpage_articles(html: HTML) -> Generator[dict, None, None]:
    for tr in html.find("tr.headline.news"):
        topic: Dict = {
            "title": tr.find(".title a", first=True).text,
            "url": tr.find(".title a", first=True).attrs["href"],
            "comment_count": get_comment_count(tr),
            "publication_time": tr.find(".publicationTime", first=True).text,
        }
        yield topic


def article_comments(html: HTML) -> Generator[dict, None, None]:
    for div in html.find("div.reactieBody"):
        comment: Dict = {
            "username": _get_text(div, selector=".userLink"),
            "date": dateparser.parse(
                _get_text(div, selector="a.date"), languages=["nl"]
            ),
            "text": _get_text(div, selector=".reactieContent"),
            "score": int(_get_text(div, selector="a.scoreButton")),
        }
        yield comment


def _get_text(html: HTML, selector: str) -> Union[str, None]:
    try:
        return html.find(selector, first=True).text
    except AttributeError:
        return
