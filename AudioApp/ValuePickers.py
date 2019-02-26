from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
                             QSizePolicy)
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


class CentralWidget(QWidget):

    def __init__(self, parent=None):

        super(CentralWidget, self).__init__(parent=parent, flags=Qt.Widget)

        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()

        self.label = QLabel("Choose the frequency value:")
        self.line = QLineEdit()

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_event)

        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.ok_event)

        self.init_ui()

    def init_ui(self):

        self.line.setMinimumWidth(self.label.width() / 3)
        self.ok_btn.setMinimumWidth(self.label.width()/6)
        self.cancel_btn.setMinimumWidth(self.label.width()/6)

        self.v_layout.addWidget(self.label, alignment=Qt.AlignHCenter)
        self.v_layout.addStretch(0)
        self.v_layout.addWidget(self.line, alignment=Qt.AlignHCenter)
        self.v_layout.addStretch(0)

        self.h_layout.addWidget(self.ok_btn, alignment=Qt.AlignHCenter)
        self.h_layout.addWidget(self.cancel_btn, alignment=Qt.AlignHCenter)

        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

        self.show()

    def ok_event(self):

        self.parent().ok = True
        self.parent().value = self.line.text()
        self.parent().close()

    def cancel_event(self):

        self.parent().ok = False
        self.parent().close()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Return:
            self.ok_event()
        elif e.key() == Qt.Key_Escape:
            self.cancel_event()


class FrequencyPicker(QMainWindow):

    def __init__(self, parent: QPushButton):

        super(FrequencyPicker, self).__init__(parent=parent, flags=Qt.Window)

        self.ok = False
        self.value = ""
        self.closed = False

        self.center_widget = CentralWidget(self)
        self.setCentralWidget(self.center_widget)

        self.x_pos = QCursor.pos().x() - 10
        self.y_pos = QCursor.pos().y() - 10

        self.init_ui()

    def init_ui(self):

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.move(self.x_pos, self.y_pos)
        self.resize(120, 80)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.show()

    def leaveEvent(self, e):

        self.close()

    def closeEvent(self, e):

        if self.ok and self.value is not "" and not self.closed:
            self.parent().setText(self.value)
            parent = self.parent().parent()
            parent.parent().preview_fft_left.plot()
            parent.parent().preview_fft_right.plot()
            parent.parent().preview_expected_left.plot()
            parent.parent().preview_expected_right.plot()
            self.closed = True
            e.accept()

        elif not self.ok:
            e.accept()

        else:
            e.ignore()


class ModulationCW(CentralWidget):

    def __init__(self, parent=None):

        super(ModulationCW, self).__init__(parent=parent)
        self.label.setText("Choose the modulation value:")


class ModulationPicker(QMainWindow):

    def __init__(self, parent: QPushButton):

        super(ModulationPicker, self).__init__(parent=parent, flags=Qt.Window)

        self.ok = False
        self.value = ""
        self.closed = False

        self.center_widget = ModulationCW(self)
        self.setCentralWidget(self.center_widget)

        self.x_pos = QCursor.pos().x() - 10
        self.y_pos = QCursor.pos().y() - 10

        self.init_ui()

    def init_ui(self):

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.move(self.x_pos, self.y_pos)
        self.resize(120, 80)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.show()

    def leaveEvent(self, e):

        self.close()

    def closeEvent(self, e):

        if self.ok and self.value is not "" and not self.closed:
            self.parent().setText(self.value)
            parent = self.parent().parent()
            parent.parent().preview_fft_left.plot()
            parent.parent().preview_fft_right.plot()
            parent.parent().preview_expected_left.plot()
            parent.parent().preview_expected_right.plot()
            self.closed = True
            e.accept()

        elif not self.ok:
            e.accept()

        else:
            e.ignore()


class AMPercentageCW(CentralWidget):

    def __init__(self, parent=None):

        super(AMPercentageCW, self).__init__(parent=parent)
        self.label.setText("Choose the AM percentage value:")


