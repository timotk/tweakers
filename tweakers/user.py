from typing import Optional

from pydantic import BaseModel, model_validator


class User(BaseModel):
    """A Tweakers.net user"""

    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None

    @model_validator(mode="before")
    def check_name_or_id(cls, values):
        if (values.get("name") is None) and (values.get("id") is None):
            raise ValueError("Either name or id is required")
        return values

    # @property
    # def url(self):
    #     if self.id is not None:
    #         return f"https://tweakers.net/gallery/{self.id}/"
    #     elif self.name is not None:
    #         return f"https://tweakers.net/gallery/{self.name}/"
    #     else:
    #         raise ValueError("Either name or id is required")
