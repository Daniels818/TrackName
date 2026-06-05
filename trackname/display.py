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
