import datetime
from typing import Any, List, Optional

from pydantic import BaseModel

from tweakers import parsers
from tweakers.comment import Comment
from tweakers.utils import get


class Article(BaseModel):
    url: str
    title: str
    comment_count: int
    published_at: datetime.datetime
    _comments: Optional[List[Comment]] = None
    _html: Optional[Any] = None
    _text: Optional[str] = None

    @property
    def comments(self) -> List[Comment]:
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
