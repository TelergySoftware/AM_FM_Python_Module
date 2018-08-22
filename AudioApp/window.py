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

        self.vertical_layout = QVBoxLayout()  # Create a vertical layout container
        
        # Create an object of AFMWave with carrier frequency of 60Hz, 4 of amplitude and buffer size of 1024
        self.wave = AFMWave(60, 4, 1024)
        self.wave.setAMDepth(1)
        self.wave.setAMFrequency(10)
        self.wave.setDT(0.0005)  # Value of dt in seconds

        self.test_button = QPushButton("Test!!")  # Just testing matplotlib

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize ui elements

        :return: None
        """

        self.test_button.clicked.connect(self.plot)  # When test button is clicked, call self.plot

        self.vertical_layout.addWidget(self.test_button)  # Add test button to vertical_layout

        self.setLayout(self.vertical_layout)  # Set this widget layout as vertical_layout

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

        self.central_widget = CentralWidget(self)  # Create a CentralWidget object and set self as parent

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

        self.setCentralWidget(self.central_widget)  # Set central_widget as the MainWindow's central widget

        self.addToolBar(self.tool_bar)  # Add tool_bar in the screen
        
        # Set top menu actions
        self.file_menu.addAction(self.exit_action)
        self.help_menu.addAction(self.about_action)

        self.show()  # Set self visible


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = MainWindow("Audio App")
    sys.exit(app.exec_())
