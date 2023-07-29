"""
Utilities.
"""
from requests import Response
from requests_html import HTMLResponse, HTMLSession
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from tweakers.exceptions import (
    CaptchaRequiredException,
    InvalidCredentialsException,
    RateLimitException,
)

session = HTMLSession()
session.headers.update({"X-Cookies-Accepted": "1"})  # Bypass the cookiewall


@retry(
    retry=retry_if_exception_type(),
    wait=wait_exponential(multiplier=1, min=5, max=10),
    stop=stop_after_attempt(3),
)
def get(url: str) -> HTMLResponse:
    response = session.get(url)
    if response.status_code == 429:
        raise RateLimitException()
    if not 200 <= response.status_code < 300:
        raise Exception(f"Url {url} returned a {response.status_code}")
    return response


def id_from_url(url: str) -> int:
    """
    Parse the id from the URL

    :param url: url to get id from.
    :raises NotImplementedError: If getting id from this url is not supported.
    :return: integer id.
    """
    parts = url.split("/")
    if "aanbod" in parts:
        id = parts[parts.index("aanbod") + 1]
    elif "list_messages" in parts:
        id = parts[parts.index("list_messages") + 1]
    elif "pricewatch" in parts:
        id = parts[parts.index("pricewatch") + 1]
    else:
        raise NotImplementedError(
            "Getting the id for url ({url}) is not yet implemented"
        )
    return int(id)


def login(username: str, password: str) -> None:  # pragma: no cover
    url = "https://tweakers.net/my.tnet/login/"
    response = session.get(url)
    try:
        token = response.html.find("input[name=tweakers_login_form\[_token\]]")[
            0
        ].attrs["value"]
    except IndexError:  # Already logged in
        return

    data = {
        "tweakers_login_form[_token]": token,
        "tweakers_login_form[user]": username,
        "tweakers_login_form[password]": password,
    }
    login_response = session.post(url=url, data=data)

    _raise_for_invalid_credentials(login_response)
    _raise_for_captcha_error(login_response)


def _raise_for_invalid_credentials(login_response: Response) -> None:
    login_error_text = (
        "De combinatie van gebruikersnaam of e-mailadres en wachtwoord is onjuist."
    )
    if login_error_text in login_response.text:
        raise InvalidCredentialsException


def _raise_for_captcha_error(login_response: Response) -> None:
    captcha_error_text = (
        "Om te bewijzen dat je geen robot bent, moet een captcha worden ingevuld."
    )
    if captcha_error_text in login_response.text:
        raise CaptchaRequiredException
