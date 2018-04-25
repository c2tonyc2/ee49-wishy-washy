import csv
from collections import OrderedDict
import sheets


FIELD_NAME_MAP = OrderedDict([
    ('field1', 'noise'),
    ('field2', 'accelerometer'),
    ('field3', 'gyroscope'),
    ('field4', 'magnetometer'),
    ('field5', 'temperature')
])
VECTORS = set(['accelerometer', 'gyroscope', 'magnetometer'])

def get_vector_labels(label):
    return ["{0}-{1}".format(label, dim) for dim in ["x", "y", "z"]]

def format_labels(labels):
    """Converts list of labels from MQTT to specific names in
    Google Sheets
    """
    formatted_labels = []
    for label in labels:
        if label not in FIELD_NAME_MAP:
            formatted_labels.append(label)
        elif FIELD_NAME_MAP[label] not in VECTORS:
            formatted_labels.append(FIELD_NAME_MAP[label])
        else:
            formatted_labels += get_vector_labels(FIELD_NAME_MAP[label])
    return formatted_labels

def format_row(row):
    """Formats a keyed row into Google sheets format
    """
    formatted_row = []
    for field, value in row.items():
        if field not in FIELD_NAME_MAP or FIELD_NAME_MAP[field] not in VECTORS:
            formatted_row.append(value)
        else:
            formatted_row += [v for v in value.split(",")]
    return formatted_row

def mqtt_to_sheets(file="feeds.csv", sheets_name="ee49-feeds-2"):
    sheets_rows = []
    with open(file, 'r') as csvfile:
        laundry_data = csv.DictReader(csvfile)
        sheets_rows.append(format_labels(laundry_data.fieldnames))
        for row in laundry_data:
            sheets_rows.append(format_row(row))

    sheet_obj = sheets.init()
    sheets.create_sheet(sheet_obj, sheets_name)
    sheets.append_to_sheet(sheet_obj, sheets_name, sheets_rows)
    return

if __name__ == '__main__':
    mqtt_to_sheets()
