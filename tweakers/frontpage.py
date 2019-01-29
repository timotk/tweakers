"""
https://tweakers.net frontpage.
"""

from typing import List

from requests_html import HTMLResponse
from .utils import fetch
from .topic import Topic
from . import parsers


url = "https://tweakers.net"


class Article:
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)


def articles() -> List["Articles"]:
    response: HTMLResponse = fetch(url)
    articles: List = [Article(**d) for d in parsers.frontpage_articles(response.html)]
    return articles


def active_topics() -> List[Topic]:
    response: HTMLResponse = fetch(url=f"{url}/forum/list_activetopics")
    topics: List = [Topic(**d) for d in parsers.active_topics(response.html)]
    return topics