class AMPercentagePicker(QMainWindow):

    def __init__(self, parent: QPushButton):

        super(AMPercentagePicker, self).__init__(parent=parent, flags=Qt.Window)

        self.ok = False
        self.value = ""
        self.closed = False

        self.center_widget = AMPercentageCW(self)
        self.setCentralWidget(self.center_widget)

        self.x_pos = QCursor.pos().x() - 10
        self.y_pos = QCursor.pos().y() - 10

        self.init_ui()

    def init_ui(self):

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.move(self.x_pos, self.y_pos)
        self.resize(120, 80)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.show()

    def leaveEvent(self, e):

        self.close()

    def closeEvent(self, e):

        if self.ok and self.value is not "" and not self.closed:
            self.parent().setText(self.value)
            parent = self.parent().parent()
            parent.parent().preview_fft_left.plot()
            parent.parent().preview_fft_right.plot()
            parent.parent().preview_expected_left.plot()
            parent.parent().preview_expected_right.plot()
            self.closed = True
            e.accept()

        elif not self.ok:
            e.accept()

        else:
            e.ignore()


class FMPercentageCW(CentralWidget):

    def __init__(self, parent=None):

        super(FMPercentageCW, self).__init__(parent=parent)
        self.label.setText("Choose the FM percentage value:")


class FMPercentagePicker(QMainWindow):

    def __init__(self, parent: QPushButton):

        super(FMPercentagePicker, self).__init__(parent=parent, flags=Qt.Window)

        self.ok = False
        self.value = ""
        self.closed = False

        self.center_widget = FMPercentageCW(self)
        self.setCentralWidget(self.center_widget)

        self.x_pos = QCursor.pos().x() - 10
        self.y_pos = QCursor.pos().y() - 10

        self.init_ui()

    def init_ui(self):

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.move(self.x_pos, self.y_pos)
        self.resize(120, 80)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.show()

    def leaveEvent(self, e):

        self.close()

    def closeEvent(self, e):

        if self.ok and self.value is not "" and not self.closed:
            self.parent().setText(self.value)
            parent = self.parent().parent()
            parent.parent().preview_fft_left.plot()
            parent.parent().preview_fft_right.plot()
            parent.parent().preview_expected_left.plot()
            parent.parent().preview_expected_right.plot()
            self.closed = True
            e.accept()

        elif not self.ok:
            e.accept()

        else:
            e.ignore()


class FMPhaseCW(CentralWidget):

    def __init__(self, parent=None):

        super(FMPhaseCW, self).__init__(parent=parent)
        self.label.setText("Choose the FM phase value:")


class FMPhasePicker(QMainWindow):

    def __init__(self, parent: QPushButton):

        super(FMPhasePicker, self).__init__(parent=parent, flags=Qt.Window)

        self.ok = False
        self.value = ""
        self.closed = False

        self.center_widget = FMPercentageCW(self)
        self.setCentralWidget(self.center_widget)

        self.x_pos = QCursor.pos().x() - 10
        self.y_pos = QCursor.pos().y() - 10

        self.init_ui()

    def init_ui(self):

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.move(self.x_pos, self.y_pos)
        self.resize(120, 80)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.show()

    def leaveEvent(self, e):

        self.close()

    def closeEvent(self, e):

        if self.ok and self.value is not "" and not self.closed:
            self.parent().setText(self.value)
            parent = self.parent().parent()
            parent.parent().preview_fft_left.plot()
            parent.parent().preview_fft_right.plot()
            parent.parent().preview_expected_left.plot()
            parent.parent().preview_expected_right.plot()
            self.closed = True
            e.accept()

        elif not self.ok:
            e.accept()

        else:
            e.ignore()


class AmplitudeCW(CentralWidget):

    def __init__(self, parent=None):

        super(AmplitudeCW, self).__init__(parent=parent)
        self.label.setText("Choose the Amplitude value:")


class AmplitudePicker(QMainWindow):

    def __init__(self, parent: QPushButton):

        super(AmplitudePicker, self).__init__(parent=parent, flags=Qt.Window)

        self.ok = False
        self.value = ""
        self.closed = False

        self.center_widget = FMPercentageCW(self)
        self.setCentralWidget(self.center_widget)

        self.x_pos = QCursor.pos().x() - 10
        self.y_pos = QCursor.pos().y() - 10

        self.init_ui()

    def init_ui(self):

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.move(self.x_pos, self.y_pos)
        self.resize(120, 80)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.show()

    def leaveEvent(self, e):

        self.close()

    def closeEvent(self, e):

        if self.ok and self.value is not "" and not self.closed:
            self.parent().setText(self.value)
            parent = self.parent().parent()
            parent.parent().preview_fft_left.plot()
            parent.parent().preview_fft_right.plot()
            parent.parent().preview_expected_left.plot()
            parent.parent().preview_expected_right.plot()
            self.closed = True
            e.accept()

        elif not self.ok:
            e.accept()

        else:
            e.ignore()
