from unittest import mock

import pytest

from tweakers import utils
from tweakers.exceptions import CaptchaRequiredException, InvalidCredentialsException


def test_get():
    response = utils.get(url="https://tweakers.net")
    assert "Laatste nieuws" in response.html.text
    assert "Cookies op Tweakers" not in response.html.text


def test_get_exception():
    with pytest.raises(Exception):
        utils.get(url="https://tweakers.net/a/")


@pytest.mark.parametrize(
    "url,item_id",
    [
        ("https://gathering.tweakers.net/forum/list_messages/1908208", 1908208),
        ("https://tweakers.net/aanbod/1/deur-lian-li-pc-60-zonder-window.html", 1),
        (
            "https://tweakers.net/pricewatch/1118063/samsung-galaxy-s9-dual-sim-64gb-zwart.html",
            1118063,
        ),
    ],
)
def test_id_from_url(url, item_id):
    assert utils.id_from_url(url) == item_id


def test_id_from_url_exception():
    url = "https://tweakers.net/nieuws/1/aol-netscape-en-open-source.html"

    with pytest.raises(NotImplementedError):
        assert utils.id_from_url(url) == 1


def test__raise_for_invalid_credentials():
    response = mock.Mock()
    response.text = (
        "De combinatie van gebruikersnaam of e-mailadres en wachtwoord is onjuist."
    )
    with pytest.raises(InvalidCredentialsException):
        utils._raise_for_invalid_credentials(response)


def test__raise_for_captcha_error():
    response = mock.Mock()
    response.text = (
        "Om te bewijzen dat je geen robot bent, moet een captcha worden ingevuld."
    )
    with pytest.raises(CaptchaRequiredException):
        utils._raise_for_captcha_error(response)
