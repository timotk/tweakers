"""
A tweakers.net user.
"""


class User:
    """A Tweakers.net user"""

    def __init__(self, **kwargs) -> None:
        required = ["id", "name"]
        assert any(
            x in required for x in kwargs
        ), f"Missing one of required keywords: {required}"

        for k, v in kwargs.items():
            if k == "id":
                k = "_id"
            setattr(self, k, v)
