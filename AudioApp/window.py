from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, QAction, QToolBar, QPushButton,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QDockWidget, QLineEdit, QLabel, QSizePolicy,
                             QMessageBox)
from PyQt5.QtCore import Qt
import sys
from PyWave.PyAFM import AFMWave
import Calc
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
        self.c_frequency_element = DockElement("Carrier Frequency:")
        self.c_amplitude_element = DockElement("Carrier Amplitude:")
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
        self.vertical_layout.addWidget(self.c_frequency_element)
        self.vertical_layout.addWidget(self.c_amplitude_element)
        self.vertical_layout.addWidget(self.am_frequency_element)
        self.vertical_layout.addWidget(self.am_depth_element)
        self.vertical_layout.addWidget(self.fs_element)

        # Set default values
        self.c_frequency_element.set_text(1000)
        self.c_amplitude_element.set_text(1)
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
        wave = AFMWave(self.c_frequency_element.get_value(), self.c_amplitude_element.get_value(), 2048)

        wave.setAMFrequency(self.am_frequency_element.get_value())
        wave.setAMDepth(self.am_depth_element.get_value())
        wave.setFS(self.fs_element.get_value())

        frq, yf = Calc.calc_fft(wave.getAMWave(), wave.getBufferSize(), wave.getFS())

        fig, ax = plt.subplots(2)
        ax[0].plot(frq[:wave.getBufferSize() // 2], abs(yf[:wave.getBufferSize() // 2]))
        ax[1].plot(wave.getAMWave())

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


class SettingsTabWidget(QWidget):

    def __init__(self, parent=None):
        """
        Class constructor

        :param parent: Widget
        """
        super(SettingsTabWidget, self).__init__(parent=parent, flags=Qt.Widget)

        self.left_layout = QGridLayout()
        self.right_layout = QGridLayout()
        self.horizontal_layout = QHBoxLayout()

        # Labels for wave components on the left side
        self.left_components = []
        for i in range(4):
            component = QLabel("Component " + str(i + 1))
            component.setMaximumHeight(30)
            component.setProperty("UseSeparator", True)
            component.setProperty("SettingsLabel", True)
            self.left_components.append(component)

        # Labels for wave components on the right side
        self.right_components = []
        for i in range(4):
            component = QLabel("Component " + str(i + 1))
            component.setMaximumHeight(30)
            component.setProperty("UseSeparator", True)
            component.setProperty("SettingsLabel", True)
            self.right_components.append(component)

        # Initial buttons that will be used to change wave parameters
        # Left side
        self.left_buttons = []
        for i in range(4):
            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            self.left_buttons.append(button)

        # Initial buttons that will be used to change wave parameters
        # Right side
        self.right_buttons = []
        for i in range(4):
            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            self.right_buttons.append(button)

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize ui elements
        :return: None
        """

        self.left_layout.setSpacing(0)  # Set left layout spacing as zero

        # Add the labels from the left side to left_layout
        self.left_layout.addWidget(self.left_components[0], 0, 0)
        self.left_layout.addWidget(self.left_components[1], 0, 1)
        self.left_layout.addWidget(self.left_components[2], 0, 2)
        self.left_layout.addWidget(self.left_components[3], 0, 3)
        # Add initial buttons from the left side to left_layout
        self.left_layout.addWidget(self.left_buttons[0], 1, 0)
        self.left_layout.addWidget(self.left_buttons[1], 1, 1)
        self.left_layout.addWidget(self.left_buttons[2], 1, 2)
        self.left_layout.addWidget(self.left_buttons[3], 1, 3)

        # Add empty widgets to align everything on the top
        self.left_layout.addWidget(QWidget(self), 2, 0)
        self.left_layout.addWidget(QWidget(self), 2, 1)
        self.left_layout.addWidget(QWidget(self), 2, 2)
        self.left_layout.addWidget(QWidget(self), 2, 3)

        self.right_layout.setSpacing(0)  # Set right layout spacing as zero

        # Add the labels from the right side to right_layout
        self.right_layout.addWidget(self.right_components[0], 0, 0)
        self.right_layout.addWidget(self.right_components[1], 0, 1)
        self.right_layout.addWidget(self.right_components[2], 0, 2)
        self.right_layout.addWidget(self.right_components[3], 0, 3)
        # Add initial buttons from the right side to right_layout
        self.right_layout.addWidget(self.right_buttons[0], 1, 0)
        self.right_layout.addWidget(self.right_buttons[1], 1, 1)
        self.right_layout.addWidget(self.right_buttons[2], 1, 2)
        self.right_layout.addWidget(self.right_buttons[3], 1, 3)

        # Add empty widgets to align everything on the top
        self.right_layout.addWidget(QWidget(self), 2, 0)
        self.right_layout.addWidget(QWidget(self), 2, 1)
        self.right_layout.addWidget(QWidget(self), 2, 2)
        self.right_layout.addWidget(QWidget(self), 2, 3)

        self.right_layout.setRowStretch(0, 1)
        self.right_layout.setRowStretch(1, 3)

        # Add right and left layout to horizontal layout
        self.horizontal_layout.addLayout(self.left_layout)
        self.horizontal_layout.addLayout(self.right_layout)
        # Set self layout as horizontal_layout
        self.setLayout(self.horizontal_layout)

        self.show()  # Set self visible


class ResultsTabWidget(QWidget):

    def __init__(self, parent=None):
        """
        Class constructor

        :param parent: Widget
        """
        super(ResultsTabWidget, self).__init__(parent=parent, flags=Qt.Widget)

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
        self.settings_tab = SettingsTabWidget()
        self.results_tab = ResultsTabWidget()

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize ui elements

        :return: None
        """
        # Add tabs to self
        self.addTab(self.settings_tab, "Settings")
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

    def closeEvent(self, e):

        reply = QMessageBox.question(self, "Exit?", "Do you really want to quit?",
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            e.accept()
        else:
            e.ignore()


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
