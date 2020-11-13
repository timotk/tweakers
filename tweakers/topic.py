"""
gathering.tweakers.net topics
"""

import time

from typing import Union, List, Generator

from requests_html import HTMLResponse

from .utils import id_from_url, get
from .comment import Comment
from . import parsers


class Topic:
    """
    A topic on gathering.tweakers.net
    """

    def __init__(self, url, **kwargs) -> None:
        self.__dict__.update(kwargs)
        self.url: str = url
        self.id: int = id_from_url(self.url)

    def comments(self, page: Union[int, str]) -> List[Comment]:
        """
        Get comments for a specific Topic page

        :param page: Page number (zero indexed) or 'last' for last page.
        :return: A list of Comment objects.
        """
        response: HTMLResponse = get(url=f"{self.url}/{page}")
        return [Comment(**d) for d in parsers.topic_comments(response.html)]

    def comment_stream(
        self, refresh: int = 15, last: int = 3
    ) -> Generator[Comment, None, None]:
        """
        Generator of new comments.

        :param refresh: Refresh timer in seconds (default 15).
        :param last: Number of already posted comments to return (default 15).
        :return: A generator of Comment objects.
        """

        # get the last posted comment id, required for getting new comments
        comments: List = self.comments("last")
        last_message_id: int = comments[-1].id

        # yield last n comments
        for comment in comments[-last:]:
            yield comment

        timer: int = refresh
        while True:
            epoch_time: int = int(time.time())  # required for getting new comments
            ajax_url: str = f"https://gathering.tweakers.net/ajax/list_new_messages/{self.id}/{last_message_id}?output=json\
                    &nocache={epoch_time}"
            comments = self.get_new_comments(ajax_url)

            if comments:
                last_message_id = comments[-1].id
            for comment in comments:
                yield comment

            # decrease timer each second
            while timer > 0:  # pragma: no cover
                time.sleep(1)
                timer -= 1
            else:  # pragma: no cover
                timer = refresh

    def get_new_comments(self, ajax_url: str) -> List[Comment]:  # pragma: no cover
        """
        Get new comments for a given ajax_url

        :param ajax_url: Ajax url to query for new comments.
        :return: A list of comment objects.
        """
        json = get(ajax_url).json()

        new_comments: List
        try:
            html: str = "".join(json["data"]["messages"])
            new_comments = [Comment(**d) for d in parsers.topic_comments(html)]
        except KeyError:  # no new messages
            new_comments = []
        return new_comments
