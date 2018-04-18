from board import SDA, SCL, ADC6
from machine import Pin, Timer, ADC, deepsleep
from mpu9250 import MPU9250
from machine import I2C, SPI
from mqttclient import MQTTClient
from time import sleep


MPU9250._chip_id = 115
BATCH_SIZE = 10
CALIBRATION_SIZE = 1000
SLEEP_DURATION = 10000
SEND_TIME = 5
BROKER = "mqtt.thingspeak.com"
TS_CHANNEL_ID = "472546"
TS_WRITE_KEY = "TQ6PXDYGOSXZV2XA"
OFFSETS = {}

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

def imu_collect():
    return {
        "accel": Vector3.from_imu_vector(imu.accel.xyz),
        "gyro": Vector3.from_imu_vector(imu.gyro.xyz),
        "mag": Vector3.from_imu_vector(imu.mag.xyz),
        "temp": imu.temperature
    }

mic_adc = ADC(Pin(ADC6))
mic_adc.atten(ADC.ATTN_11DB)

def main():
    noise_avg = 0
    imu_values_avg = {
        "accel": Vector3(),
        "gyro": Vector3(),
        "mag": Vector3(),
        "temp": 0
    }
    print("collecting data ... ")
    for i in range(BATCH_SIZE):
        noise = mic_adc.read()
        noise_avg += noise

        imu_values = imu_collect()
        imu_values.update((k, v + imu_values[k]) for k, v in imu_values_avg.items())

    noise_avg = noise_avg/BATCH_SIZE
    imu_values_avg.update((k, v / BATCH_SIZE) for k, v in imu_values_avg.items())


    topic = "channels/" + TS_CHANNEL_ID + "/publish/" + TS_WRITE_KEY
    message = "field1={}&field2={}&field3={}&field4={}&field5={}".format(
        noise_avg,
        imu_values_avg["accel"],
        imu_values_avg["gyro"],
        imu_values_avg["mag"],
        imu_values_avg["temp"]
    )
    mqtt.publish(topic, message)
    sleep(SEND_TIME)
    deepsleep(SLEEP_DURATION)

main()
