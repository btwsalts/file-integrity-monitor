import tempfile
import unittest
from pathlib import Path

from src.fim import collect_hashes, scan


class FileIntegrityTests(unittest.TestCase):
    def test_detects_added_modified_deleted_and_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "same.txt").write_text("same", encoding="utf-8")
            (root / "changed.txt").write_text("new", encoding="utf-8")
            (root / "added.txt").write_text("added", encoding="utf-8")

            baseline = {
                "same.txt": "placeholder",
                "changed.txt": "old-hash",
                "deleted.txt": "deleted-hash",
            }

            current = collect_hashes(root, root / ".baseline")
            baseline["same.txt"] = current["same.txt"]

            result = scan(current, baseline)

            self.assertEqual(result["added"], ["added.txt"])
            self.assertEqual(result["deleted"], ["deleted.txt"])
            self.assertEqual(result["modified"], ["changed.txt"])
            self.assertEqual(result["unchanged"], ["same.txt"])

    def test_hashes_nested_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nested = root / "logs"
            nested.mkdir()
            (nested / "app.log").write_text("event", encoding="utf-8")

            current = collect_hashes(root, root / ".baseline")

            self.assertIn("logs/app.log", current)


if __name__ == "__main__":
    unittest.main()
