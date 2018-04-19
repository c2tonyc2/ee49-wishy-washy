from board import SDA, SCL, ADC6
from machine import Pin, Timer, ADC
from mpu9250 import MPU9250
from machine import I2C, SPI
from time import sleep
from mqttclient import MQTTClient
from network import WLAN, STA_IF


MPU9250._chip_id = 115
BATCH_SIZE = 100
CALIBRATION_SIZE = 100
DATA_FREQUENCY = 60000 # Data collection frequency in ms
SEND_TIME = 5 # time in s to wait for a MQTT message to go out
BROKER = "mqtt.thingspeak.com"
TS_CHANNEL_ID = "472546"
TS_WRITE_KEY = "TQ6PXDYGOSXZV2XA"
OFFSETS = {}
SCALARS = set(["noise", "temp"])

class Vector3(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, imu_vector):
        return Vector3(
            x=self.x + imu_vector.x,
            y=self.y + imu_vector.y,
            z=self.z + imu_vector.z
        )

    def __sub__(self, imu_vector):
        return Vector3(
            x=self.x - imu_vector.x,
            y=self.y - imu_vector.y,
            z=self.z - imu_vector.z
        )

    def __truediv__(self, sample_num):
        return Vector3(
            x=self.x / sample_num,
            y=self.y / sample_num,
            z=self.z / sample_num
        )

    def dist(self, imu_vector):
        return Vector3(
            x=abs(self.x - imu_vector.x),
            y=abs(self.y - imu_vector.y),
            z=abs(self.z - imu_vector.z)
        )

    def __str__(self):
        return "{0},{1},{2}".format(self.x, self.y, self.z)

    @classmethod
    def from_imu_vector(cls, imu_vector):
        return cls(imu_vector[0], imu_vector[1], imu_vector[2])

print("Connecting to broker", BROKER, "...")
mqtt = MQTTClient(BROKER, user=None, password=None, ssl=True)
print("MQQTClient Connected!")

i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)
imu = MPU9250(i2c)

def dist(curr, key):
    if key in SCALARS:
        return abs(curr - OFFSETS[key])
    else:
        return Vector3(
            x=abs(curr.x - OFFSETS[key].x),
            y=abs(curr.y - OFFSETS[key].y),
            z=abs(curr.z - OFFSETS[key].z)
        )


def imu_collect():
    return {
        "accel": Vector3.from_imu_vector(imu.accel.xyz),
        "gyro": Vector3.from_imu_vector(imu.gyro.xyz),
        "mag": Vector3.from_imu_vector(imu.mag.xyz),
        "temp": imu.temperature
    }

mic_adc = ADC(Pin(ADC6))
mic_adc.atten(ADC.ATTN_11DB)

def calibrate():
    print("calibrating...")
    total_noise = 0
    total_temp = 0
    total_accel = Vector3()
    total_gyro = Vector3()
    total_mag = Vector3()
    for _ in range(CALIBRATION_SIZE):
        total_noise += mic_adc.read()
        imu_values = imu_collect()
        total_accel += imu_values["accel"]
        total_gyro += imu_values["gyro"]
        total_mag += imu_values["mag"]
        total_temp += imu_values["temp"]
    OFFSETS["noise"] = total_noise/CALIBRATION_SIZE
    OFFSETS["accel"] = total_accel/CALIBRATION_SIZE
    OFFSETS["gyro"] = total_gyro/CALIBRATION_SIZE
    OFFSETS["mag"] = total_mag/CALIBRATION_SIZE
    OFFSETS["temp"] = total_temp/CALIBRATION_SIZE
    print("offsets...")
    for key, offset in OFFSETS.items():
        print("{0}: {1}".format(key, offset))
    sleep(10)

def collect_data(timer):
    nose_avg = 0
    imu_values_avg = {
        "accel": Vector3(),
        "gyro": Vector3(),
        "mag": Vector3(),
        "temp": 0
    }
    print("collecting data ... ")
    for i in range(BATCH_SIZE):
        value = abs(mic_adc.read() - OFFSETS["noise"])
        nose_avg += dist(mic_adc.read(), "noise")

        imu_values = imu_collect()
        imu_values_avg.update(
            (k, v + dist(imu_values[k], k))
            for k, v in imu_values_avg.items()
        )

    nose_avg = nose_avg/BATCH_SIZE
    imu_values_avg.update((k, v / BATCH_SIZE) for k, v in imu_values_avg.items())

    topic = "channels/" + TS_CHANNEL_ID + "/publish/" + TS_WRITE_KEY
    message = "field1={}&field2={}&field3={}&field4={}&field5={}".format(
        nose_avg,
        imu_values_avg["accel"],
        imu_values["gyro"],
        imu_values["mag"],
        imu_values_avg["temp"]
    )
    mqtt.publish(topic, message)
    sleep(SEND_TIME)

calibrate()
data_timer = Timer(0)
data_timer.init(
    period=DATA_FREQUENCY,
    mode=Timer.PERIODIC,
    callback=collect_data
)
