"""
https://tweakers.net frontpage.
"""

from typing import List

from requests_html import HTMLResponse

from . import parsers
from .article import Article
from .utils import get

url = "https://tweakers.net"


def articles() -> List[Article]:
    response: HTMLResponse = get(url)
    articles: List = [Article(**d) for d in parsers.frontpage_articles(response.html)]
    return articles
