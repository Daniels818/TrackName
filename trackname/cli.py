import os
import sys

import requests

from trackname.api import InvalidAPIResponseError, search_genius
from trackname.display import display_results
from trackname.text import clean_query


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
        user_input = input("  Search (title / artist / both) - or 'q' to quit: ").strip()
        print()

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

        try:
            hits = search_genius(query, token)
            display_results(hits)

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "?"
            if status == 401:
                print("  Error: Token rejected (401). Double-check GENIUS_ACCESS_TOKEN.")
            else:
                print(f"  HTTP {status} error from Genius API: {e}")

        except requests.exceptions.Timeout:
            print("  Error: Request timed out - check your internet connection and retry.")

        except requests.exceptions.RequestException as e:
            print(f"  Network error: {e}")

        except InvalidAPIResponseError as e:
            print(f"  Invalid response from Genius API: {e}")

        input("  Press Enter to continue...")
        print()
