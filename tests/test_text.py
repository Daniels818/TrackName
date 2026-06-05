import unittest

from trackname.text import clean_query


class CleanQueryTest(unittest.TestCase):
    def test_lowercases_removes_noisy_punctuation_and_collapses_spaces(self):
        self.assertEqual(
            clean_query("  Bohemian,   Rhapsody!!! (Official Video)  "),
            "bohemian rhapsody official video",
        )

    def test_keeps_apostrophes_and_hyphens(self):
        self.assertEqual(
            clean_query("Don't Stop - Fleetwood Mac"),
            "don't stop - fleetwood mac",
        )

    def test_punctuation_only_becomes_empty_query(self):
        self.assertEqual(clean_query("?!()[]{}"), "")


if __name__ == "__main__":
    unittest.main()
