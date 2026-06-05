import io
import unittest
from contextlib import redirect_stdout

from trackname.display import display_results


class DisplayResultsTest(unittest.TestCase):
    def test_prints_empty_result_message(self):
        output = io.StringIO()

        with redirect_stdout(output):
            display_results([])

        self.assertIn("No songs found", output.getvalue())

    def test_prints_top_five_results_with_links(self):
        hits = [
            {
                "result": {
                    "title": f"Song {i}",
                    "primary_artist": {"name": "Artist"},
                    "release_date_for_display": "2024",
                    "url": f"https://genius.com/song-{i}",
                }
            }
            for i in range(1, 7)
        ]
        output = io.StringIO()

        with redirect_stdout(output):
            display_results(hits)

        text = output.getvalue()
        self.assertIn("1. Song 1 - Artist (2024)", text)
        self.assertIn("https://genius.com/song-1", text)
        self.assertIn("5. Song 5 - Artist (2024)", text)
        self.assertNotIn("Song 6", text)

    def test_skips_malformed_hits(self):
        output = io.StringIO()

        with redirect_stdout(output):
            display_results([{"unexpected": "shape"}])

        self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
