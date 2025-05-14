# storage.py
import json
import os

class StorageManager:
    def __init__(self, file_path="record.jsonl"):
        self.file_path = file_path

    def save_records(self, records):
        # If records are custom objects, ensure they are serializable (e.g., use .to_dict())
        def to_serializable(obj):
            if hasattr(obj, 'to_dict'):
                return obj.to_dict()
            elif hasattr(obj, '__dict__'):
                return obj.__dict__
            return obj

        with open(self.file_path, "w") as file:
            json.dump([to_serializable(r) for r in records], file, indent=4)

    def load_records(self):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    # File exists but couldn't parse JSON; treat as empty
                    return []
        return []