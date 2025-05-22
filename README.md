Travel Agency Record Management System

A comprehensive desktop application designed for efficient management of travel agency records, including clients, airlines, and flights. This application features a user-friendly graphical user interface (GUI) and ensures data persistence using JSON files.

Features

GUI-based Management: Add, edit, search, and delete client, airline, and flight records through an intuitive graphical interface.

Persistent Storage: Records are saved in JSON files, facilitating easy viewing and portability.

Search Functionality: Efficiently search through records using various fields.

Organized Structure: Utilizes an MVC-inspired design for maintainable and extendable code.

Dependencies

All core dependencies are included within the Python standard library:
•	`sys`
•	`os`
•	`json`
•	`tkinter` (for GUI)
Note: `tkinter` is included in most Python distributions; however, if any issues arise, ensure it is installed on your system:

•	On Ubuntu/Debian: `sudo apt-get install python3-tk`

•	On MacOS/Homebrew Python: Already included
No third-party libraries are required.

Installation

Clone the repository:

git clone https://github.com/lush-suit/TravelMgmtSystem.git

cd TravelMgmtSystem

Ensure you have Python 3.6+ installed.

(Linux only) Install `tkinter` if needed:

sudo apt-get install python3-tk

Usage

To initiate the application, execute:

sh python main.py

A desktop window will launch, enabling you to manage records for clients, airlines, and flights.

Data Files

•	Entries are stored as JSON files in the `record/` directory.

•	Example formats are provided for clients, airlines, and flights.

Customization

You are encouraged to extend the data models or enhance the GUI to incorporate additional features.
