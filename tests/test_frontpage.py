from tweakers import frontpage


def test_articles():
    articles = frontpage.articles()
    assert len(articles) > 0


def test_article_comments():
    article = frontpage.Article(
        url="https://tweakers.net/nieuws/148534/amd-maakt-meer-winst-dankzij-goede-verkopen-van-ryzen-cpus.html"
    )
    assert len(article.comments()) > 0
