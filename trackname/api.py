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

    response_data = data.get("response")
    if not isinstance(response_data, dict) or "hits" not in response_data:
        detail = (data.get("meta") or {}).get("message", "missing response.hits")
        raise InvalidAPIResponseError(f"Unexpected Genius API response: {detail}")

    return response_data["hits"]
