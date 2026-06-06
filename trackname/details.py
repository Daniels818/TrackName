import requests

from trackname.api import InvalidAPIResponseError


def fetch_song_details(song_id, token):
    """Fetch detailed info about a song from the Genius API."""
    url = f"https://api.genius.com/songs/{song_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    try:
        data = response.json()
    except ValueError as exc:
        raise InvalidAPIResponseError(
            "Genius returned a response that was not valid JSON."
        ) from exc

    song = data.get("response", {}).get("song", {})
    album = song.get("album") or {}
    release = song.get("release_date_components") or {}

    return {
        "album_name": album.get("name"),
        "album_year": release.get("year"),
        "annotations": song.get("annotation_count", 0),
        "pageviews": (song.get("stats") or {}).get("pageviews"),
        "featured": [a["name"] for a in (song.get("featured_artists") or [])],
        "description": (song.get("description") or {}).get("plain", ""),
    }


def fetch_lyrics_preview(url):
    """Fetch the first 4 lines of lyrics from a Genius song page."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return ""

    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        containers = soup.select('div[data-lyrics-container="true"]')
        if not containers:
            return ""
        lines = []
        for container in containers:
            text = container.get_text(separator="\n").strip()
            if text:
                lines.extend(text.split("\n"))
        first = [l.strip() for l in lines if l.strip()][:4]
        return "\n".join(first)
    except Exception:
        return ""
