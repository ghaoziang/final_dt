import csv
import app.gather_keys_oauth2 as Oauth2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import os
import fitbit
from app.utils import load_config
import datetime
import pandas as pd
from app.analyzer import HRAnalyzer
import sys

config_path = os.path.join(os.path.pardir, "device_config")
ecg_path = "/home/gaoziang/databox/raw_ecg/"
polar_path = "/home/gaoziang/databox/polar_h10/"
fitbit_path = "/home/gaoziang/databox/fitbit/"


class FitbitClientWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 300, 400, 300)
        self.setWindowTitle('Fitbit Client Creation')

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
        with open(os.path.join(config_path, 'fit_config.yml'), 'w') as file:
            file.write('client_id: ' + self.id_str + '\n')
            file.write('client_secret: ' + self.secret_str + '\n')
            file.close()
        self.close()

    def cancel_button_click(self):
        print("Cancel Creation !")
        self.close()


class TimeInfoWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 300, 400, 300)
        self.setWindowTitle('Sleep Time Info')

        # Labels
        self.start_time = QLabel(self)
        self.start_time.setText("Start Time")
        self.end_time = QLabel(self)
        self.end_time.setText("End Time")
        self.start_minute = QLabel(self)
        self.start_minute.setText("Minute: ")
        self.end_minute = QLabel(self)
        self.end_minute.setText("Minute: ")
        self.start_hour = QLabel(self)
        self.start_hour.setText("Hour: ")
        self.end_hour = QLabel(self)
        self.end_hour.setText("Hour: ")
        self.start_day = QLabel(self)
        self.start_day.setText("Day: ")
        self.end_day = QLabel(self)
        self.end_day.setText("Day: ")
        self.start_month = QLabel(self)
        self.start_month.setText("Month: ")
        self.end_month = QLabel(self)
        self.end_month.setText("Month: ")
        self.start_year = QLabel(self)
        self.start_year.setText("Year: ")
        self.end_year = QLabel(self)
        self.end_year.setText("Year: ")

        # Entries
        self.start_minute_text = QLineEdit(self)
        self.end_minute_text = QLineEdit(self)
        self.start_hour_text = QLineEdit(self)
        self.end_hour_text = QLineEdit(self)
        self.start_day_text = QLineEdit(self)
        self.end_day_text = QLineEdit(self)
        self.start_month_text = QLineEdit(self)
        self.end_month_text = QLineEdit(self)
        self.start_year_text = QLineEdit(self)
        self.end_year_text = QLineEdit(self)

        # Buttons
        self.ok_button = QPushButton("&OK")
        self.ok_button.clicked.connect(self.upload_fitbit_data)
        self.cancel_button = QPushButton("&Cancel")
        self.cancel_button.clicked.connect(self.cancel)

        # Layout
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.start_time, 0, 0, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.end_time, 0, 2, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.start_minute, 1, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.start_minute_text, 1, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.end_minute, 1, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.end_minute_text, 1, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.start_hour, 2, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.start_hour_text, 2, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.end_hour, 2, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.end_hour_text, 2, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.start_day, 3, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.start_day_text, 3, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.end_day, 3, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.end_day_text, 3, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.start_month, 4, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.start_month_text, 4, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.end_month, 4, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.end_month_text, 4, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.start_year, 5, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.start_year_text, 5, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.end_year, 5, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.end_year_text, 5, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.ok_button, 6, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.cancel_button, 6, 2, 1, 1, Qt.AlignCenter)

    def upload_fitbit_data(self):
        print("Upload Fitbit Data")
        config = load_config(os.path.join(config_path, 'fit_config.yml'))
        c_id = config.get('client_id')
        c_secret = config.get('client_secret')

        server = Oauth2.OAuth2Server(c_id, c_secret)
        server.browser_authorize()
        ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
        REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
        auth2_client = fitbit.Fitbit(c_id, c_secret, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

        start_date = datetime.date(int(self.start_year_text.text()), int(self.start_month_text.text()),
                                   int(self.start_day_text.text()))
        end_date = datetime.date(int(self.end_year_text.text()), int(self.end_month_text.text()),
                                 int(self.end_day_text.text()))
        start_time = datetime.time(int(self.start_hour_text.text()), int(self.start_minute_text.text()))
        end_time = datetime.time(int(self.end_hour_text.text()), int(self.end_minute_text.text()))
        dic_list = list()
        if start_date == end_date:
            fit_statshr = auth2_client.intraday_time_series('activities/heart', base_date=start_date,
                                                            detail_level='1sec', start_time=start_time,
                                                            end_time=end_time)
            dic_list = fit_statshr['activities-heart-intraday']['dataset']
            dic_list = self.fill_list(dic_list, start_time, end_time, start_date)
        else:
            last_time = datetime.time(hour=23, minute=59)
            fit_statshr1 = auth2_client.intraday_time_series('activities/heart', base_date=start_date,
                                                             detail_level='1sec', start_time=start_time, end_time=last_time)
            early_time = datetime.time(hour=0, minute=0)
            fit_statshr2 = auth2_client.intraday_time_series('activities/heart', base_date=end_date,
                                                             detail_level='1sec', end_time=end_time, start_time=early_time)
            dic_list1 = fit_statshr1['activities-heart-intraday']['dataset']

            dic_list1 = self.fill_list(dic_list1, start_time, last_time, start_date)
            dic_list2 = fit_statshr2['activities-heart-intraday']['dataset']

            dic_list2 = self.fill_list(dic_list2, early_time, end_time, end_date)
            dic_list = dic_list1 + dic_list2

        file_name = os.path.join(fitbit_path, str(start_date) + '-' + str(start_time) +
                                 '_to_' + str(end_date) + '-' + str(end_time) + '.csv')
        with open(file_name, 'w') as f:
            w = csv.writer(f)
            w.writerow(["time", "value"])
            if len(dic_list) != 0:
                for dic in dic_list:
                    time = dic['time']
                    value = dic['value']
                    w.writerow([time, value])

        self.close()

    def cancel(self):
        self.close()

    def fill_list(self, dict_list, start_time, end_time, date):
        df = pd.DataFrame(dict_list)
        print(df)
        df.index = pd.to_datetime(date.strftime('%Y-%m-%d') + ' ' + df.time, format='%Y-%m-%d %H:%M:%S')
        start_ = pd.Timestamp(year=date.year, month=date.month, day=date.day,
                              hour=start_time.hour, minute=start_time.minute, second=0)
        end_ = pd.Timestamp(year=date.year, month=date.month, day=date.day,
                            hour=end_time.hour, minute=end_time.minute, second=0)
        ix = pd.date_range(freq='S', start=start_, end=end_)
        df = df.reindex(ix)
        df = df.drop(['time'], axis=1)
        new_df = self.fill_gap(df)
        new_df['time'] = new_df.index.to_native_types()
        new_list = new_df.to_dict('records')
        return new_list

    def fill_gap(self, frame):
        for i in range(len(frame)):
            v = frame.iloc[i, 0]
            count = 0
            if pd.isnull(v):
                j = i
                while pd.isnull(frame.iloc[j, 0]):
                    count = count + 1
                    j = j + 1
                    if j == len(frame):
                        break

                count = count + 1
                if j != len(frame):
                    e_v = frame.iloc[j, 0]
                    if i == 0:
                        frame.iloc[i, 0] = e_v
                    else:
                        s_v = frame.iloc[i-1, 0]
                        frame.iloc[i, 0] = (e_v-s_v)/count + s_v
                else:
                    if i == 0:
                        frame.iloc[i, 0] = 60
                    else:
                        s_v = frame.iloc[i-1, 0]
                        frame.iloc[i, 0] = s_v
        return frame


class FitbitWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 300, 400, 300)
        self.setWindowTitle('Fitbit Databox')

        self.selected_file = None
        self.list_file = QListWidget(self)
        self.list_file.clicked.connect(self.select_file_click)
        for filename in os.listdir(fitbit_path):
            if filename.endswith(".csv"):
                new_fitbit = QListWidgetItem(os.path.basename(filename))
                self.list_file.addItem(new_fitbit)

        # Fitbit Config
        fitbit_config = os.path.join(config_path, "fit_config.yml")
        if os.path.isfile(fitbit_config):
            print("Client has already existed")
        else:
            print("Create a Fitbit Client...")
            fcw = FitbitClientWindow()
            fcw.show()
            fcw.exec_()

        self.access_button = QPushButton("&Access Data")
        self.access_button.clicked.connect(self.access_click)
        self.delete_button = QPushButton("&Delete")
        self.delete_button.clicked.connect(self.delete_click)
        self.refresh_button = QPushButton("&Refresh")
        self.refresh_button.clicked.connect(self.refresh_click)
        self.analyze_button = QPushButton("&Analyze")
        self.analyze_button.clicked.connect(self.analyze_click)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.access_button, 0, 0, 1, 4, Qt.AlignCenter)
        self.layout.addWidget(self.list_file, 1, 0, 3, 3, Qt.AlignCenter)
        self.layout.addWidget(self.refresh_button, 1, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.delete_button, 2, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.analyze_button, 3, 3, 1, 1, Qt.AlignCenter)

    def access_click(self):
        print("Access Fitbit Data")
        if os.path.isfile(os.path.join(config_path, "fit_config.yml")):
            tw = TimeInfoWindow()
            tw.show()
            tw.exec_()
        else:
            box = QMessageBox()
            warning = QMessageBox.warning(box, "Lack Authorization", "Fitbit Client does not exist !",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def select_file_click(self):
        current_file = self.list_file.currentItem()
        self.selected_file = os.path.join(fitbit_path, current_file.text())
        print(self.selected_file)

    def delete_click(self):
        print("Delete Fitbit HR file")
        if self.selected_file is None:
            return
        os.remove(self.selected_file)
        self.refresh_click()

    def refresh_click(self):
        print("Refresh Fitbit Space")
        self.list_file.clear()
        for filename in os.listdir(fitbit_path):
            if filename.endswith(".csv"):
                new_fitbit = QListWidgetItem(os.path.basename(filename))
                self.list_file.addItem(new_fitbit)

    def analyze_click(self):
        print("Analyze Sleep Quality")
        analyzer = HRAnalyzer()
        analyzer.process_input(self.selected_file)
        labels, info = analyzer.analyze()
        print(labels)
        '''
        fname = "fitbit_" + os.path.basename(self.selected_file)
        print(fname)
        with open(fname, 'wb') as f:
            np.savetxt(f, labels, delimiter=' ', newline='\n', header='')
        '''
        m_box = QMessageBox()
        m_box.setText(info)
        m_box.exec()

