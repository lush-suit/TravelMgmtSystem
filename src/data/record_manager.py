# record_manager.py

class RecordManager:
    def __init__(self):
        self.records = {
            "client": [],
            "airline": [],
            "flight": []
        }

    def set_records(self, records_dict):
        for key in self.records:
            self.records[key] = records_dict.get(key, [])

    def create_record(self, record):
        # record must have 'type'
        rec_type = record.to_dict().get("type")
        if rec_type == "client":
            self.records["client"].append(record.to_dict())
        elif rec_type == "airline":
            self.records["airline"].append(record.to_dict())
        elif rec_type == "flight" or (
             "flight_date" in record.to_dict() and rec_type is None
        ):
            self.records["flight"].append(record.to_dict())

    def delete_record(self, rec_type, record_id_or_composite):
        if rec_type == "client":
            self.records["client"] = [record for record in self.records["client"] if record.get("id") != record_id_or_composite]
        elif rec_type == "airline":
            self.records["airline"] = [record for record in self.records["airline"] if record.get("id") != record_id_or_composite]
        elif rec_type == "flight":
            # record_id_or_composite: a dict with {client_id, airline_id, flight_date, start_city, end_city}
            to_del = record_id_or_composite
            def flight_match(f):
                return (
                    f.get("client_id") == to_del["client_id"] and
                    f.get("airline_id") == to_del["airline_id"] and
                    str(f.get("flight_date")) == str(to_del["flight_date"]) and
                    f.get("start_city") == to_del["start_city"] and
                    f.get("end_city") == to_del["end_city"]
                )
            self.records["flight"] = [f for f in self.records["flight"] if not flight_match(f)]

    def update_record(self, rec_type, record_id_or_composite, updated_values):
        if rec_type == "client":
            for record in self.records["client"]:
                if record.get("id") == record_id_or_composite:
                    record.update(updated_values)
                    return True
        elif rec_type == "airline":
            for record in self.records["airline"]:
                if record.get("id") == record_id_or_composite:
                    record.update(updated_values)
                    return True
        elif rec_type == "flight":
            to_update = record_id_or_composite
            for record in self.records["flight"]:
                if (
                    record.get("client_id") == to_update["client_id"] and
                    record.get("airline_id") == to_update["airline_id"] and
                    str(record.get("flight_date")) == str(to_update["flight_date"]) and
                    record.get("start_city") == to_update["start_city"] and
                    record.get("end_city") == to_update["end_city"]
                ):
                    record.update(updated_values)
                    return True
        return False

    def search_record(self, rec_type, field, value):
        return [record for record in self.records[rec_type] if str(record.get(field, "")).lower() == value.lower()]

    def display_records(self, rec_type):
        return self.records[rec_type]