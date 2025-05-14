# models.py
class ClientRecord:
    def __init__(self, record_id, name, address_line1, address_line2, address_line3, city, state, zip_code, country, phone_number):
        self.id = record_id
        self.type = "client"
        self.name = name
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.address_line3 = address_line3
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.phone_number = phone_number

    def to_dict(self):
        return self.__dict__


class AirlineRecord:
    def __init__(self, record_id, company_name):
        self.id = record_id
        self.type = "airline"
        self.company_name = company_name

    def to_dict(self):
        return self.__dict__


class FlightRecord:
    def __init__(self, client_id, airline_id, flight_date, start_city, end_city):
        self.client_id = client_id
        self.airline_id = airline_id
        self.flight_date = flight_date
        self.start_city = start_city
        self.end_city = end_city

    def to_dict(self):
        return self.__dict__