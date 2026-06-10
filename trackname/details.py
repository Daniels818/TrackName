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
    """Fetch lyrics from lyrics.ovh API using artist and title.
    Tries the exact match first, then attempts cleaned versions of the query.
    """
    import urllib.parse
    import re

    def _request(a, t):
        a_enc = urllib.parse.quote(a)
        t_enc = urllib.parse.quote(t)
        url = f"https://api.lyrics.ovh/v1/{a_enc}/{t_enc}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json().get("lyrics", "")

    # 1. Try exact match
    try:
        return _request(artist, title)
    except Exception:
        pass

    # 2. Try cleaned versions
    # Clean title: remove parentheses/brackets
    clean_title = re.sub(r'\(.*?\)|\[.*?\]', '', title).strip()
    # Clean artist: remove "feat.", "ft.", etc.
    clean_artist = re.split(r'\s*(?:feat\.?|ft\.?|featuring|&|/|,|;)\s*', artist, flags=re.IGNORECASE)[0].strip()

    if clean_title != title or clean_artist != artist:
        try:
            return _request(clean_artist, clean_title)
        except Exception:
            pass

    return ""


def fetch_lyrics_preview(artist, title):
    """Fetch the first 8 lines of lyrics using the lyrics.ovh API."""
    lyrics = fetch_lyrics(artist, title)
    if not lyrics:
        return ""
    lines = [line.strip() for line in lyrics.splitlines() if line.strip()]
    return "\n".join(lines[:8])
