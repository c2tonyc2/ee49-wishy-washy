import json


with open("/flash/offset.txt", 'w') as out_file:
    out_file.write(json.dumps({
        "accel": 1,
        "gyro": 2,
        "mag": 3,
        "temp": 4,
    }))

with open("/flash/offset.txt", 'r') as in_file:
    print(in_file.read())
