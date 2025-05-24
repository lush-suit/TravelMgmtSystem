import sys
import unittest

sys.path.append("./")
from src.data.record_manager import RecordManager

class DummyRecord:
    def __init__(self, data):
        self._data = data
    def to_dict(self):
        return self._data

class TestRecordManager(unittest.TestCase):
    def setUp(self):
        self.manager = RecordManager()
        self.client_record = DummyRecord({"id": 1, "type": "client", "name": "Alice"})
        self.airline_record = DummyRecord({"id": 5, "type": "airline", "name": "JetSet"})
        self.flight_record = DummyRecord({
            "type": "flight", "client_id": 1, "airline_id": 5,
            "flight_date": "2024-01-01", "start_city": "A", "end_city": "B", "flight_num": "JS123"
        })
        self.flight_identifier = {
            "client_id": 1, "airline_id": 5, "flight_date": "2024-01-01", "start_city": "A", "end_city": "B"
        }

    def test_create_record_client(self):
        self.manager.create_record(self.client_record)
        self.assertEqual(len(self.manager.records["client"]), 1)
        self.assertEqual(self.manager.records["client"][0]["name"], "Alice")

    def test_create_record_airline(self):
        self.manager.create_record(self.airline_record)
        self.assertEqual(len(self.manager.records["airline"]), 1)
        self.assertEqual(self.manager.records["airline"][0]["name"], "JetSet")

    def test_create_record_flight(self):
        self.manager.create_record(self.flight_record)
        self.assertEqual(len(self.manager.records["flight"]), 1)
        self.assertEqual(self.manager.records["flight"][0]["flight_num"], "JS123")

    def test_set_records(self):
        data = {
            "client": [{"id": 2, "type": "client", "name": "Bob"}],
            "airline": [],
            "flight": []
        }
        self.manager.set_records(data)
        self.assertEqual(self.manager.records["client"][0]["name"], "Bob")
        self.assertEqual(self.manager.records["airline"], [])

    def test_delete_record_client(self):
        self.manager.create_record(self.client_record)
        self.manager.delete_record("client", 1)
        self.assertEqual(self.manager.records["client"], [])

    def test_delete_record_airline(self):
        self.manager.create_record(self.airline_record)
        self.manager.delete_record("airline", 5)
        self.assertEqual(self.manager.records["airline"], [])

    def test_delete_record_flight(self):
        self.manager.create_record(self.flight_record)
        self.manager.delete_record("flight", self.flight_identifier)
        self.assertEqual(self.manager.records["flight"], [])

    def test_update_record_client(self):
        self.manager.create_record(self.client_record)
        result = self.manager.update_record("client", 1, {"name": "Charlie"})
        self.assertTrue(result)
        self.assertEqual(self.manager.records["client"][0]["name"], "Charlie")

    def test_update_record_airline(self):
        self.manager.create_record(self.airline_record)
        result = self.manager.update_record("airline", 5, {"name": "AirMax"})
        self.assertTrue(result)
        self.assertEqual(self.manager.records["airline"][0]["name"], "AirMax")

    def test_update_record_flight(self):
        self.manager.create_record(self.flight_record)
        result = self.manager.update_record("flight", self.flight_identifier, {"flight_num": "JS456"})
        self.assertTrue(result)
        self.assertEqual(self.manager.records["flight"][0]["flight_num"], "JS456")

    def test_update_record_not_found(self):
        result = self.manager.update_record("client", 999, {"name": "Nobody"})
        self.assertFalse(result)

    def test_search_record(self):
        self.manager.create_record(self.client_record)
        results = self.manager.search_record("client", "name", "alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], 1)

    def test_display_records(self):
        self.manager.create_record(self.airline_record)
        records = self.manager.display_records("airline")
        self.assertEqual(records, [self.airline_record.to_dict()])

if __name__ == '__main__':
    unittest.main()