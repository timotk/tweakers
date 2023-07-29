import datetime
from typing import Any, Optional

from pydantic import BaseModel

from tweakers import parsers
from tweakers.models import Comment
from tweakers.utils import get


class Article(BaseModel):
    url: str
    title: str
    comment_count: int
    published_at: datetime.datetime
    _comments: Optional[list[Comment]] = None
    _html: Optional[Any] = None
    _text: Optional[str] = None

    @property
    def comments(self) -> list[Comment]:
        # TODO: Add pagination of comments
        if self._comments is None:
            self._comments = [Comment(**d) for d in parsers.article_comments(self.html)]
        return self._comments

    @property
    def html(self):
        if self._html is None:
            response = get(self.url)
            self._html = response.html
        return self._html

    @property
    def text(self) -> str:
        if self._text is None:
            self._text = self.html.find(".articleContent")[0].text
        return self._text
