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

    song = (data.get("response") or {}).get("song") or {}
    album = song.get("album") or {}
    release = song.get("release_date_components") or {}

    return {
        "album_name": album.get("name"),
        "album_year": release.get("year"),
        "annotations": song.get("annotation_count", 0),
        "pageviews": (song.get("stats") or {}).get("pageviews"),
        "featured": [a.get("name") for a in (song.get("featured_artists") or []) if a.get("name")],
        "description": (song.get("description") or {}).get("plain", ""),
    }


def fetch_lyrics(artist, title):
    """Fetch lyrics from lyrics.ovh API using artist and title."""
    import urllib.parse
    artist_enc = urllib.parse.quote(artist)
    title_enc = urllib.parse.quote(title)
    url = f"https://api.lyrics.ovh/v1/{artist_enc}/{title_enc}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("lyrics", "")
    except Exception:
        return ""


def fetch_lyrics_preview(artist, title):
    """Fetch the first 8 lines of lyrics using the lyrics.ovh API."""
    lyrics = fetch_lyrics(artist, title)
    if not lyrics:
        return ""
    lines = [line.strip() for line in lyrics.splitlines() if line.strip()]
    return "\n".join(lines[:8])
