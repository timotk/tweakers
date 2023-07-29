import datetime
from typing import Optional

from pydantic import BaseModel

from tweakers.user import User


class Comment(BaseModel):
    id: int
    user: User
    created: datetime.datetime
    text: Optional[str] = None  # None if comment hidden because of low score
    score: Optional[int] = None
    # TODO: url: str
