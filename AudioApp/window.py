from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, QAction, QToolBar, QPushButton,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QDockWidget, QLineEdit, QLabel, QSizePolicy,
                             QMessageBox, QGroupBox, QDesktopWidget, QCheckBox)
from PyQt5.QtCore import Qt
import sys
from PyWave.PyAFM import AFMWave
import Calc
from ValuePickers import *
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import scipy.fftpack
import random


class PlotWidget(QWidget):

    def __init__(self, parent=None):
        
        super(PlotWidget, self).__init__(parent=parent, flags=Qt.Widget)

        # Setting up graph style
        plt.style.use("grayscale")
        plt.rcParams['axes.facecolor'] = "61656b"
        plt.rcParams['figure.facecolor'] = "61656b"
        plt.rcParams.update({"font.size": 8})

        # Starting Figure and Canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Setting up the layout
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.canvas, alignment=Qt.AlignHCenter)
        self.setLayout(self.vertical_layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.plot()  # Plot data

    def plot(self):

        data = [random.random() for i in range(50)]

        ax = self.figure.add_subplot(111)

        ax.plot(data, "-")
        self.canvas.draw()


class DockElement(QWidget):

    def __init__(self, label: str = "", parent=None):

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
        self.n_stimuli = DockElement("Number of stimuli:")
        self.stimuli_duration = DockElement("Stimuli duration:")
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
        self.vertical_layout.addWidget(self.n_stimuli)
        self.vertical_layout.addWidget(self.stimuli_duration)
        self.vertical_layout.addWidget(self.fs_element)

        # Set default values
        self.n_stimuli.set_text(10)
        self.stimuli_duration.set_text(1.024)
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


class GroupBox(QGroupBox):

    def __init__(self, parent=None):

        super(GroupBox, self).__init__(parent)

    def resizeEvent(self, e):

        self.resize(self.parentWidget().width() / 2 - 10, self.size().height())
        self.setMaximumWidth(self.parentWidget().width() / 2 - 10)


class SettingsTabWidget(QWidget):

    def __init__(self, parent=None):
        """
        Class constructor

        :param parent: Widget
        """
        super(SettingsTabWidget, self).__init__(parent=parent, flags=Qt.Widget)

        self.left_layout = QGridLayout()  # Layout that will gather the left parameters
        self.right_layout = QGridLayout()  # Layout that will gather the right parameters
        self.horizontal_layout = QHBoxLayout()  # Layout that will gather the left and right grids
        self.vertical_layout = QVBoxLayout()  # Layout that will gather all layouts in this tab

        self.preview_fft_layout = QHBoxLayout()  # Layout that will gather the FFT previews
        self.preview_expected_layout = QHBoxLayout()  # Layout that will gather the expected results previews

        self.left_group = GroupBox(self)  # Separator for the left parameters
        self.right_group = GroupBox(self)  # Separator for the right parameters
        # self.left_preview = GroupBox(self)  # Separator for the left previews
        # self.right_preview = GroupBox(self)  # Separator for the right previews

        self.preview_fft_left = PlotWidget(self)  # Left FFT preview
        self.preview_fft_right = PlotWidget(self)  # Right FFT preview
        self.preview_expected_left = PlotWidget(self)  # Left expected result preview
        self.preview_expected_right = PlotWidget(self)  # Right expected result preview

        self.enable_left = QCheckBox()  # Checkbox that will enable/disable the left components
        self.enable_right = QCheckBox()  # Checkbox that will enable/disable the right components

        # Labels for wave components on the left side
        self.left_components = []
        for i in range(4):
            component = QLabel(str(i + 1))
            component.setMaximumHeight(30)
            component.setMinimumWidth(50)
            component.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            component.setProperty("UseSeparator", True)
            component.setProperty("SettingsLabel", True)
            self.left_components.append(component)

        # Labels for wave components on the right side
        self.right_components = []
        for i in range(4):
            component = QLabel(str(i + 1))
            component.setMaximumHeight(30)
            component.setMinimumWidth(50)
            component.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            component.setProperty("UseSeparator", True)
            component.setProperty("SettingsLabel", True)
            self.right_components.append(component)

        # Initial buttons that will be used to change wave parameters
        # Left side
        self.left_buttons_frequency = []
        self.left_buttons_modulation = []
        self.left_buttons_am_deepness = []
        self.left_buttons_fm_deepness = []
        self.left_buttons_fm_phase = []
        self.left_buttons_amplitude = []
        for i in range(4):
            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            button.clicked.connect(self.on_click_frequency)
            self.left_buttons_frequency.append(button)

            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            button.clicked.connect(self.on_click_am_percentage)
            self.left_buttons_am_deepness.append(button)

            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            button.clicked.connect(self.on_click_modulation)
            self.left_buttons_modulation.append(button)

            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            button.clicked.connect(self.on_click_fm_percentage)
            self.left_buttons_fm_deepness.append(button)

            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            button.clicked.connect(self.on_click_fm_phase)
            self.left_buttons_fm_phase.append(button)

            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            button.clicked.connect(self.on_click_amplitude)
            self.left_buttons_amplitude.append(button)

        # Initial buttons that will be used to change wave parameters
        # Right side
        self.right_buttons_frequency = []
        self.right_buttons_modulation = []
        self.right_buttons_am_deepness = []
        self.right_buttons_fm_deepness = []
        self.right_buttons_fm_phase = []
        self.right_buttons_amplitude = []
        for i in range(4):
            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            button.clicked.connect(self.on_click_frequency)
            self.right_buttons_frequency.append(button)

            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            button.clicked.connect(self.on_click_am_percentage)
            self.right_buttons_am_deepness.append(button)

            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            button.clicked.connect(self.on_click_fm_percentage)
            self.right_buttons_fm_deepness.append(button)

            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            button.clicked.connect(self.on_click_modulation)
            self.right_buttons_modulation.append(button)

            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            button.clicked.connect(self.on_click_fm_phase)
            self.right_buttons_fm_phase.append(button)

            button = QPushButton("  +   ")
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setObjectName("Parameter")
            button.clicked.connect(self.on_click_amplitude)
            self.right_buttons_amplitude.append(button)

            # Right labels
            self.right_carrier_frequency_label = QLabel("Carrier Frequency: ")
            self.right_carrier_frequency_label.setProperty("UseSeparator", True)
            self.right_carrier_frequency_label.setProperty("SettingsLabel", True)

            self.right_modulation_label = QLabel("Modulation: ")
            self.right_modulation_label.setProperty("UseSeparator", True)
            self.right_modulation_label.setProperty("SettingsLabel", True)

            self.right_am_percentage_label = QLabel("AM Percentage: ")
            self.right_am_percentage_label.setProperty("UseSeparator", True)
            self.right_am_percentage_label.setProperty("SettingsLabel", True)

            self.right_fm_percentage_label = QLabel("FM Percentage: ")
            self.right_fm_percentage_label.setProperty("UseSeparator", True)
            self.right_fm_percentage_label.setProperty("SettingsLabel", True)

            self.right_fm_phase_label = QLabel("FM Phase: ")
            self.right_fm_phase_label.setProperty("UseSeparator", True)
            self.right_fm_phase_label.setProperty("SettingsLabel", True)

            self.right_amplitude_label = QLabel("Amplitude: ")
            self.right_amplitude_label.setProperty("UseSeparator", True)
            self.right_amplitude_label.setProperty("SettingsLabel", True)

            # Left labels
            self.left_carrier_frequency_label = QLabel("Carrier Frequency: ")
            self.left_carrier_frequency_label.setProperty("UseSeparator", True)
            self.left_carrier_frequency_label.setProperty("SettingsLabel", True)

            self.left_modulation_label = QLabel("Modulation: ")
            self.left_modulation_label.setProperty("UseSeparator", True)
            self.left_modulation_label.setProperty("SettingsLabel", True)

            self.left_am_percentage_label = QLabel("AM Percentage: ")
            self.left_am_percentage_label.setProperty("UseSeparator", True)
            self.left_am_percentage_label.setProperty("SettingsLabel", True)

            self.left_fm_percentage_label = QLabel("FM Percentage: ")
            self.left_fm_percentage_label.setProperty("UseSeparator", True)
            self.left_fm_percentage_label.setProperty("SettingsLabel", True)

            self.left_fm_phase_label = QLabel("FM Phase: ")
            self.left_fm_phase_label.setProperty("UseSeparator", True)
            self.left_fm_phase_label.setProperty("SettingsLabel", True)

            self.left_amplitude_label = QLabel("Amplitude: ")
            self.left_amplitude_label.setProperty("UseSeparator", True)
            self.left_amplitude_label.setProperty("SettingsLabel", True)

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize ui elements
        :return: None
        """

        self.left_group.setLayout(self.left_layout)
        self.left_group.setTitle("Left Ear")
        self.left_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.right_group.setLayout(self.right_layout)
        self.right_group.setTitle("Right Ear")
        self.right_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.left_layout.setSpacing(0)  # Set left layout spacing as zero

        self.enable_right.setChecked(True)
        self.enable_right.stateChanged.connect(self.change_check)

        self.enable_left.setChecked(True)
        self.enable_left.stateChanged.connect(self.change_check)

        # Add the check boxes
        self.left_layout.addWidget(self.enable_left, 0, 0)
        self.right_layout.addWidget(self.enable_right, 0, 0)

        # Add the labels and initial buttons from the left side to left_layout
        self.left_layout.addWidget(self.left_carrier_frequency_label, 1, 0)
        self.left_layout.addWidget(self.left_modulation_label, 2, 0)
        self.left_layout.addWidget(self.left_am_percentage_label, 3, 0)
        self.left_layout.addWidget(self.left_fm_percentage_label, 4, 0)
        self.left_layout.addWidget(self.left_fm_phase_label, 5, 0)
        self.left_layout.addWidget(self.left_amplitude_label, 6, 0)

        for i in range(4):
            self.left_layout.addWidget(self.left_components[i], 0, i+1)
            self.left_layout.addWidget(self.left_buttons_frequency[i], 1, i+1)
            self.left_layout.addWidget(self.left_buttons_modulation[i], 2, i+1)
            self.left_layout.addWidget(self.left_buttons_am_deepness[i], 3, i+1)
            self.left_layout.addWidget(self.left_buttons_fm_deepness[i], 4, i+1)
            self.left_layout.addWidget(self.left_buttons_fm_phase[i], 5, i+1)
            self.left_layout.addWidget(self.left_buttons_amplitude[i], 6, i+1)
            self.left_layout.addWidget(QWidget(self, flags=Qt.Widget), 7, i+1)

        self.right_layout.setSpacing(0)  # Set right layout spacing as zero

        # Add the labels and initial buttons from the right side to right_layout
        self.right_layout.addWidget(self.right_carrier_frequency_label, 1, 0)
        self.right_layout.addWidget(self.right_modulation_label, 2, 0)
        self.right_layout.addWidget(self.right_am_percentage_label, 3, 0)
        self.right_layout.addWidget(self.right_fm_percentage_label, 4, 0)
        self.right_layout.addWidget(self.right_fm_phase_label, 5, 0)
        self.right_layout.addWidget(self.right_amplitude_label, 6, 0)

        for i in range(4):
            self.right_layout.addWidget(self.right_components[i], 0, i+1)
            self.right_layout.addWidget(self.right_buttons_frequency[i], 1, i+1)
            self.right_layout.addWidget(self.right_buttons_modulation[i], 2, i+1)
            self.right_layout.addWidget(self.right_buttons_am_deepness[i], 3, i+1)
            self.right_layout.addWidget(self.right_buttons_fm_deepness[i], 4, i+1)
            self.right_layout.addWidget(self.right_buttons_fm_phase[i], 5, i+1)
            self.right_layout.addWidget(self.right_buttons_amplitude[i], 6, i+1)
            self.right_layout.addWidget(QWidget(self, flags=Qt.Widget), 7, i+1)

        # Add right and left layout to horizontal layout
        self.horizontal_layout.addWidget(self.left_group, alignment=Qt.AlignLeft)
        self.horizontal_layout.addWidget(self.right_group, alignment=Qt.AlignLeft)

        # Add previews to their layouts
        self.preview_fft_layout.addWidget(self.preview_fft_left, alignment=Qt.AlignCenter)
        self.preview_fft_layout.addWidget(self.preview_fft_right, alignment=Qt.AlignCenter)
        self.preview_expected_layout.addWidget(self.preview_expected_left, alignment=Qt.AlignCenter)
        self.preview_expected_layout.addWidget(self.preview_expected_right, alignment=Qt.AlignCenter)

        self.vertical_layout.addLayout(self.horizontal_layout)
        self.vertical_layout.addLayout(self.preview_fft_layout)
        self.vertical_layout.addLayout(self.preview_expected_layout)
        self.vertical_layout.addStretch()
        # Set self layout as horizontal_layout
        self.setLayout(self.vertical_layout)

        self.show()  # Set self visible

    def on_click_frequency(self):
        """
        When the frequency button is clicked, this method will be called.
        OBS.: When the mouse leaves the pop-up window, the pop-up will close itself.
        :return: None
        """
        btn = self.sender()  # Gets the button responsible for the call
        FrequencyPicker(btn)  # Calls the pop-up value picker

    def on_click_modulation(self):
        btn = self.sender()
        ModulationPicker(btn)

    def on_click_am_percentage(self):
        btn = self.sender()
        AMPercentagePicker(btn)

    def on_click_fm_percentage(self):
        btn = self.sender()
        FMPercentagePicker(btn)

    def on_click_fm_phase(self):
        btn = self.sender()
        FMPhasePicker(btn)

    def on_click_amplitude(self):
        btn = self.sender()
        AmplitudePicker(btn)

    def test_event(self):
        print(self.right_group.size())

    def resizeEvent(self, e):

        self.left_group.resize(self.size().width() / 2 - 10, self.left_group.size().height())
        self.left_group.setMaximumWidth(self.width() / 2 - 10)

        self.right_group.resize(self.size().width() / 2 - 10, self.right_group.size().height())
        self.right_group.setMaximumWidth(self.width() / 2 - 10)

    def change_check(self):
        check = self.sender()
        if check is self.enable_left:
            if not self.enable_left.checkState():
                for b1, b2, b3, b4, b5, b6 in zip(self.left_buttons_frequency, self.left_buttons_amplitude,
                                                  self.left_buttons_fm_phase, self.left_buttons_fm_deepness,
                                                  self.left_buttons_am_deepness, self.left_buttons_modulation):

                    b1.setDisabled(True)
                    b2.setDisabled(True)
                    b3.setDisabled(True)
                    b4.setDisabled(True)
                    b5.setDisabled(True)
                    b6.setDisabled(True)

            else:
                for b1, b2, b3, b4, b5, b6 in zip(self.left_buttons_frequency, self.left_buttons_amplitude,
                                                  self.left_buttons_fm_phase, self.left_buttons_fm_deepness,
                                                  self.left_buttons_am_deepness, self.left_buttons_modulation):
                    b1.setDisabled(False)
                    b2.setDisabled(False)
                    b3.setDisabled(False)
                    b4.setDisabled(False)
                    b5.setDisabled(False)
                    b6.setDisabled(False)

        elif check is self.enable_right:
            if not self.enable_right.checkState():
                for b1, b2, b3, b4, b5, b6 in zip(self.right_buttons_frequency, self.right_buttons_amplitude,
                                                  self.right_buttons_fm_phase, self.right_buttons_fm_deepness,
                                                  self.right_buttons_am_deepness, self.right_buttons_modulation):

                    b1.setDisabled(True)
                    b2.setDisabled(True)
                    b3.setDisabled(True)
                    b4.setDisabled(True)
                    b5.setDisabled(True)
                    b6.setDisabled(True)

            else:
                for b1, b2, b3, b4, b5, b6 in zip(self.right_buttons_frequency, self.right_buttons_amplitude,
                                                  self.right_buttons_fm_phase, self.right_buttons_fm_deepness,
                                                  self.right_buttons_am_deepness, self.right_buttons_modulation):
                    b1.setDisabled(False)
                    b2.setDisabled(False)
                    b3.setDisabled(False)
                    b4.setDisabled(False)
                    b5.setDisabled(False)
                    b6.setDisabled(False)


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

        desktop = QDesktopWidget()
        self.setMaximumSize(desktop.size())
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
