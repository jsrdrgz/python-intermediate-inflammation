"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains
inflammation data for a single patient taken over a number of days
and each column represents a single day across all patients.
"""

import numpy as np


def load_csv(filename):
    """Load a Numpy array from a CSV

    :param filename: Filename of CSV to load
    """
    return np.loadtxt(fname=filename, delimiter=',')


def daily_mean(data):
    """Calculate the daily mean of a 2D inflammation data array for each day.

    :param data: A 2D data array with inflammation data for individual patients for each day.
    :returns: An array of mean values of measurements for each day.
    """
    return np.mean(data, axis=0)


def daily_max(data):
    """Calculate the daily maximum of a 2D inflammation data array for each day.

    :param data: A 2D data array with inflammation data for individual patients for each day.
    :returns: An array of minimum values of measurements for each day.
    """
    return np.max(data, axis=0)


def daily_min(data):
    """Calculate the daily minimum of a 2D inflammation data array for each day.

    :param data: A 2D data array with inflammation data for individual patients for each day.
    :returns: An array of max values of measurements for each day.
    """
    return np.min(data, axis=0)

def patient_normalise(data):
    """Normalise patient data from a 2D inflammation data array.

    NaN values are ignored, and normalized to 0.

    Negative values are rounded to 0.
    """

    max_data = np.nanmax(data, axis=1)
    with np.errstate(invalid="ignore", divide='ignore'):
        normalised = data / max[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0
    normalised[normalised < 0] = 0
    return normalised

def attach_names(data, names):
    """Attach patient names to patient data"""
    assert len(data) == len(names)
    patient_info = []

    for data_row, name in zip(data, names):
        patient_info.append({'name': name,
                             'data': data_row})

    return patient_info

class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Patient(Person):
    def __init__(self, name):
        super().__init__(name)
        self.observations = []

    def add_observation(self, value, day=None):

        if day is None:

            try:
                day = self.observations[-1]['day'] + 1

            except IndexError:
                daya = 0

        new_observation = {
            'day': day,
            'value': value,
        }

        self.observations.append(new_observation)
        return new_observation

    @property
    def last_observation(self, ):
        return self.observations[-1]

    def __str__(self):
        return self.name

class Observation:

    def __init__(self, day, value):
        self.day = day
        self.value = value

    def __str__(self):
        return str(self.value)

class Doctor(Person):

    def __init__(self, name):
        super().__init__(name)
        self.patient_list = []

    def add_patient(self, new_patient):

        self.patient_list.append(new_patient)
        return new_patient


alice = Patient('Alice')
print(alice)

observation = alice.add_observation(3)
print(observation)
print(alice.observations)

obs = alice.last_observation
print(obs)

judy = Doctor('Judy')
judy.add_patient("Alice")
print(judy)
print(judy.patient_list)