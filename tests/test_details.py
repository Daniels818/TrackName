import unittest
from unittest.mock import Mock, patch

from trackname import details


class FetchSongDetailsTest(unittest.TestCase):
    @patch("trackname.details.requests.get")
    def test_fetch_song_details_happy_path(self, mock_get):
        response = Mock()
        response.json.return_value = {
            "response": {
                "song": {
                    "album": {"name": "After Hours"},
                    "release_date_components": {"year": 2020},
                    "annotation_count": 42,
                    "stats": {"pageviews": 1234567},
                    "featured_artists": [],
                    "description": {"plain": "A song about..."},
                }
            }
        }
        mock_get.return_value = response

        result = details.fetch_song_details(123, "token")

        self.assertEqual(result["album_name"], "After Hours")
        self.assertEqual(result["album_year"], 2020)
        self.assertEqual(result["annotations"], 42)
        self.assertEqual(result["pageviews"], 1234567)
        self.assertEqual(result["featured"], [])
        self.assertEqual(result["description"], "A song about...")

        mock_get.assert_called_once_with(
            "https://api.genius.com/songs/123",
            headers={"Authorization": "Bearer token"},
            timeout=10,
        )
        response.raise_for_status.assert_called_once()

    @patch("trackname.details.requests.get")
    def test_fetch_song_details_none_fields(self, mock_get):
        response = Mock()
        response.json.return_value = {
            "response": {
                "song": {
                    "album": None,
                    "release_date_components": None,
                    "annotation_count": 0,
                    "stats": {},
                    "featured_artists": None,
                    "description": None,
                }
            }
        }
        mock_get.return_value = response

        result = details.fetch_song_details(456, "token")

        self.assertIsNone(result["album_name"])
        self.assertIsNone(result["album_year"])
        self.assertEqual(result["annotations"], 0)
        self.assertIsNone(result["pageviews"])
        self.assertEqual(result["featured"], [])
        self.assertEqual(result["description"], "")


class FetchLyricsPreviewTest(unittest.TestCase):
    """fetch_lyrics_preview(artist, title) delegates to fetch_lyrics (lyrics.ovh)
    and trims the result to the first 8 non-blank lines. These tests were
    previously written against an older bs4/Genius-scraping implementation
    that no longer exists, causing them to fail with a TypeError."""

    @patch("trackname.details.fetch_lyrics")
    def test_fetch_lyrics_preview_no_lyrics_found(self, mock_fetch_lyrics):
        mock_fetch_lyrics.return_value = ""

        result = details.fetch_lyrics_preview("Artist", "Title")

        self.assertEqual(result, "")
        mock_fetch_lyrics.assert_called_once_with("Artist", "Title")

    @patch("trackname.details.fetch_lyrics")
    def test_fetch_lyrics_preview_truncates_to_eight_lines(self, mock_fetch_lyrics):
        mock_fetch_lyrics.return_value = "\n".join(f"Line {i}" for i in range(1, 12))

        result = details.fetch_lyrics_preview("Artist", "Title")

        self.assertEqual(result, "\n".join(f"Line {i}" for i in range(1, 9)))

    @patch("trackname.details.fetch_lyrics")
    def test_fetch_lyrics_preview_strips_blank_lines(self, mock_fetch_lyrics):
        mock_fetch_lyrics.return_value = "First line\n\n   \nSecond line\n"

        result = details.fetch_lyrics_preview("Artist", "Title")

        self.assertEqual(result, "First line\nSecond line")

    @patch("trackname.details.fetch_lyrics")
    def test_fetch_lyrics_preview_fewer_than_eight_lines(self, mock_fetch_lyrics):
        mock_fetch_lyrics.return_value = "Only one line"

        result = details.fetch_lyrics_preview("Artist", "Title")

        self.assertEqual(result, "Only one line")


if __name__ == "__main__":
    unittest.main()
