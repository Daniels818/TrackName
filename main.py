# =============================================================================
# SMART LYRICS — Song lyrics search engine
# Phase 3: Genius API integration
#
# How it works:
#   1. The user types a lyric fragment.
#   2. We clean it up (lowercase, strip punctuation that messes up searches).
#   3. We hit the Genius search endpoint and show the top 5 results.
# =============================================================================

import os
import re
import sys

import requests


def clean_text(text):
    """Normalize the user's input so the API has a better chance of finding it.

    We go lowercase and strip out punctuation that Genius doesn't care about.
    Apostrophes are intentionally kept — we don't want "don't" to become "dont".
    Parentheses and brackets are also removed because they often wrap extra info
    like "(Official Video)" that would only confuse the search query.
    """
    text = text.lower()
    # Ditch common punctuation that adds noise without helping the search
    text = re.sub(r'[.,;:!?"()\[\]{}]', "", text)
    return text.strip()


def search_genius(query, token):
    """Send a search request to the Genius API and return the list of hits.

    Args:
        query: The cleaned lyric fragment to search for.
        token: A valid Genius Client Access Token.

    Returns:
        A list of hit objects from the API response.

    Raises:
        requests.exceptions.HTTPError: If the API returns a non-2xx status code.
        requests.exceptions.Timeout: If the server doesn't respond in time.
        requests.exceptions.RequestException: For any other network-level problem.
        ValueError: If the JSON response doesn't have the expected structure.
    """
    url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query}

    # 10-second timeout so we don't hang forever waiting on a slow connection
    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    # Guard against weird API responses before we try to drill into the dict
    if "response" not in data or "hits" not in data.get("response", {}):
        raise ValueError(
            f"Unexpected API response: {data.get('meta', {}).get('message', 'no details')}"
        )

    return data["response"]["hits"]


def display_results(hits):
    """Print the top results to the console in a readable format.

    Shows at most 5 results. If the API returns nothing, we let the user know
    right away instead of just printing a blank screen.

    Args:
        hits: The list of hit objects returned by search_genius().
    """
    if not hits:
        print("  No songs found with that fragment.")
        return

    for i, hit in enumerate(hits[:5], 1):
        # Each "hit" should have a "result" key — but let's not assume the API
        # is always consistent. Skip any malformed entries gracefully.
        result = hit.get("result")
        if not result:
            continue

        title = result.get("title", "Unknown title")
        # The artist can also be missing in rare edge cases, so we fall back safely
        artist = result.get("primary_artist", {}).get("name", "Unknown artist")
        date = result.get("release_date_for_display", "Unknown date")
        url = result.get("url", "")

        print(f"  {i}. {title} — {artist} ({date})")
        if url:
            print(f"     {url}")
        print()


def main():
    """Entry point — set up the token, then loop asking for lyric fragments."""
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
        # Pause before quitting so the message is readable when the script is
        # launched by double-clicking on Windows (which would close the window instantly)
        input("\n  Press Enter to exit...")
        sys.exit(1)

    # Print the banner once, outside the loop — no need to repeat it every search
    print("=" * 55)
    print("  SMART LYRICS — Song lyrics search engine")
    print("=" * 55)
    print()

    while True:
        user_input = input("  Enter a lyric fragment (or 'q' to quit): ").strip()
        print()

        if user_input.lower() in ("q", "quit", "exit"):
            print("  Goodbye!")
            break

        if not user_input:
            print("  You didn't type anything — try again.")
            print()
            continue

        clean_query = clean_text(user_input)

        # Edge case: the user typed only punctuation (e.g. "???"), which gets
        # stripped to nothing — sending an empty string to the API is pointless
        if not clean_query:
            print("  That doesn't look like a lyric — try using actual words.")
            print()
            continue

        try:
            hits = search_genius(clean_query, token)
            display_results(hits)
        except requests.exceptions.HTTPError as e:
            # Pull out the status code so the message is actually useful
            status = e.response.status_code if e.response is not None else "?"
            if status == 401:
                print("  Error: Token rejected (401). Double-check GENIUS_ACCESS_TOKEN.")
            else:
                print(f"  HTTP {status} error from Genius API: {e}")
        except requests.exceptions.Timeout:
            print("  Error: Request timed out — check your internet connection and try again.")
        except requests.exceptions.RequestException as e:
            print(f"  Network error: {e}")
        except ValueError as e:
            # Raised when the API sends back a response we didn't expect
            print(f"  Unexpected API response: {e}")

        input("  Press Enter to continue...")
        print()


if __name__ == "__main__":
    main()
