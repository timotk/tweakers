from tweakers import gathering


def test_active_topics():
    assert len(gathering.active_topics()) > 0


def test_search():
    assert len(gathering.search("tweakers")) > 0
