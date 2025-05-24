import unittest
from data_manager import create_record, delete_record, update_record, search_record

class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.sample_clients = [
            {"ID": 1, "Type": "Client", "Name": "Alice", "City": "London"},
            {"ID": 2, "Type": "Client", "Name": "Bob", "City": "Paris"}
        ]

    def test_create_record(self):
        new_client = {"ID": 3, "Type": "Client", "Name": "Charlie", "City": "Berlin"}
        result = create_record(self.sample_clients.copy(), new_client)
        self.assertEqual(len(result), 3)
        self.assertIn(new_client, result)

    def test_delete_record(self):
        result = delete_record(self.sample_clients.copy(), 1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["ID"], 2)

    def test_update_record(self):
        updated = update_record(self.sample_clients.copy(), 1, {"Name": "Alicia"})
        self.assertTrue(updated)

    def test_update_nonexistent_record(self):
        updated = update_record(self.sample_clients.copy(), 99, {"Name": "Ghost"})
        self.assertFalse(updated)

    def test_search_record_found(self):
        result = search_record(self.sample_clients, 2)
        self.assertIsNotNone(result)
        self.assertEqual(result["Name"], "Bob")

    def test_search_record_not_found(self):
        result = search_record(self.sample_clients, 99)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()