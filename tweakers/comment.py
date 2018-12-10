"""
Tweakers.net comments.
"""

from .user import User


class Comment:
    """
    A comment on a gathering.tweakers.net topic
    """

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if k == "username":
                setattr(self, "user", User(name=v))
            else:
                setattr(self, k, v)
