"""
    Start point of gui
"""


from PySide6.QtWidgets import QApplication
from src.telegram_client.frontend.gui import main_window
import sys



def start_gui():
    app = QApplication(sys.argv)
    main_window_widget = main_window.MainWindow(None)
    main_window_widget.show()
    sys.exit(app.exec_())

