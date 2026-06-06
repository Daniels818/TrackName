def display_results(hits):
    """Print the top Genius results to the console."""
    if not hits:
        print("  No songs found. Try a different title or artist name.")
        return

    for i, hit in enumerate(hits[:5], 1):
        result = (hit or {}).get("result")
        if not result:
            continue

        title = result.get("title", "Unknown title")
        artist = (result.get("primary_artist") or {}).get("name", "Unknown artist")
        date = result.get("release_date_for_display", "Unknown date")
        url = result.get("url", "")

        print(f"  {i}. {title} - {artist} ({date})")
        if url:
            print(f"     {url}")
        print()


def display_song_detail(hit, details, lyrics_preview):
    """Print detailed song info to the console."""
    result = (hit or {}).get("result") or {}
    title = result.get("title", "Unknown title")
    artist = (result.get("primary_artist") or {}).get("name", "Unknown artist")

    print("\u2550" * 46)
    print(f"  {title} \u2014 {artist}")
    print("\u2550" * 46)

    album = details.get("album_name")
    year = details.get("album_year")
    if album and year:
        print(f"  Album      : {album} ({year})")
    elif album:
        print(f"  Album      : {album}")
    elif year:
        print(f"  Album      : {year}")

    featured = details.get("featured", [])
    if featured:
        print(f"  Featured   : {', '.join(featured)}")
    else:
        print("  Featured   : (none)")

    annotations = details.get("annotations", 0)
    pageviews = details.get("pageviews")
    views_str = f"{pageviews:,}" if pageviews is not None else "N/A"
    print(f"  Annotations: {annotations}  |  Views: {views_str}")

    description = details.get("description", "")
    if description:
        print()
        print("  Description:")
        print(f'  "{description}"')

    if lyrics_preview:
        print()
        print("  Lyrics preview:")
        for line in lyrics_preview.split("\n"):
            print(f"  {line}")
    else:
        print()
        print("  (lyrics not available)")

    print("\u2550" * 46)
