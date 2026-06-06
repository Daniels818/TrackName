import unittest
from unittest.mock import Mock, patch
import sys
from types import SimpleNamespace

if "requests" in sys.modules and not hasattr(sys.modules["requests"], "exceptions"):
    sys.modules["requests"].exceptions = SimpleNamespace(
        RequestException=type("RequestException", (Exception,), {})
    )
import requests

from trackname.lyrics_search import search_by_lyrics, LyricsSearchError


class LyricsSearchTest(unittest.TestCase):
    @patch("trackname.lyrics_search.requests.get")
    def test_happy_path_returns_list_of_dicts(self, mock_get):
        response = Mock()
        response.json.return_value = {
            "data": [
                {"title": "Song A", "artist": {"name": "Artist A"}},
                {"title": "Song B", "artist": {"name": "Artist B"}},
                {"title": "Song A", "artist": {"name": "Artist A"}}  # Duplicado para probar deduplicación
            ]
        }
        mock_get.return_value = response

        results = search_by_lyrics("some fragment")
        self.assertEqual(results, [
            {"title": "Song A", "artist": "Artist A"},
            {"title": "Song B", "artist": "Artist B"}
        ])

    @patch("trackname.lyrics_search.requests.get")
    def test_empty_data_returns_empty_list(self, mock_get):
        response = Mock()
        response.json.return_value = {"data": []}
        mock_get.return_value = response

        self.assertEqual(search_by_lyrics("not found"), [])

    @patch("trackname.lyrics_search.requests.get")
    def test_network_failure_raises_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        with self.assertRaises(LyricsSearchError):
            search_by_lyrics("fragment")

    @patch("trackname.lyrics_search.requests.get")
    def test_malformed_json_raises_error(self, mock_get):
        response = Mock()
        response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = response
        with self.assertRaises(LyricsSearchError):
            search_by_lyrics("fragment")


if __name__ == "__main__":
    unittest.main()
