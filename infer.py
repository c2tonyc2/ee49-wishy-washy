import csv
from util import Vector3, dist
from collections import Counter


NUM_AMBIENT = 10
FIELDS = {
    "noise": [20, .05],
    "accelerometer-x": [.005, .2],
    "accelerometer-y": [.005, .2],
    "accelerometer-z": [.015, .4],
    "gyroscope-x": [1.5 , .05],
    "gyroscope-y": [1.5 , .05],
    "gyroscope-z": [1.5 , .05],
    "magnetometer-x": [1, 0],
    "magnetometer-y": [1, 0],
    "magnetometer-z": [1, 0],
    "temperature": [1, 0]
}
ambient = {field: 0 for field in FIELDS}


def check(field_key, value):
    if (abs(ambient[field_key] - float(value)) > FIELDS[field_key][0]):
        return FIELDS[field_key][1]
    return 0

def evaluate_ambient(ambient_points):
    for point in ambient_points:
        for field in FIELDS:
            ambient[field] += float(point[field])
    ambient.update((k, v / NUM_AMBIENT) for k, v in ambient.items())

def label_points(data_points):
    for point in data_points:
        a = [check(field, point[field]) for field in FIELDS]
        if sum(a) > .5:
            point['label'] = "ON"
        else:
            point['label'] = "OFF"

def infer_sheets_data(
    in_file="data/feeds-sheets.csv",
    out_file="data/feeds-sheets-labeled.csv"
):
    fieldnames = []
    data_points = []
    with open(in_file, 'r') as csvfile:
        laundry_data = csv.DictReader(csvfile)
        fieldnames = laundry_data.fieldnames

        data_points = list(laundry_data)
        evaluate_ambient(data_points[:NUM_AMBIENT])

    label_points(data_points)
    fieldnames.append('label')

    with open(out_file, 'w') as csvfile:
        labeled_data = csv.DictWriter(csvfile, fieldnames=fieldnames)
        labeled_data.writeheader()
        labeled_data.writerows(data_points)

if __name__ == '__main__':
    infer_sheets_data()
