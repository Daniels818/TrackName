import unittest
import sys
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.modules.setdefault("requests", SimpleNamespace(get=None))

from trackname.api import InvalidAPIResponseError, search_genius


class SearchGeniusTest(unittest.TestCase):
    @patch("trackname.api.requests.get")
    def test_returns_hits_from_valid_response(self, mock_get):
        response = Mock()
        response.json.return_value = {"response": {"hits": [{"result": {"title": "Song"}}]}}
        mock_get.return_value = response

        hits = search_genius("song", "token")

        self.assertEqual(hits, [{"result": {"title": "Song"}}])
        mock_get.assert_called_once_with(
            "https://api.genius.com/search",
            headers={"Authorization": "Bearer token"},
            params={"q": "song"},
            timeout=10,
        )
        response.raise_for_status.assert_called_once()

    @patch("trackname.api.requests.get")
    def test_invalid_json_raises_clear_error(self, mock_get):
        response = Mock()
        response.json.side_effect = ValueError("bad json")
        mock_get.return_value = response

        with self.assertRaisesRegex(InvalidAPIResponseError, "not valid JSON"):
            search_genius("song", "token")

    @patch("trackname.api.requests.get")
    def test_unexpected_response_shape_raises_clear_error(self, mock_get):
        response = Mock()
        response.json.return_value = {"meta": {"message": "shape changed"}}
        mock_get.return_value = response

        with self.assertRaisesRegex(InvalidAPIResponseError, "shape changed"):
            search_genius("song", "token")


if __name__ == "__main__":
    unittest.main()
