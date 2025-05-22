import json
import os

class StorageManager:
    def __init__(self, base_path="."):
        self.base_path = base_path
        self.files = {
            "client": os.path.join(base_path, "record/clients.json"),
            "airline": os.path.join(base_path, "record/airlines.json"),
            "flight": os.path.join(base_path, "record/flights.json"),
        }

    def save_records(self, data_dict):
        """
        data_dict: {'client': [...], 'airline': [...], 'flight': [...]}
        """
        for key, records in data_dict.items():
            file_path = self.files[key]
            def to_serializable(obj):
                if hasattr(obj, 'to_dict'):
                    return obj.to_dict()
                elif hasattr(obj, '__dict__'):
                    return obj.__dict__
                return obj
            with open(file_path, "w") as file:
                json.dump([to_serializable(r) for r in records], file, indent=4)

    def load_records(self):
        all_records = {}
        for key, file_path in self.files.items():
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, "r") as file:
                    try:
                        all_records[key] = json.load(file)
                    except json.JSONDecodeError:
                        all_records[key] = []
            else:
                all_records[key] = []
        return all_records