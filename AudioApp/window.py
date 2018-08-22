from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QToolBar
from PyQt5.QtCore import Qt
import sys
import PyAFM


class CentralWidget(QWidget):

    def __init__(self, parent=None):
        """
        Class constructor

        :param parent: Widget
        """
        super(CentralWidget, self).__init__(parent=parent, flags=Qt.Widget)

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize ui elements

        :return: None
        """

        self.show()  # Set self visible


class MainWindow(QMainWindow):

    def __init__(self, title: str = "Window", resolution: tuple = (800, 600), parent=None):
        """
        Class constructor

        :param title: str
        :param resolution: int tuple
        :param parent: Widget
        """
        super(MainWindow, self).__init__(parent=parent, flags=Qt.Window)

        self.setWindowTitle(title)
        self.resize(resolution[0], resolution[1])  # Change initial window size to resolution parameter

        self.tool_bar = QToolBar()  # Create a QToolBar object

        # Create menus that are going to be used in the top menu
        self.file_menu = self.menuBar().addMenu("&File")
        self.tools_menu = self.menuBar().addMenu("&Tools")
        self.help_menu = self.menuBar().addMenu("&Help")

        # Create QAction objects that are going to be used in tool_bar
        self.exit_action = QAction("Exit", self)
        self.about_action = QAction("About", self)

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize ui elements
        :return: None
        """

        self.addToolBar(self.tool_bar)

        self.file_menu.addAction(self.exit_action)
        self.help_menu.addAction(self.about_action)

        self.show()  # Set self visible


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = MainWindow("Audio App")
    sys.exit(app.exec_())
