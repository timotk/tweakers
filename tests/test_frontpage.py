from unittest import mock
from tests.mocks import mock_get
from tweakers import frontpage


@mock.patch("tweakers.frontpage.get", mock_get)
def test_articles():
    articles = frontpage.articles()
    assert len(articles) > 0


@mock.patch("tweakers.frontpage.get", mock_get)
def test_article_comments():
    article = frontpage.Article(
        url="https://tweakers.net/nieuws/148534/amd-maakt-meer-winst-dankzij-goede-verkopen-van-ryzen-cpus.html"
    )
    assert len(article.comments()) > 0
