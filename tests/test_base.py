import pytest
from tweakers import utils


def test__require_cookies():
    assert len(utils.session.cookies) == 0
    utils._require_cookies()
    assert len(utils.session.cookies) == 3


def test_fetch():
    response = utils.fetch(url="https://tweakers.net")
    assert "Nieuws van vandaag" in response.html.text
    assert "Cookies op Tweakers" not in response.html.text


def test_fetch_exception():
    with pytest.raises(Exception):
        utils.fetch(url="https://tweakers.net/a/")


def test_id_from_url():
    urls_ids = {
        "https://gathering.tweakers.net/forum/list_messages/812397": 812397,
        "https://tweakers.net/aanbod/1/deur-lian-li-pc-60-zonder-window.html": 1,
        "https://tweakers.net/pricewatch/1118063/samsung-galaxy-s9-dual-sim-64gb-zwart.html": 1118063,
    }
    for url, id in urls_ids.items():
        assert utils.id_from_url(url) == id


def test_id_from_url_exception():
    url = "https://tweakers.net/nieuws/1/aol-netscape-en-open-source.html"

    with pytest.raises(NotImplementedError):
        assert utils.id_from_url(url) == 1
