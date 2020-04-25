import datetime
import numpy as np
import pyeeg
import math


def ecg_time_extract(file_path):
    times = np.genfromtxt(file_path, dtype=str, delimiter=',', usecols=(0,), skip_header=True)
    start = times[1]
    time_str = datetime.datetime.strptime(start, "'[%H:%M:%S.%f %d/%m/%Y]'")
    return time_str


def hr_time_extract(file_path):
    times = np.genfromtxt(file_path, dtype=str, delimiter=',', usecols=(0,), skip_header=True)
    start = times[0]
    print(start)
    time_str = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    return time_str


def kfd(ecg):
    result = (math.log(ecg.shape[0]))
    par = math.log(np.max(np.sqrt(np.power(ecg-ecg[0], 2) + np.power(np.arange(ecg.shape[0]), 2)))/np.sum(np.sqrt(np.power(np.diff(ecg), 2)+1)))
    result = result/(result+par)
    return result


def ecg_extract(file_path, time_length):
    ecg_mat = np.genfromtxt(file_path, dtype=float, delimiter=',', usecols=(1,), skip_header=True)
    num = ecg_mat.shape[0]
    col = time_length*250
    row = int(num / col)

    ecg_mat = ecg_mat[1:row*col+1].reshape(row, col)
    num_row = ecg_mat.shape[0]

    result = np.zeros((num_row, 5))

    for i in range(num_row):
        ecg = ecg_mat[i, :]
        if np.any(np.isnan(ecg)):
            indices = np.where(np.isnan(ecg))[0]
            for j in indices:
                ecg[j] = ecg[j - 1]

        power = np.sum(np.power(ecg, 4))
        k = kfd(ecg)
        hjm = pyeeg.hjorth(ecg)
        pfd = pyeeg.pfd(ecg)

        result[i, 0] = power
        result[i, 1] = k
        result[i, 2] = hjm[0]
        result[i, 3] = hjm[1]
        result[i, 4] = pfd
    return result


def hr_extract(file_path, time_length):
    hr_mat = np.genfromtxt(file_path, dtype=float, delimiter=',', usecols=(1,), skip_header=True)
    num = hr_mat.shape[0]
    noise = np.random.normal(0, 1.1, num)
    hr_mat = hr_mat + noise
    col = time_length
    row = int(num / col)
    hr_mat = hr_mat[:row*col].reshape(row, col)
    num_row = hr_mat.shape[0]
    result = np.zeros((num_row, 5))

    for i in range(num_row):
        hr = hr_mat[i, :]
        if np.any(np.isnan(hr)):
            indices = np.where(np.isnan(hr))[0]
            for j in indices:
                hr[j] = hr[j - 1]

        power = np.sum(np.power(hr, 4))
        k = kfd(hr)
        hjm = pyeeg.hjorth(hr)
        pfd = pyeeg.pfd(hr)

        result[i, 0] = power
        result[i, 1] = k
        result[i, 2] = hjm[0]
        result[i, 3] = hjm[1]
        result[i, 4] = pfd

    result = result[:, 1:]
    return result








