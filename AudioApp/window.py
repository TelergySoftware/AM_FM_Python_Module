from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, QAction, QToolBar, QPushButton,
                             QVBoxLayout, QHBoxLayout, QDockWidget, QLineEdit, QLabel)
from PyQt5.QtCore import Qt
import sys
from PyWave.PyAFM import AFMWave
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack


class DockElement(QWidget):

    def __init__(self, label: str="", parent=None):

        super(DockElement, self).__init__(parent=parent, flags=Qt.Widget)

        self.label = QLabel(label)  # Set label text
        self.line_edit = QLineEdit()

        self.horizontal_layout = QHBoxLayout()

        self.init_ui()
        
    def init_ui(self):

        self.line_edit.setMinimumWidth(100)

        self.horizontal_layout.setAlignment(Qt.AlignRight)

        self.horizontal_layout.addWidget(self.label, alignment=Qt.AlignLeft)
        self.horizontal_layout.addStretch()
        self.horizontal_layout.addWidget(self.line_edit, alignment=Qt.AlignRight)

        self.setLayout(self.horizontal_layout)

        self.show()

    def set_text(self, text: float) -> None:

        self.line_edit.setText(str(text))

    def get_value(self) -> float:

        value = float(self.line_edit.text())
        return value


class DockContainer(QWidget):

    def __init__(self, parent=None):
        """
        Class constructor

        :param parent: Widget
        """

        super(DockContainer, self).__init__(parent=parent, flags=Qt.Widget)

        self.vertical_layout = QVBoxLayout()  # Create a vertical layout container

        # Adding some elements
        self.am_frequency_element = DockElement("AM Frequency:")
        self.am_depth_element = DockElement("AM Depth:")
        self.fs_element = DockElement("FS:")

        # Test button
        self.test_button = QPushButton("Test button")

        self.init_ui()

    def init_ui(self) -> None:
        """
        initialize ui elements

        :return: None
        """

        # bind action to button
        self.test_button.clicked.connect(self.show_values)

        # Add all widgets to the vertical_layout
        self.vertical_layout.addWidget(self.am_frequency_element)
        self.vertical_layout.addWidget(self.am_depth_element)
        self.vertical_layout.addWidget(self.fs_element)

        # Set default values
        self.am_frequency_element.set_text(60)
        self.am_depth_element.set_text(1)
        self.fs_element.set_text(200)

        self.vertical_layout.addWidget(self.test_button, alignment=Qt.AlignCenter)

        self.vertical_layout.addStretch()  # Keep widgets at the top of the vertical_layout

        self.setLayout(self.vertical_layout)  # Set self layout as vertical_layout

        self.show()  # Set self visible

    def show_values(self) -> None:
        """
        To be deleted
        :return: None
        """
        wave = AFMWave(1000, 1, 2048)

        wave.setAMFrequency(self.am_frequency_element.get_value())
        wave.setAMDepth(self.am_depth_element.get_value())
        wave.setFS(self.fs_element.get_value())

        yf = scipy.fftpack.fft(wave.getAMWave().reshape(wave.getBufferSize()))
        d = len(yf) // 2
        plt.plot(abs(yf[: (d - 1)]))
        # plt.plot(wave.getAMWave())

        plt.show()


class DockWidget(QDockWidget):

    def __init__(self, name: str="", parent=None):
        """
        Class constructor

        :param name: str
        :param parent: Widget
        """

        super(DockWidget, self).__init__(name, parent)

        self.container = DockContainer(self)  # Create a DockContainer object

        self.init_ui()

    def init_ui(self) -> None:
        """
        initialize ui elements

        :return: None
        """

        self.setFeatures(self.DockWidgetMovable)  # Set self to be only movable

        self.setWidget(self.container)  # Set self widget as container

        self.show()  # Set self visible


class TabWidget(QWidget):

    def __init__(self, parent=None):
        """
        Class constructor

        :param parent: Widget
        """
        super(TabWidget, self).__init__(parent=parent, flags=Qt.Widget)

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize ui elements
        :return: None
        """

        self.show()  # Set self visible


class CentralWidget(QTabWidget):

    def __init__(self, parent=None):
        """
        Class constructor

        :param parent: Widget
        """
        super(CentralWidget, self).__init__(parent=parent)

        self.vertical_layout = QVBoxLayout()  # Create a vertical layout container

        # Create Right and Left ear window tab object
        self.right_tab = TabWidget()
        self.left_tab = TabWidget()
        self.results_tab = TabWidget()

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize ui elements

        :return: None
        """
        # Add tabs to self
        self.addTab(self.left_tab, "Left Ear")
        self.addTab(self.right_tab, "Right Ear")
        self.addTab(self.results_tab, "Results")

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

        self.central_widget = CentralWidget(self)  # Create a CentralWidget object and set self as parent
        self.dock_widget = DockWidget("Options", self)

        self.setWindowTitle(title)
        self.resize(resolution[0], resolution[1])  # Change window size to resolution parameter

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
        # Actions setup
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.exit)

        self.setCentralWidget(self.central_widget)  # Set central_widget as the MainWindow's central widget

        self.addToolBar(self.tool_bar)  # Add tool_bar in the screen

        self.statusBar()  # Add the status bar in the screen

        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget, Qt.Vertical)  # Set dock_widget in the screen
        
        # Set top menu actions
        self.file_menu.addAction(self.exit_action)
        self.help_menu.addAction(self.about_action)

        self.showMaximized()
        self.show()  # Set self visible

    def exit(self) -> None:
        """
        Used to close the main window
        :return: None
        """
        self.close()


def get_style() -> str:
    """
    Read the style file and return its contents

    :return: str
    """

    with open("./Style/style.css", "r") as file:
        return file.read()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyleSheet(get_style())
    main_window = MainWindow("Audio App")
    sys.exit(app.exec_())
