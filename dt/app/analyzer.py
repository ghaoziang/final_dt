import pickle
import os
import app.feature_extraction.ecg_extraction as extraction
from sklearn.preprocessing import normalize, StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import datetime


def convert_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return hours, mins, secs


def sleep_scoring(wake_percent, light_percent, deep_percent, rem_percent, sleep_time):
    points = 0
    if 10 <= wake_percent <= 15:
        points = points + 4
    elif 7.5 <= wake_percent < 10 or 15 < wake_percent <= 17.5:
        points = points + 3
    elif 5 <= wake_percent < 7.5 or 17.5 < wake_percent <= 20:
        points = points + 2
    elif 2.5 <= wake_percent < 5 or 20 < wake_percent <= 22.5:
        points = points + 1
    else:
        points = points + 0

    if 46.6 <= light_percent <= 53.3:
        points = points + 4
    elif 43.3 <= light_percent < 46.6 or 53.3 < light_percent <= 56.6:
        points = points + 3
    elif 40 <= light_percent < 43.3 or 56.6 < light_percent <= 60:
        points = points + 2
    elif 36.6 <= light_percent < 40 or 60 < light_percent <= 63.3:
        points = points + 1
    else:
        points = points + 0

    if 15.7 <= deep_percent <= 19.4:
        points = points + 4
    elif 13.9 <= deep_percent < 15.7 or 19.4 < deep_percent <= 21.3:
        points = points + 3
    elif 12 <= deep_percent < 13.9 or 21.3 < deep_percent <= 23:
        points = points + 2
    elif 10.2 <= deep_percent < 12 or 23 < deep_percent <= 24.8:
        points = points + 1
    else:
        points = points + 0

    if 18.3 <= rem_percent <= 21.7:
        points = points + 4
    elif 16.6 <= rem_percent < 18.3 or 21.7 < rem_percent <= 23.3:
        points = points + 3
    elif 15 <= rem_percent < 16.6 or 23.3 < rem_percent <= 25:
        points = points + 2
    elif 13.3 <= rem_percent < 15 or 25 < rem_percent <= 26.7:
        points = points + 1
    else:
        points = points + 0

    if 406 <= sleep_time <= 453:
        points = points + 4
    elif 383 <= sleep_time < 406 or 453 < sleep_time <= 476:
        points = points + 3
    elif 360 <= sleep_time < 383 or 476 < sleep_time <= 500:
        points = points + 2
    elif 337 <= sleep_time < 360 or 500 < sleep_time <= 523:
        points = points + 1
    else:
        points = points + 0

    print(points)
    if 0 <= points <= 5:
        return "Your sleep problems seem to be severe. You should try to get some help."
    elif 6 <= points <= 10:
        return "You have some sleep problems. " \
               "It is important to examine your sleep habits and see how you can make changes."
    elif 11 <= points <= 15:
        return "You sleep in good shape, but there are still many steps you can take to make it even better."
    else:
        return "You sleep in great shape, Keep doing what you are doing and spread the word!"


