import requests


class InvalidAPIResponseError(ValueError):
    """Raised when Genius returns data that TrackName cannot parse."""


def search_genius(query, token):
    """Send a search request to the Genius API and return the list of hits."""
    url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    try:
        data = response.json()
    except ValueError as exc:
        raise InvalidAPIResponseError(
            "Genius returned a response that was not valid JSON."
        ) from exc

    if "response" not in data or "hits" not in data.get("response", {}):
        detail = data.get("meta", {}).get("message", "missing response.hits")
        raise InvalidAPIResponseError(f"Unexpected Genius API response: {detail}")

    return data["response"]["hits"]
