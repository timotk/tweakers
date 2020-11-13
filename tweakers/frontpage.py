"""
https://tweakers.net frontpage.
"""

from typing import List

from requests_html import HTMLResponse
from .utils import get
from .topic import Topic
from .comment import Comment
from . import parsers


url = "https://tweakers.net"


class Article:
    def __init__(self, url, **kwargs):
        self.url = url
        self.__dict__.update(kwargs)

    def comments(self):
        """Get comments for a frontpage article.

        :return: A list of Comment objects.
        """
        # TODO: ADD PAGINATION OF COMMENTS
        response: HTMLResponse = get(url=f"{self.url}")
        return [Comment(**d) for d in parsers.article_comments(response.html)]


def articles() -> List["Articles"]:
    response: HTMLResponse = get(url)
    articles: List = [Article(**d) for d in parsers.frontpage_articles(response.html)]
    return articles


def active_topics() -> List[Topic]:
    response: HTMLResponse = get(url=f"{url}/forum/list_activetopics")
    topics: List = [Topic(**d) for d in parsers.active_topics(response.html)]
    return topics
