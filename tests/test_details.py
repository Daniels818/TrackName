import unittest
from unittest.mock import MagicMock, Mock, patch

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

    def _mock_bs4_import(self):
        """Return a context manager that patches __import__ so bs4 resolves to a MagicMock."""
        import builtins
        original = builtins.__import__
        mock_bs4 = MagicMock()

        def mock_import(name, *args, **kwargs):
            if name == "bs4":
                return mock_bs4
            return original(name, *args, **kwargs)

        return patch("builtins.__import__", side_effect=mock_import), mock_bs4

    @patch("trackname.details.requests.get")
    def test_fetch_lyrics_preview_bs4_not_available(self, mock_get):
        import builtins
        original = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "bs4":
                raise ImportError
            return original(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            result = details.fetch_lyrics_preview("https://genius.com/")

        self.assertEqual(result, "")
        mock_get.assert_not_called()

    @patch("trackname.details.requests.get")
    def test_fetch_lyrics_preview_request_fails(self, mock_get):
        mock_get.side_effect = Exception("connection error")

        ctx, _ = self._mock_bs4_import()
        with ctx:
            result = details.fetch_lyrics_preview("https://genius.com/")

        self.assertEqual(result, "")
        mock_get.assert_called_once_with("https://genius.com/", timeout=8)

    @patch("trackname.details.requests.get")
    def test_fetch_lyrics_preview_parses_lyrics(self, mock_get):
        ctx, mock_bs4 = self._mock_bs4_import()

        mock_soup = MagicMock()
        mock_bs4.BeautifulSoup.return_value = mock_soup
        mock_container = MagicMock()
        mock_container.get_text.return_value = (
            "First line\nSecond line\nThird line\nFourth line\nFifth line"
        )
        mock_soup.select.return_value = [mock_container]

        response = Mock()
        response.text = "<html>dummy</html>"
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        with ctx:
            result = details.fetch_lyrics_preview("https://genius.com/song")

        self.assertEqual(result, "First line\nSecond line\nThird line\nFourth line")

    @patch("trackname.details.requests.get")
    def test_fetch_lyrics_preview_no_lyrics_container(self, mock_get):
        ctx, mock_bs4 = self._mock_bs4_import()

        mock_soup = MagicMock()
        mock_bs4.BeautifulSoup.return_value = mock_soup
        mock_soup.select.return_value = []

        response = Mock()
        response.text = "<html>dummy</html>"
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        with ctx:
            result = details.fetch_lyrics_preview("https://genius.com/song")

        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
