"""
gathering.tweakers.net
"""
from typing import List

from .utils import fetch
from .topic import Topic
from . import parsers


url = "https://gathering.tweakers.net"


def active_topics() -> List[Topic]:
    response = fetch(url=f"{url}/forum/list_activetopics")
    return [Topic(**d) for d in parsers.active_topics(response.html)]


def search(query: str) -> List[Topic]:
    """Search for topics given a query.
    :param query: Search query.
    """
    response = fetch(url=f"{url}/forum/find?keyword={query}")
    return [Topic(**d) for d in parsers.search_topics(response.html)]