class ECGAnalyzer:
    def __init__(self):
        print("Using ECG analyzer")
        self.features = None
        self.model_path = os.path.join(os.getcwd(), 'models/ECG_classifier.pkl')
        with open(self.model_path, 'rb') as fid:
            self.model = pickle.load(fid)
        self.scalar_path = os.path.join(os.getcwd(), 'models/ecg_scalar.pkl')
        self.scalar = pickle.load(open(self.scalar_path, 'rb'))
        self.start_time = None

    def process_input(self, csv_file, time_length=30):
        print("Processing CSV to feature format")
        new_features = extraction.ecg_extract(csv_file, time_length)
        self.features = new_features
        print(self.features.shape)
        self.start_time = extraction.ecg_time_extract(csv_file)

    def analyze(self):
        if self.features is None:
            print("No Input Data")
            return
        model_input = self.features
        zero_indexes = np.all(model_input == 0, axis=1)
        model_input = model_input[~zero_indexes]
        model_input = np.nan_to_num(model_input)
        model_input = self.scalar.transform(model_input)
        model_input = normalize(model_input, axis=1)
        labels = self.model.predict(model_input)
        times = ["-" for x in range(len(labels))]
        for i in range(len(labels)):
            time = self.start_time + i * datetime.timedelta(seconds=30)
            times[i] = str(time.time())
        print(times)
        plt.fill_between(times, labels, where=(labels == 0), color='red', alpha=0.6, interpolate=True)
        plt.fill_between(times, labels, where=(labels == 1), color='yellow', alpha=0.3, interpolate=True)
        plt.fill_between(times, labels, where=(labels == 2), color='green', alpha=0.3, interpolate=True)
        plt.fill_between(times, labels, where=(labels == 3), color='blue', alpha=0.3, interpolate=True)
        plt.show()

        unique, count = np.unique(labels, return_counts=True)

        stages = []
        for item in unique:
            if item == 0:
                stages.append("Wake")
            elif item == 1:
                stages.append("Light Sleep")
            elif item == 2:
                stages.append("Deep Sleep")
            else:
                stages.append("REM")
        print(count)
        print(stages)
        print(unique)
        fig1, ax1 = plt.subplots()
        ax1.pie(count, labels=stages, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        plt.show()
        sleep_seconds = 0
        for i in range(len(unique)):
            sleep_seconds = sleep_seconds + count[i] * 30
        sleep_minutes = sleep_seconds / 60
        wake_percent = 0
        light_percent = 0
        deep_percent = 0
        rem_percent = 0
        sum_labels = sum(count)
        for i in range(len(unique)):
            if unique[i] == 0:
                wake_percent = (count[i] / sum_labels) * 100
            elif unique[i] == 1:
                light_percent = (count[i] / sum_labels) * 100
            elif unique[i] == 2:
                deep_percent = (count[i] / sum_labels) * 100
            elif unique[i] == 3:
                rem_percent = (count[i] / sum_labels) * 100

        quality_info = sleep_scoring(wake_percent,
                                     light_percent,
                                     deep_percent, rem_percent, sleep_minutes)

        return labels, quality_info


class HRAnalyzer:
    def __init__(self):
        print("Using HR analyzer")
        self.features = None
        self.model_path = os.path.join(os.getcwd(), 'models/HR_classifier.pkl')
        with open(self.model_path, 'rb') as fid:
            self.model = pickle.load(fid)
        self.scalar_path = os.path.join(os.getcwd(), 'models/hr_scalar.pkl')
        self.scalar = pickle.load(open(self.scalar_path, 'rb'))
        self.start_time = None

    def process_input(self, csv_file, time_length=30):
        print("Processing CSV to feature format")
        new_features = extraction.hr_extract(csv_file, time_length)
        self.features = new_features
        self.start_time = extraction.hr_time_extract(csv_file)

    def analyze(self):
        if self.features is None:
            print("No Input Data")
            return
        model_input = self.features
        zero_indexes = np.all(model_input == 0, axis=1)
        model_input = model_input[~zero_indexes]
        model_input = np.nan_to_num(model_input)
        model_input = self.scalar.transform(model_input)
        model_input = normalize(model_input, axis=1)
        labels = self.model.predict(model_input)
        print(labels.shape)
        times = ["-" for x in range(len(labels))]
        for i in range(len(labels)):
            time = self.start_time + i * datetime.timedelta(seconds=30)
            times[i] = str(time.time())
        plt.fill_between(times, labels, where=(labels == 0), color='red', alpha=0.6, interpolate=True)
        plt.fill_between(times, labels, where=(labels == 1), color='yellow', alpha=0.3, interpolate=True)
        plt.fill_between(times, labels, where=(labels == 2), color='green', alpha=0.3, interpolate=True)
        plt.fill_between(times, labels, where=(labels == 3), color='blue', alpha=0.3, interpolate=True)
        plt.show()

        unique, count = np.unique(labels, return_counts=True)

        stages = []
        for item in unique:
            if item == 0:
                stages.append("Wake")
            elif item == 1:
                stages.append("Light Sleep")
            elif item == 2:
                stages.append("Deep Sleep")
            else:
                stages.append("REM")
        print(count)
        print(stages)
        print(unique)
        fig1, ax1 = plt.subplots()
        ax1.pie(count, labels=stages, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        plt.show()
        sleep_seconds = 0
        for i in range(len(unique)):
            sleep_seconds = sleep_seconds + count[i] * 30
        for i in range(len(unique)):
            sleep_seconds = sleep_seconds + count[i] * 30
        sleep_minutes = sleep_seconds / 60
        wake_percent = 0
        light_percent = 0
        deep_percent = 0
        rem_percent = 0
        sum_labels = sum(count)
        for i in range(len(unique)):
            if unique[i] == 0:
                wake_percent = (count[i] / sum_labels) * 100
            elif unique[i] == 1:
                light_percent = (count[i] / sum_labels) * 100
            elif unique[i] == 2:
                deep_percent = (count[i] / sum_labels) * 100
            elif unique[i] == 3:
                rem_percent = (count[i] / sum_labels) * 100

        quality_info = sleep_scoring(wake_percent,
                                     light_percent,
                                     deep_percent, rem_percent, sleep_minutes)
        return labels, quality_info
