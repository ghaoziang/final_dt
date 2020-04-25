from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import os
import sys
from app.analyzer import ECGAnalyzer

ecg_path = "/home/gaoziang/databox/raw_ecg/"


class ECGWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 300, 400, 300)
        self.setWindowTitle('ECG Databox')

        self.selected_file = None
        self.list_file = QListWidget(self)
        self.list_file.clicked.connect(self.select_file_click)
        for filename in os.listdir(ecg_path):
            if filename.endswith(".csv"):
                new_ecg = QListWidgetItem(os.path.basename(filename))
                self.list_file.addItem(new_ecg)

        self.delete_button = QPushButton("&Delete")
        self.delete_button.clicked.connect(self.delete_click)
        self.refresh_button = QPushButton("&Refresh")
        self.refresh_button.clicked.connect(self.refresh_click)
        self.analyze_button = QPushButton("&Analyze")
        self.analyze_button.clicked.connect(self.analyze_click)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.list_file, 0, 0, 3, 3, Qt.AlignCenter)
        self.layout.addWidget(self.delete_button, 0, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.refresh_button, 1, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.analyze_button, 2, 3, 1, 1, Qt.AlignCenter)

    def select_file_click(self):
        current_file = self.list_file.currentItem()
        self.selected_file = os.path.join(ecg_path, current_file.text())
        print(self.selected_file)

    def delete_click(self):
        print("Delete ECG HR file")
        if self.selected_file is None:
            return
        os.remove(self.selected_file)
        self.refresh_click()

    def refresh_click(self):
        print("Refresh ECG Space")
        self.list_file.clear()
        for filename in os.listdir(ecg_path):
            if filename.endswith(".csv"):
                new_ecg = QListWidgetItem(os.path.basename(filename))
                self.list_file.addItem(new_ecg)

    def analyze_click(self):
        print("Analyze ECG file")
        analyzer = ECGAnalyzer()
        analyzer.process_input(self.selected_file)
        labels, info = analyzer.analyze()
        m_box = QMessageBox()
        m_box.setText(info)
        m_box.exec()

