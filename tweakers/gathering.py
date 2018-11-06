"""
gathering.tweakers.net
"""
from typing import List

from requests_html import HTMLResponse
from .utils import fetch
from .topic import Topic
from . import parsers


url = "https://gathering.tweakers.net"


def active_topics() -> List[Topic]:
    response: HTMLResponse = fetch(url=f"{url}/forum/list_activetopics")
    topics: List = [Topic(**d) for d in parsers.active_topics(response.html)]
    return topics


def search(query: str) -> List[Topic]:
    """Search for topics given a query.
    :param query: Search query.
    """
    response: HTMLResponse = fetch(url=f"{url}/forum/find?keyword={query}")
    topics: List = [Topic(**d) for d in parsers.search_topics(response.html)]
    return topics
