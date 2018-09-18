"""
Session handler
"""
from requests_html import HTMLSession, HTMLResponse


session = HTMLSession()


def fetch(url: str) -> HTMLResponse:
    """
    :param url: Url to fetch.
    :return: HTMLResponse.
    """
    _require_cookies()

    response = session.get(url)
    if not 200 >= response.status_code < 300:
        raise Exception(f"Url {url} returned a {response.status_code}")
    return response


def _require_cookies():
    """
    Get cookies if not already accepted
    """
    if len(session.cookies) > 2:
        return

    url = "https://tweakers.net"
    response = session.get(url)
    token = response.html.find("input[name=tweakers_token]")[0].attrs["value"]
    data = {"decision": "accept", "tweakers_token": token}
    session.post(url="https://tweakers.net/my.tnet/cookies", data=data)


def id_from_url(url):
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
