import json
import unittest
import unittest.mock
from pathlib import Path
from tempfile import TemporaryDirectory

import trackname.storage as storage


class StorageTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = TemporaryDirectory()
        self.data_dir = Path(self.tmpdir.name)
        self.history_file = self.data_dir / "history.json"
        self.favorites_file = self.data_dir / "favorites.json"

        patcher1 = unittest.mock.patch.object(storage, "DATA_DIR", self.data_dir)
        patcher2 = unittest.mock.patch.object(storage, "HISTORY_FILE", self.history_file)
        patcher3 = unittest.mock.patch.object(storage, "FAVORITES_FILE", self.favorites_file)
        patcher1.start()
        patcher2.start()
        patcher3.start()
        self.addCleanup(patcher1.stop)
        self.addCleanup(patcher2.stop)
        self.addCleanup(patcher3.stop)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_save_and_load_history(self):
        entries = [
            {
                "query": "bohemian rhapsody",
                "timestamp": "2025-01-01T00:00:00",
                "results": [{"title": "Bohemian Rhapsody", "artist": "Queen", "year": "1975", "url": ""}],
            }
        ]
        storage.save_history(entries)
        loaded = storage.load_history()
        self.assertEqual(loaded, entries)

    def test_corrupt_json_returns_empty_list(self):
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.history_file.write_text("not json", encoding="utf-8")
        self.assertEqual(storage.load_history(), [])

    def test_add_favorite_then_list(self):
        song = {"title": "Imagine", "artist": "John Lennon", "year": "1971", "url": "https://genius.com/"}
        storage.add_favorite_entry(song)
        favorites = storage.load_favorites()
        self.assertEqual(len(favorites), 1)
        self.assertEqual(favorites[0]["title"], "Imagine")

    def test_add_history_entry_creates_entry(self):
        hits = [
            {
                "result": {
                    "title": "Song A",
                    "primary_artist": {"name": "Artist A"},
                    "release_date_for_display": "2024",
                    "url": "https://genius.com/a",
                }
            }
        ]
        storage.add_history_entry("song a", hits)
        history = storage.load_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["query"], "song a")
        self.assertEqual(len(history[0]["results"]), 1)
        self.assertEqual(history[0]["results"][0]["title"], "Song A")

    def test_missing_file_returns_empty_list(self):
        self.assertEqual(storage.load_history(), [])
        self.assertEqual(storage.load_favorites(), [])

    def test_clear_history(self):
        storage.save_history([{"query": "test", "timestamp": "", "results": []}])
        storage.clear_history()
        self.assertEqual(storage.load_history(), [])

    def test_json_with_dict_returns_empty_list(self):
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.history_file.write_text('{"not": "a list"}', encoding="utf-8")
        self.assertEqual(storage.load_history(), [])

    def test_json_with_null_returns_empty_list(self):
        self.favorites_file.parent.mkdir(parents=True, exist_ok=True)
        self.favorites_file.write_text("null", encoding="utf-8")
        self.assertEqual(storage.load_favorites(), [])

    def test_empty_file_returns_empty_list(self):
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.history_file.write_text("", encoding="utf-8")
        self.assertEqual(storage.load_history(), [])

    def test_add_history_entry_limits_to_five_results(self):
        hits = [
            {"result": {"title": f"Song {i}", "primary_artist": {"name": "A"},
                         "release_date_for_display": "2024", "url": f"https://genius.com/{i}"}}
            for i in range(10)
        ]
        storage.add_history_entry("many songs", hits)
        history = storage.load_history()
        self.assertEqual(len(history[0]["results"]), 5)

    def test_add_history_entry_with_empty_hits(self):
        storage.add_history_entry("nada", [])
        history = storage.load_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["results"], [])



if __name__ == "__main__":
    unittest.main()
