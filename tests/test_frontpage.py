from tweakers import frontpage


def test_articles():
    articles = frontpage.articles()
    assert len(articles) > 0
