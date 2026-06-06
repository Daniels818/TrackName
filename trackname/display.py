def display_results(hits):
    """Print the top Genius results to the console."""
    if not hits:
        print("  No songs found. Try a different title or artist name.")
        return

    for i, hit in enumerate(hits[:5], 1):
        result = hit.get("result")
        if not result:
            continue

        title = result.get("title", "Unknown title")
        artist = result.get("primary_artist", {}).get("name", "Unknown artist")
        date = result.get("release_date_for_display", "Unknown date")
        url = result.get("url", "")

        print(f"  {i}. {title} - {artist} ({date})")
        if url:
            print(f"     {url}")
        print()


def display_song_detail(hit, details, lyrics_preview):
    """Print detailed song info to the console."""
    result = hit.get("result", {})
    title = result.get("title", "Unknown title")
    artist = result.get("primary_artist", {}).get("name", "Unknown artist")

    print("\u2550" * 46)
    print(f"  {title} \u2014 {artist}")
    print("\u2550" * 46)

    album = details.get("album_name")
    year = details.get("album_year")
    if album and year:
        print(f"  \u00c1lbum      : {album} ({year})")
    elif album:
        print(f"  \u00c1lbum      : {album}")
    elif year:
        print(f"  \u00c1lbum      : {year}")

    featured = details.get("featured", [])
    if featured:
        print(f"  Featured   : {', '.join(featured)}")
    else:
        print("  Featured   : (ninguno)")

    annotations = details.get("annotations", 0)
    pageviews = details.get("pageviews")
    views_str = f"{pageviews:,}" if pageviews is not None else "N/A"
    print(f"  Anotaciones: {annotations}  |  Vistas: {views_str}")

    description = details.get("description", "")
    if description:
        print()
        print("  Descripci\u00f3n:")
        print(f'  "{description}"')

    if lyrics_preview:
        print()
        print("  Extracto de letra:")
        for line in lyrics_preview.split("\n"):
            print(f"  {line}")
    else:
        print()
        print("  (letra no disponible)")

    print("\u2550" * 46)
