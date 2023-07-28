from unittest import mock
from tests.mocks import mock_get
from tweakers import gathering


@mock.patch("tweakers.gathering.get", mock_get)
def test_active_topics():
    assert len(gathering.active_topics()) > 0


@mock.patch("tweakers.gathering.get", mock_get)
def test_search():
    assert len(gathering.search("playstation")) > 0
