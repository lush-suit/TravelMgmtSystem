# main.py
import sys

sys.path.append("./")
from src.gui.gui import TravelAgentGUI
from src.data.record_manager import RecordManager
from src.data.storage import StorageManager

if __name__ == "__main__":
    record_manager = RecordManager()
    storage_manager = StorageManager()

    app = TravelAgentGUI(record_manager, storage_manager)
    app.run()