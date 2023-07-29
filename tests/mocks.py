from requests_html import HTML, HTMLResponse, HTMLSession


def mock_get(url: str):
    if "/nieuws/" in url:
        case = "article"
    elif "/list_messages/" in url:
        case = "topic"
    elif "/gallery/" in url:
        case = "user"
    elif "/list_activetopics" in url:
        case = "active_topics"
    elif "forum/find" in url:
        case = "find"
    elif url in ("https://tweakers.net/", "https://tweakers.net"):
        case = "frontpage"
    else:
        raise NotImplementedError(f"Url {url} not implemented")

    with open(f"tests/pages/{case}.html") as f:
        response = HTMLResponse(session=HTMLSession)
        response._html = HTML(html=f.read())
    return response
