import urllib.parse
import requests


class LyricsSearchError(Exception):
    """Raised when lyrics.ovh search fails or returns invalid data."""


def search_by_lyrics(fragment):
    """Search for songs matching a lyrics fragment using lyrics.ovh."""
    url = f"https://api.lyrics.ovh/suggest/{urllib.parse.quote(fragment)}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.exceptions.RequestException, ValueError) as exc:
        raise LyricsSearchError(f"Error fetching suggestions: {exc}") from exc

    results_data = data.get("data")
    if results_data is None:
        if data.get("error"):
            raise LyricsSearchError(data["error"])
        return []

    results = []
    seen = set()
    for item in results_data:
        if not isinstance(item, dict):
            continue
        title = item.get("title", "")
        artist = (item.get("artist") or {}).get("name", "")
        if not title or not artist:
            continue
        
        key = f"{title.lower()} - {artist.lower()}"
        if key not in seen:
            seen.add(key)
            results.append({"title": title, "artist": artist})

    return results
