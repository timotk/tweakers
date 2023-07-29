"""
gathering.tweakers.net (forums).
"""

from typing import List

from requests_html import HTMLResponse

from . import parsers
from .topic import Topic
from .utils import get

url = "https://gathering.tweakers.net"


def active_topics() -> List[Topic]:
    response: HTMLResponse = get(url=f"{url}/forum/list_activetopics")
    topics: List = [Topic(**d) for d in parsers.active_topics(response.html)]
    return topics


def search(query: str) -> List[Topic]:
    """Search for topics given a query.
    :param query: Search query.
    """
    response: HTMLResponse = get(url=f"{url}/forum/find?keyword={query}")
    topics: List = [Topic(**d) for d in parsers.search_topics(response.html)]
    return topics


def bookmarks() -> List[Topic]:
    """Get a list of bookmarks

    :return: Bookmarks
    """
    response: HTMLResponse = get(url=f"{url}/forum/list_bookmarks")
    topics: List = [Topic(**d) for d in parsers.bookmark_topics(response.html)]
    return topics
