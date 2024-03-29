import datetime
from unittest import mock

from tests.mocks import mock_get
from tweakers import frontpage
from tweakers.comment import Comment


@mock.patch("tweakers.frontpage.get", mock_get)
def test_articles():
    articles = frontpage.articles()
    assert len(articles) > 0


@mock.patch("tweakers.article.get", mock_get)
def test_article_comments():
    article = frontpage.Article(
        url="https://tweakers.net/nieuws/148534/amd-maakt-meer-winst-dankzij-goede-verkopen-van-ryzen-cpus.html",
        title="AMD maakt meer winst dankzij goede verkopen van Ryzen-cpu's",
        comment_count=10,  # Can be any number here
        published_at=datetime.datetime(2019, 1, 30, 10, 45),
    )
    assert len(article.comments) > 0
    assert all([isinstance(comment, Comment) for comment in article.comments])
