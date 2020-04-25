import csv
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import os
import numpy as np
import app.authorization as au
from app.access_polar import PolarAccessLinkExample
from app.analyzer import HRAnalyzer
import sys

config_path = os.path.join(os.path.pardir, "device_config")
polar_path = "/home/gaoziang/databox/polar_h10/"


class PolarClientWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 300, 400, 300)
        self.setWindowTitle('Polar H10 Client')

        # Client Labels
        self.id_label = QLabel(self)
        self.secret_label = QLabel(self)
        self.id_label.setText("Client ID: ")
        self.secret_label.setText("Client Secret: ")

        # Client Info Entry
        self.id_text = QLineEdit(self)
        self.secret_text = QLineEdit(self)
        self.id_str = ""
        self.secret_str = ""

        # Client Buttons
        self.create_button = QPushButton("&OK")
        self.cancel_button = QPushButton("&Cancel")
        self.create_button.clicked.connect(self.create_button_click)
        self.cancel_button.clicked.connect(self.cancel_button_click)

        # Layout
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.id_label, 0, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.secret_label, 1, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.id_text, 0, 1, 1, 4, Qt.AlignCenter)
        self.layout.addWidget(self.secret_text, 1, 1, 1, 4, Qt.AlignCenter)
        self.layout.addWidget(self.create_button, 2, 1, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.cancel_button, 2, 3, 1, 2, Qt.AlignCenter)

    def create_button_click(self):
        print("Create Client !")
        self.id_str = self.id_text.text()
        self.secret_str = self.secret_text.text()
        print(self.id_str)
        print(self.secret_str)
        with open(os.path.join(config_path, 'config.yml'), 'w') as file:
            file.write('client_id: ' + self.id_str + '\n')
            file.write('client_secret: ' + self.secret_str + '\n')
            file.close()
        self.close()

    def cancel_button_click(self):
        print("Cancel Creation !")
        self.close()


class PolarWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 300, 400, 300)
        self.setWindowTitle('Polar H10 Databox')

        self.auth_button = QPushButton("&Authorize")
        self.auth_button.clicked.connect(self.auth_button_click)
        self.attach_button = QPushButton("&Attach New Exercises")
        self.attach_button.clicked.connect(self.attach_click)
        self.delete_button = QPushButton("&Delete")
        self.delete_button.clicked.connect(self.delete_click)
        self.refresh_button = QPushButton("&Refresh")
        self.refresh_button.clicked.connect(self.refresh_click)
        self.analyze_button = QPushButton("&Analyze")
        self.analyze_button.clicked.connect(self.analyze_click)

        self.selected_file = None
        self.list_file = QListWidget(self)
        self.list_file.clicked.connect(self.select_file_click)
        for filename in os.listdir(polar_path):
            if filename.endswith(".csv"):
                new_exercise = QListWidgetItem(os.path.basename(filename))
                self.list_file.addItem(new_exercise)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.auth_button, 0, 0, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.attach_button, 0, 2, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.list_file, 1, 0, 3, 3, Qt.AlignCenter)
        self.layout.addWidget(self.delete_button, 1, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.refresh_button, 2, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.analyze_button, 3, 3, 1, 1, Qt.AlignCenter)

    def auth_button_click(self):
        print("Get Polar Client Authorization")
        if os.path.isfile(os.path.join(config_path, "config.yml")):
            print(True)
            t = threading.Thread(target=au.auth)
            t.setDaemon(True)
            t.start()
        else:
            print(False)
            pcw = PolarClientWindow()
            pcw.show()
            pcw.exec_()

    def attach_click(self):
        print("Attach New Exercises in Polar H10")
        example = PolarAccessLinkExample()
        example.get_exercises_list()

    def delete_click(self):
        print("Delete Exercise")
        if self.selected_file is None:
            return
        os.remove(self.selected_file)
        self.refresh_click()

    def refresh_click(self):
        print("Refresh Polar Space")
        self.list_file.clear()
        for filename in os.listdir(polar_path):
            if filename.endswith(".csv") or filename.endswith(".CSV"):
                new_exercise = QListWidgetItem(os.path.basename(filename))
                self.list_file.addItem(new_exercise)

    def analyze_click(self):
        print("Analyze the Exercise")
        analyzer = HRAnalyzer()
        analyzer.process_input(self.selected_file)
        labels, info = analyzer.analyze()
        '''
        fname = "polar_" + os.path.basename(self.selected_file)
        print(fname)
        with open(fname, 'wb') as f:
            np.savetxt(f, labels, delimiter=' ', newline='\n', header='')
        '''
        m_box = QMessageBox()
        m_box.setText(info)
        m_box.exec()

    def select_file_click(self):
        current_file = self.list_file.currentItem()
        self.selected_file = os.path.join(polar_path, current_file.text())
        print(self.selected_file)
