"""
Utilities.
"""
from .rate_limit import rate_limit
from requests_html import HTMLSession, HTMLResponse

session = HTMLSession()


def get(url: str) -> HTMLResponse:
    response = session.get(url)
    if response.status_code == 429:
        raise Exception(
            "Error [HTTP 429]: Too Many Requests. This is a rate limit problem."
        )
    if not 200 <= response.status_code < 300:
        raise Exception(f"Url {url} returned a {response.status_code}")
    return response


@rate_limit
def fetch(url: str) -> HTMLResponse:
    """
    :param url: Url to fetch.
    :return: HTMLResponse.
    """
    _require_cookies()

    response = get(url)
    return response


def _require_cookies() -> None:
    """
    Get cookies if not already accepted
    """
    if len(session.cookies) > 2:
        return

    url = "https://tweakers.net"
    response = get(url)
    token = response.html.find("input[name=tweakers_token]")[0].attrs["value"]
    data = {"decision": "accept", "tweakers_token": token}
    session.post(url="https://tweakers.net/my.tnet/cookies", data=data)


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

    login_error_text = (
        "De combinatie van gebruikersnaam of e-mailadres en wachtwoord is onjuist."
    )
    if login_error_text in login_response.text:
        raise ValueError("Invalid username or password.")

    captcha_error_text = (
        "Om te bewijzen dat je geen robot bent, moet een captcha worden ingevuld."
    )
    if captcha_error_text in login_response.text:
        raise Exception("Captcha warning triggered, unable to login!")
