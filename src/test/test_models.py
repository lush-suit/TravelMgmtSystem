import sys
import unittest

sys.path.append("./")
from src.conf.models import ClientRecord, AirlineRecord, FlightRecord

class TestClientRecord(unittest.TestCase):
    def setUp(self):
        self.args = {
            "record_id": 1,
            "name": "Alice Smith",
            "address_line1": "123 Main St",
            "address_line2": "Suite 456",
            "address_line3": "",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62704",
            "country": "USA",
            "phone_number": "+1-217-555-1234"
        }
        self.client = ClientRecord(**self.args)

    def test_attributes(self):
        self.assertEqual(self.client.id, self.args["record_id"])
        self.assertEqual(self.client.type, "client")
        self.assertEqual(self.client.name, self.args["name"])
        self.assertEqual(self.client.address_line1, self.args["address_line1"])
        self.assertEqual(self.client.address_line2, self.args["address_line2"])
        self.assertEqual(self.client.address_line3, self.args["address_line3"])
        self.assertEqual(self.client.city, self.args["city"])
        self.assertEqual(self.client.state, self.args["state"])
        self.assertEqual(self.client.zip_code, self.args["zip_code"])
        self.assertEqual(self.client.country, self.args["country"])
        self.assertEqual(self.client.phone_number, self.args["phone_number"])

    def test_to_dict(self):
        d = self.client.to_dict()
        for k, v in self.args.items():
            key = "id" if k == "record_id" else k
            self.assertIn(key, d)
            self.assertEqual(d[key], v)
        self.assertEqual(d["type"], "client")


class TestAirlineRecord(unittest.TestCase):
    def setUp(self):
        self.airline = AirlineRecord(record_id=7, company_name="Sky Flyers")

    def test_attributes(self):
        self.assertEqual(self.airline.id, 7)
        self.assertEqual(self.airline.type, "airline")
        self.assertEqual(self.airline.company_name, "Sky Flyers")

    def test_to_dict(self):
        d = self.airline.to_dict()
        self.assertEqual(d["id"], 7)
        self.assertEqual(d["type"], "airline")
        self.assertEqual(d["company_name"], "Sky Flyers")


class TestFlightRecord(unittest.TestCase):
    def setUp(self):
        self.flight = FlightRecord(
            client_id=11, airline_id=5, flight_date="2024-07-10",
            start_city="New York", end_city="Los Angeles"
        )

    def test_attributes(self):
        self.assertEqual(self.flight.client_id, 11)
        self.assertEqual(self.flight.airline_id, 5)
        self.assertEqual(self.flight.flight_date, "2024-07-10")
        self.assertEqual(self.flight.start_city, "New York")
        self.assertEqual(self.flight.end_city, "Los Angeles")

    def test_to_dict(self):
        d = self.flight.to_dict()
        self.assertEqual(d["client_id"], 11)
        self.assertEqual(d["airline_id"], 5)
        self.assertEqual(d["flight_date"], "2024-07-10")
        self.assertEqual(d["start_city"], "New York")
        self.assertEqual(d["end_city"], "Los Angeles")


if __name__ == '__main__':
    unittest.main()