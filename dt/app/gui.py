
import sys
from app.fitbit_gui import *
from app.ecg_gui import *
from app.polar_gui import PolarWindow
import os

config_path = os.path.join(os.getcwd(), "device_config")
ecg_path = "/home/databox/raw_ecg/"
polar_path = "/home/databox/polar_h10/"
fitbit_path = "/home/databox/fitbit/"


class InitWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 300, 400, 300)
        self.setWindowTitle('Databox')

        # Add a label with tooltip
        self.label = QLabel(self)
        self.label.setText('Welcome to Databox!')
        self.label.setToolTip("This is a <b>QLabel</b> widget with Tooltip")

        # Add ECG Button
        self.ecg_button = QPushButton("&ECG")
        self.ecg_button.clicked.connect(self.ecg_button_click)

        # Add Polar H10 Button
        self.polar_button = QPushButton("&Polar H10")
        self.polar_button.clicked.connect(self.polar_button_click)

        # Add Fitbit Button
        self.fitbit_button = QPushButton("&Fitbit")
        self.fitbit_button.clicked.connect(self.fitbit_button_click)

        # Add main Layout
        main_layout = QGridLayout(self)
        main_layout.addWidget(self.label, 0, 1, 1, 2, Qt.AlignCenter)
        main_layout.addWidget(self.ecg_button, 1, 1, 2, 2)
        main_layout.addWidget(self.polar_button, 2, 1, 2, 2)
        main_layout.addWidget(self.fitbit_button, 3, 1, 2, 2)

    def ecg_button_click(self):
        print("ECG Button Click")
        ew = ECGWindow()
        ew.show()
        ew.exec_()

    def polar_button_click(self):
        print("Polar Button Click")
        pw = PolarWindow()
        pw.show()
        pw.exec_()

    def fitbit_button_click(self):
        print("Fitbit Button Click")
        fw = FitbitWindow()
        fw.show()
        fw.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Build the window widget
    w = InitWindow()
    # Show window and run
    w.show()
    app.exec_()