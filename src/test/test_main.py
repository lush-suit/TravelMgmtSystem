import unittest
from unittest.mock import patch, MagicMock
import os

class TestMainEntryPoint(unittest.TestCase):
    @patch('src.gui.gui.TravelAgentGUI')
    @patch('src.data.storage.StorageManager')
    @patch('src.data.record_manager.RecordManager')
    def test_main_entry_point(self, mock_record_manager, mock_storage_manager, mock_travel_agent_gui):
        # Patch sys.modules to simulate "__main__"
        import importlib
        import sys

        # Setup mocks
        mock_record_manager_instance = MagicMock()
        mock_storage_manager_instance = MagicMock()
        mock_gui_instance = MagicMock()

        mock_record_manager.return_value = mock_record_manager_instance
        mock_storage_manager.return_value = mock_storage_manager_instance
        mock_travel_agent_gui.return_value = mock_gui_instance

        # Get the absolute path to main.py relative to this test file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_py_path = os.path.join(current_dir, '..', 'main.py')
        main_py_path = os.path.abspath(main_py_path)

        # Dynamically import main as __main__
        spec = importlib.util.spec_from_file_location("__main__", main_py_path)
        main = importlib.util.module_from_spec(spec)

        # Ensure __name__ == "__main__" and run code
        sys.modules["__main__"] = main
        spec.loader.exec_module(main)

        # Check instantiations and app.run() call
        mock_record_manager.assert_called_once()
        mock_storage_manager.assert_called_once()
        mock_travel_agent_gui.assert_called_once_with(
            mock_record_manager_instance,
            mock_storage_manager_instance
        )
        mock_gui_instance.run.assert_called_once()

if __name__ == "__main__":
    unittest.main()