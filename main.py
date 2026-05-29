# =============================================================================
# SMART LYRICS — Song search engine (by title or artist)
# Phase 4: Switched from lyric-fragment search to title/artist search.
#
# Background:
#   The Genius API /search endpoint does NOT index song lyrics — it only
#   matches against song titles, artist names, and album metadata. Searching
#   by lyric fragment therefore gave poor or random results. This version
#   reframes the UX: the user types a song title, an artist name, or both,
#   and the engine returns the top matches from Genius.
#
# How it works:
#   1. The user types a title, an artist, or "title - artist" style query.
#   2. We clean it up (lowercase, strip noisy punctuation).
#   3. We hit the Genius /search endpoint and display the top 5 results.
# =============================================================================

import os
import re
import sys

import requests


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def clean_query(text):
    """Normalize the user's search query before sending it to the Genius API.

    We lowercase the input and strip punctuation that adds noise without
    helping the search. Apostrophes and hyphens are kept intentionally:
      - apostrophes preserve contractions like "don't" → "don't" (not "dont")
      - hyphens are common in artist names like "Twenty One Pilots"
    Parentheses and brackets are removed because they often wrap metadata
    like "(Official Video)" or "[Remix]" that confuses the ranking.
    """
    text = text.lower()
    # Remove common punctuation that does not improve search quality
    text = re.sub(r'[.,;:!?"()\\[\\]{}]', "", text)
    # Collapse multiple spaces into one (can happen after stripping chars)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Genius API
# ---------------------------------------------------------------------------

def search_genius(query, token):
    """Send a search request to the Genius API and return the list of hits.

    The /search endpoint matches against song titles, artist names, and album
    metadata — NOT against lyrics. This makes it well-suited for title/artist
    lookups but unsuitable for lyric-fragment searches.

    Args:
        query: The cleaned search string (title, artist, or both).
        token: A valid Genius Client Access Token.

    Returns:
        A list of hit objects from the API response.

    Raises:
        requests.exceptions.HTTPError: If the API returns a non-2xx status.
        requests.exceptions.Timeout:   If the server doesn't respond in time.
        requests.exceptions.RequestException: For any other network problem.
        ValueError: If the JSON response doesn't have the expected structure.
    """
    url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query}

    # 10-second timeout so we don't hang on a slow connection
    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    # Guard against unexpected response shapes before drilling into the dict
    if "response" not in data or "hits" not in data.get("response", {}):
        raise ValueError(
            f"Unexpected API response: {data.get('meta', {}).get('message', 'no details')}"
        )

    return data["response"]["hits"]


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def display_results(hits):
    """Print the top results to the console in a clean, readable format.

    Shows at most 5 results. If the API returns nothing we let the user know
    immediately instead of just printing a blank screen.

    Args:
        hits: The list of hit objects returned by search_genius().
    """
    if not hits:
        print("  No songs found. Try a different title or artist name.")
        return

    for i, hit in enumerate(hits[:5], 1):
        # Each hit should contain a "result" key; skip malformed entries
        result = hit.get("result")
        if not result:
            continue

        title  = result.get("title", "Unknown title")
        # primary_artist can be missing in edge cases — fall back safely
        artist = result.get("primary_artist", {}).get("name", "Unknown artist")
        date   = result.get("release_date_for_display", "Unknown date")
        url    = result.get("url", "")

        print(f"  {i}. {title} — {artist} ({date})")
        if url:
            # Link to the full song page on Genius (includes lyrics)
            print(f"     {url}")
        print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    """Set up the Genius token, then loop accepting title/artist queries."""
    # We read the token from an environment variable to keep secrets out of
    # the source code. Never hard-code API tokens in version-controlled files.
    token = os.environ.get("GENIUS_ACCESS_TOKEN")
    if not token:
        print("ERROR: The GENIUS_ACCESS_TOKEN environment variable is not set.")
        print()
        print("Here's how to fix that:")
        print("  1. Sign up at https://genius.com/api-clients")
        print("  2. Create an app and copy the 'Client Access Token'")
        print("  3. Set it as an environment variable:")
        print("     Linux / macOS : export GENIUS_ACCESS_TOKEN='your_token_here'")
        print("     Windows CMD   : setx GENIUS_ACCESS_TOKEN \"your_token_here\"")
        # Pause so the message is visible if the script is launched by
        # double-clicking on Windows (the window would close instantly otherwise)
        input("\n  Press Enter to exit...")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Banner — printed once before the loop starts
    # -------------------------------------------------------------------------
    print("=" * 55)
    print("  SMART LYRICS — Song search by title or artist")
    print("=" * 55)
    print()
    print("  Tips:")
    print("    • Search by song title     →  Bohemian Rhapsody")
    print("    • Search by artist name    →  Queen")
    print("    • Combine both             →  Queen Bohemian Rhapsody")
    print()

    # -------------------------------------------------------------------------
    # Main search loop
    # -------------------------------------------------------------------------
    while True:
        user_input = input("  Search (title / artist / both) — or 'q' to quit: ").strip()
        print()

        # Exit commands
        if user_input.lower() in ("q", "quit", "exit"):
            print("  Goodbye!")
            break

        # Empty input — ask again without counting it as an error
        if not user_input:
            print("  You didn't type anything — please enter a title or artist name.")
            print()
            continue

        query = clean_query(user_input)

        # Edge case: user typed only punctuation that got stripped to nothing
        if not query:
            print("  That doesn't look like a valid search — try a song title or artist name.")
            print()
            continue

        # -----------------------------------------------------------------------
        # API call + error handling
        # -----------------------------------------------------------------------
        try:
            hits = search_genius(query, token)
            display_results(hits)

        except requests.exceptions.HTTPError as e:
            # Surface the HTTP status code so the message is actually actionable
            status = e.response.status_code if e.response is not None else "?"
            if status == 401:
                print("  Error: Token rejected (401). Double-check GENIUS_ACCESS_TOKEN.")
            else:
                print(f"  HTTP {status} error from Genius API: {e}")

        except requests.exceptions.Timeout:
            print("  Error: Request timed out — check your internet connection and retry.")

        except requests.exceptions.RequestException as e:
            print(f"  Network error: {e}")

        except ValueError as e:
            # Raised when the API returns a structure we didn't anticipate
            print(f"  Unexpected API response: {e}")

        input("  Press Enter to continue...")
        print()


if __name__ == "__main__":
    main()
