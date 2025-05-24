# data_manager.py

def create_record(records, record):
    records.append(record)
    return records

def delete_record(records, record_id):
    return [r for r in records if r["ID"] != record_id]

def update_record(records, record_id, updated_data):
    for r in records:
        if r["ID"] == record_id:
            r.update(updated_data)
            return True
    return False

def search_record(records, record_id):
    for r in records:
        if r["ID"] == record_id:
            return r
    return None