import sys
import os

# This line tells Python to look in the current folder for our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from modules.database_io import initialize_storage

if __name__ == "__main__":
    initialize_storage()
    app = MainWindow()
    app.mainloop()