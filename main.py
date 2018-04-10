from board import SDA, SCL, ADC6
from machine import Pin, Timer, ADC
from mpu9250 import MPU9250
from machine import I2C, SPI
from time import sleep


# MPU9250._chip_id = 115

# i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)
# imu = MPU9250(i2c)
#
# def imu_collect(timer):
#     print("accel: {0}".format(
#         str(imu.accel.z),
#     ))
#     return

# imu_timer = Timer(1)
# imu_timer.init(period=200, mode=Timer.PERIODIC, callback=imu_collect)

mic_adc = ADC(Pin(ADC6))
mic_adc.atten(ADC.ATTN_11DB)

for _ in range(100):
    print(mic_adc.read())
    sleep(1)
