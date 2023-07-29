from unittest import mock

import pytest

from tests.mocks import mock_get
from tweakers.comment import Comment
from tweakers.topic import Topic
from tweakers.user import User


@pytest.fixture
def topic():
    return Topic(url="https://gathering.tweakers.net/forum/list_messages/1908208")


def test_topic(topic):
    assert topic


@mock.patch("tweakers.topic.get", mock_get)
def test_topic_comments(topic):
    assert len(topic.comments(page=1)) > 0


def mock_get_new_comments(*args, **kwargs):
    return [
        Comment(id=1, text="test1", user=User(id=1)),
        Comment(id=2, text="test2", user=User(id=1)),
        Comment(id=3, text="test3", user=User(id=2)),
    ]


@mock.patch("tweakers.topic.Topic.get_new_comments", mock_get_new_comments)
def test_topic_comments_stream(topic):
    comment_generator = topic.comment_stream()
    count = 0
    comments = []
    for comment in comment_generator:
        count += 1
        comments.append(comment)
        if count == 3:
            break
    assert len(comments) == 3
    for comment in comments:
        assert comment
