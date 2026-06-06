import json
from datetime import datetime, timezone
from pathlib import Path


DATA_DIR = Path.home() / ".trackname"
HISTORY_FILE = DATA_DIR / "history.json"
FAVORITES_FILE = DATA_DIR / "favorites.json"


def _ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(path):
    try:
        data = path.read_text(encoding="utf-8")
        result = json.loads(data) if data.strip() else []
        return result if isinstance(result, list) else []
    except (FileNotFoundError, json.JSONDecodeError, ValueError, OSError):
        return []


def _save_json(path, data):
    try:
        _ensure_data_dir()
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def load_history():
    return _load_json(HISTORY_FILE)


def save_history(entries):
    _save_json(HISTORY_FILE, entries)


def load_favorites():
    return _load_json(FAVORITES_FILE)


def save_favorites(entries):
    _save_json(FAVORITES_FILE, entries)


def extract_song_data(hit):
    """Extract title, artist, year and url from a Genius API hit."""
    result = hit.get("result", {})
    return {
        "title": result.get("title", "Unknown title"),
        "artist": result.get("primary_artist", {}).get("name", "Unknown artist"),
        "year": result.get("release_date_for_display", "Unknown year"),
        "url": result.get("url", ""),
    }


def add_history_entry(query, hits, max_entries=200):
    entries = load_history()
    entry = {
        "query": query,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": [extract_song_data(hit) for hit in hits[:5]],
    }
    entries.append(entry)
    if len(entries) > max_entries:
        entries = entries[-max_entries:]
    save_history(entries)


def add_favorite_entry(song_data):
    entries = load_favorites()
    for existing in entries:
        if song_data.get("url") and existing.get("url") == song_data["url"]:
            return False
        if (existing.get("title") == song_data.get("title")
                and existing.get("artist") == song_data.get("artist")):
            return False
    entries.append(song_data)
    save_favorites(entries)
    return True


def clear_history():
    save_history([])
