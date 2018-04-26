import csv
from util import Vector3, dist
from collections import Counter


NUM_AMBIENT = 1
FIELDS = set([
    "noise",
    "accelerometer-x", "accelerometer-y", "accelerometer-z",
    "gyroscope-x", "gyroscope-y", "gyroscope-z",
    "magnetometer-x", "magnetometer-y", "magnetometer-z",
    "temperature"
])
ambient = {k: 0 for key in FIELDS}

def evaluate_ambient(ambient_points):
    for point in ambient_points:
        for field in FIELDS:
            ambient[field] += float(ambient_points[field])
    ambient.update((k, v / NUM_AMBIENT) for k, v in ambient.items())

def label_points(data_points):
    return

def infer_sheets_data(
    in_file="feeds-sheets.csv",
    out_file="feeds-sheets-labeled.csv"
):
    fieldnames = []
    data_points = []
    with open(in_file, 'r') as csvfile:
        laundry_data = csv.DictReader(csvfile)
        fieldnames = laundry_data.fieldnames

        data_points = list(laundry_data)
        evaluate_ambient(data_points[:NUM_AMBIENT])

    label_points(data_points)

    with open(out_file, 'w') as csvfile:
        labeled_data = csv.DictWriter(csvfile, fieldnames=fieldnames)
        labeled_data.writeheader()
        labeled_data.writerows(data_points)

if __name__ == '__main__':
    infer_sheets_data()
