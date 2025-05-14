# record_manager.py

class RecordManager:
    def __init__(self):
        self.records = []  # Internal storage for all records

    def create_record(self, record):
        self.records.append(record.to_dict())

    def delete_record(self, record_id):
        # Robust: avoid KeyError if any record is missing 'id'
        self.records = [record for record in self.records if record.get("id") != record_id]

    def update_record(self, record_id, updated_values):
        for record in self.records:
            if record.get("id") == record_id:
                record.update(updated_values)
                return True
        return False

    def search_record(self, field, value):
        return [record for record in self.records if record.get(field) == value]

    def display_records(self):
        return self.records