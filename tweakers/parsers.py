"""
HTML parsers.
"""

from datetime import date, datetime, timedelta
from typing import Dict, Generator, Union

import dateparser
from requests_html import HTML

from tweakers.user import User


def get_article_comment_count(html: HTML) -> int:
    comment_count: int
    try:
        comment_count = int(html.find(".comment-counter", first=True).text)
    except AttributeError:
        comment_count = 0
    return comment_count


def get_topic_comment_count(html: HTML) -> int:
    comment_count: int
    try:
        comment_count = int(html.find(".commentCount", first=True).text)
    except AttributeError:  # Also count the opening post
        comment_count = 1
    return comment_count


def active_topics(html: HTML) -> Generator[dict, None, None]:
    for tr in html.find(".listing tr")[1:]:
        poster_elem = tr.find(".poster", first=True)
        span = poster_elem.find("span", first=True)
        if span is not None and "multiauthor" in span.attrs["class"]:
            author = [
                User(name=name.strip()) for name in span.attrs["title"].split(",")
            ]
        else:
            username = poster_elem.find("a", first=True).text
            user_url = tr.find(".poster a", first=True).attrs["href"]
            user_id = user_url.split("/")[-1]
            author = User(id=user_id, name=username, url=user_url)

        topic: Dict = {
            "title": tr.find(".topic a", first=True).text,
            "url": tr.find(".topic a", first=True).attrs["href"],
            "author": author,
            "last_reply": dateparser.parse(
                tr.find(".time a", first=True).text, languages=["nl"]
            ),
            "comment_count": get_topic_comment_count(tr),
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
        id = div.attrs["data-message-id"]
        user_id = div.attrs["data-owner-id"]
        username = div.find("a.user", first=True).text
        user_url = div.find("a.user", first=True).attrs["href"]
        user = User(id=user_id, name=username, url=user_url)
        _epoch_time = div.find(".date span", first=True).attrs["data-timestamp"]
        _epoch_time = int(_epoch_time)
        timestamp = datetime.fromtimestamp(_epoch_time)
        url = div.find(".date a", first=True).attrs["href"]

        text = div.find(".messagecontent", first=True).text
        score = get_rating(div)
        comment: Dict = {
            "id": id,
            "user": user,
            "created": timestamp,
            "text": text,
            "url": url,
            "score": score,
        }
        yield comment


def frontpage_articles(html: HTML) -> Generator[dict, None, None]:
    for i, day in enumerate(
        [html.find(".headlines-head"), *html.find(".headline--day")]
    ):
        article_date = date.today() - timedelta(days=i)
        for elem in html.find(".headlineItem.news"):
            time_text = elem.find(".headline--time", first=True).text
            time = datetime.strptime(time_text, "%H:%M").time()
            timestamp = datetime.combine(article_date, time)

            topic: Dict = {
                "title": elem.find(".headline--anchor", first=True).text,
                "url": elem.find("a.headline--anchor", first=True).attrs["href"],
                "comment_count": get_article_comment_count(elem),
                "published_at": timestamp,
            }
            yield topic


def article_comments(html: HTML) -> Generator[dict, None, None]:
    for elem in html.find("twk-reaction"):
        comment_id = elem.attrs["data-reaction-id"]

        user_id = elem.attrs["data-owner-id"]
        _user_a = elem.find(".userLink", first=True)

        try:
            user_url = _user_a.attrs["href"]
            username = _user_a.text
            user = User(id=user_id, name=username, url=user_url)
        except KeyError:  # User is deleted
            username = _user_a.text
            user = User(id=user_id, name=username, url=None)

        _date = elem.find(".date", first=True)
        created = dateparser.parse(_date.text, languages=["nl"])

        try:
            text = elem.find(".reactieContent", first=True).text
        except AttributeError:  # Reaction is hidden
            text = None

        try:
            score = elem.find(".moderation-button", first=True).attrs["score"]
        except KeyError:
            score = None

        comment = {
            "id": comment_id,
            "user": user,
            "created": created,
            "text": text,
            "score": score,
        }
        yield comment


def _get_text(html: HTML, selector: str) -> Union[str, None]:
    try:
        return html.find(selector, first=True).text
    except AttributeError:
        return
