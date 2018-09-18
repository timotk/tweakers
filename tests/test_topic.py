from unittest import mock

from tweakers.topic import Topic
from tweakers.comment import Comment


def test_topic():
    topic = Topic(url="https://gathering.tweakers.net/forum/list_messages/812397")
    assert topic


def test_topic_comments():
    topic = Topic(url="https://gathering.tweakers.net/forum/list_messages/812397")
    assert len(topic.comments(page=1)) > 0


def mock_get_new_comments(*args, **kwargs):
    return [
        Comment(id=1, text="test1"),
        Comment(id=2, text="test2"),
        Comment(id=3, text="test3"),
    ]


@mock.patch("tweakers.topic.Topic.get_new_comments", mock_get_new_comments)
def test_topic_comments_stream():
    topic = Topic(url="https://gathering.tweakers.net/forum/list_messages/812397")
    comment_generator = topic.comment_stream()
    count = 0
    comments = []
    for c in comment_generator:
        count += 1
        comments.append(c)
        if count == 3:
            break
    assert len(comments) == 3
