import os
import shutil
import sys
import tempfile
import unittest

sys.path.append("./")
from src.data.storage import StorageManager

class DummyObj:
    def __init__(self, name):
        self.name = name
    def to_dict(self):
        return {'name': self.name}

class StorageManagerTest(unittest.TestCase):
    def setUp(self):
        # Create a temp directory for test files
        self.test_dir = tempfile.mkdtemp()
        # Pre-create 'record' subdirectory, as StorageManager expects it
        self.record_dir = os.path.join(self.test_dir, 'record')
        os.makedirs(self.record_dir, exist_ok=True)
        self.sm = StorageManager(base_path=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_save_and_load_dicts(self):
        data = {
            'client': [{'id': 1, 'name': 'Alice'}],
            'airline': [{'id': 2, 'name': 'AirX'}],
            'flight': [{'id': 3, 'src': 'LAX', 'dst': 'JFK'}],
        }
        self.sm.save_records(data)
        # Ensure files written
        for key in data:
            path = self.sm.files[key]
            self.assertTrue(os.path.exists(path), f"{path} should exist")
        # Test load_records returns correct data
        loaded = self.sm.load_records()
        self.assertEqual(loaded, data)

    def test_save_and_load_with_to_dict_obj(self):
        data = {
            'client': [DummyObj('John')],
            'airline': [],
            'flight': [],
        }
        self.sm.save_records(data)
        loaded = self.sm.load_records()
        self.assertEqual(loaded['client'], [{'name': 'John'}])
        self.assertEqual(loaded['airline'], [])
        self.assertEqual(loaded['flight'], [])

    def test_load_with_missing_or_empty_files(self):
        # No save, so files missing!
        loaded = self.sm.load_records()
        self.assertEqual(loaded, {'client': [], 'airline': [], 'flight': []})
        # Create empty files explicitly
        for path in self.sm.files.values():
            open(path, 'w').close()
        loaded_empty = self.sm.load_records()
        self.assertEqual(loaded_empty, {'client': [], 'airline': [], 'flight': []})
        # Corrupted file case
        with open(self.sm.files['client'], 'w') as f:
            f.write('INVALID JSON')
        loaded_with_corrupt = self.sm.load_records()
        self.assertEqual(loaded_with_corrupt['client'], [])
        self.assertEqual(loaded_with_corrupt['airline'], [])
        self.assertEqual(loaded_with_corrupt['flight'], [])

if __name__ == "__main__":
    unittest.main()