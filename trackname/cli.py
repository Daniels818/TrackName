import os
import sys
from datetime import datetime

import requests

from trackname.api import InvalidAPIResponseError, search_genius
from trackname.display import display_results
from trackname.text import clean_query
from trackname import storage


def print_missing_token_help():
    print("ERROR: The GENIUS_ACCESS_TOKEN environment variable is not set.")
    print()
    print("Here's how to fix that:")
    print("  1. Sign up at https://genius.com/api-clients")
    print("  2. Create an app and copy the 'Client Access Token'")
    print("  3. Set it as an environment variable:")
    print("     Linux / macOS : export GENIUS_ACCESS_TOKEN='your_token_here'")
    print("     Windows CMD   : setx GENIUS_ACCESS_TOKEN \"your_token_here\"")


def print_banner():
    print("=" * 55)
    print("  TrackName - Song search by title or artist")
    print("=" * 55)
    print()
    print("  Tips:")
    print("    - Search by song title     ->  Bohemian Rhapsody")
    print("    - Search by artist name    ->  Queen")
    print("    - Combine both             ->  Queen Bohemian Rhapsody")
    print("    - Special commands:")
    print("      :history      Show last 10 searches")
    print("      :favorites    List all saved favorites")
    print("      :clear        Clear search history")
    print()


def show_history():
    entries = storage.load_history()
    if not entries:
        print("  No searches yet.")
        return
    print(f"  History ({len(entries)} total):")
    print()
    for entry in entries[-10:]:
        ts = entry.get("timestamp", "")
        try:
            dt = datetime.fromisoformat(ts)
            ts = dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            pass
        query = entry.get("query", "?")
        print(f"  {ts}  {query}")
    print()


def show_favorites():
    entries = storage.load_favorites()
    if not entries:
        print("  No favorites saved yet.")
        return
    print(f"  Favorites ({len(entries)}):")
    print()
    for i, entry in enumerate(entries, 1):
        title = entry.get("title", "Unknown title")
        artist = entry.get("artist", "Unknown artist")
        year = entry.get("year", "")
        url = entry.get("url", "")
        print(f"  {i}. {title} - {artist} ({year})")
        if url:
            print(f"     {url}")
    print()


def handle_clear():
    entries = storage.load_history()
    if not entries:
        print("  History is already empty.")
        return
    confirm = input("  Delete all history? (y/N): ").strip().lower()
    if confirm == "y":
        storage.clear_history()
        print("  History cleared.")
    else:
        print("  Canceled.")
    print()


def search_and_display(user_input, query, token):
    try:
        hits = search_genius(query, token)
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "?"
        if status == 401:
            print("  Error: Token rejected (401). Double-check GENIUS_ACCESS_TOKEN.")
        else:
            print(f"  HTTP {status} error from Genius API: {e}")
        return

    except requests.exceptions.Timeout:
        print("  Error: Request timed out - check your internet connection and retry.")
        return

    except requests.exceptions.RequestException as e:
        print(f"  Network error: {e}")
        return

    except InvalidAPIResponseError as e:
        print(f"  Invalid response from Genius API: {e}")
        return

    display_results(hits)

    if not hits:
        return

    storage.add_history_entry(user_input, hits)

    fav = input("  \u00bfGuardar alg\u00fan favorito? (n\u00famero o Enter para omitir): ").strip()
    if fav.isdigit():
        idx = int(fav) - 1
        top = hits[:5]
        if 0 <= idx < len(top):
            song_data = storage.extract_song_data(top[idx])
            added = storage.add_favorite_entry(song_data)
            if added:
                print("  \u00a1Guardado en favoritos!")
            else:
                print("  Ya est\u00e1 en favoritos.")
        else:
            print("  Invalid number.")
        print()


def main():
    """Set up the Genius token, then loop accepting title/artist queries."""
    token = os.environ.get("GENIUS_ACCESS_TOKEN")
    if not token:
        print_missing_token_help()
        input("\n  Press Enter to exit...")
        sys.exit(1)

    print_banner()

    while True:
        user_input = input("  Search - or type :history, :favorites, :clear, or 'q' to quit: ").strip()
        print()

        if user_input == ":history":
            show_history()
            continue

        if user_input == ":favorites":
            show_favorites()
            continue

        if user_input == ":clear":
            handle_clear()
            continue

        if user_input.lower() in ("q", "quit", "exit"):
            print("  Goodbye!")
            break

        if not user_input:
            print("  You didn't type anything - please enter a title or artist name.")
            print()
            continue

        query = clean_query(user_input)

        if not query:
            print("  That doesn't look like a valid search - try a song title or artist name.")
            print()
            continue

        search_and_display(user_input, query, token)

        input("  Press Enter to continue...")
        print()
