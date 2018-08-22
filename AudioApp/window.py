from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QToolBar, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from matplotlib import pyplot
import sys
from PyWave.PyAFM import AFMWave


class CentralWidget(QWidget):

    def __init__(self, parent=None):
        """
        Class constructor

        :param parent: Widget
        """
        super(CentralWidget, self).__init__(parent=parent, flags=Qt.Widget)

        self.vertical_layout = QVBoxLayout()
        self.wave = AFMWave(60, 4, 1024)
        self.wave.setAMDepth(1)
        self.wave.setAMFrequency(10)
        self.wave.setDT(0.0005)

        self.test_button = QPushButton("Test!!")  # Just testing matplotlib

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize ui elements

        :return: None
        """

        self.test_button.clicked.connect(self.plot)

        self.vertical_layout.addWidget(self.test_button)

        self.setLayout(self.vertical_layout)

        self.show()  # Set self visible

    def plot(self) -> None:
        """
        A simple test

        :return: None
        """
        pyplot.plot(range(1024), self.wave.getAMWave())
        pyplot.show()


class MainWindow(QMainWindow):

    def __init__(self, title: str = "Window", resolution: tuple = (800, 600), parent=None):
        """
        Class constructor

        :param title: str
        :param resolution: int tuple
        :param parent: Widget
        """
        super(MainWindow, self).__init__(parent=parent, flags=Qt.Window)

        self.central_widget = CentralWidget(self)

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

        self.setCentralWidget(self.central_widget)

        self.addToolBar(self.tool_bar)

        self.file_menu.addAction(self.exit_action)
        self.help_menu.addAction(self.about_action)

        self.show()  # Set self visible


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = MainWindow("Audio App")
    sys.exit(app.exec_())
