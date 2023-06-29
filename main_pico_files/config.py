from machine import Pin, PWM
from time import sleep, sleep_us, ticks_us, ticks_diff

from driving_functions import *

led_onboard = machine.Pin(25, Pin.OUT)
led_onboard.value(1)

stop(1)
led_onboard.value(0)
try:
    start = ticks_us()
    while True:
        drive(0, speed,0,speed, 0.1)
        if not sensors['forward'].value():
            stop(0)
            break    
    end = ticks_us()
    distance_travled_mm = 447
    speed_time = round((ticks_diff(end, start)/distance_travled_mm),4)
    print(speed_time)
    file = open("config.txt", "w")
    file.write(str(speed_time))
    file.flush()

    sleep(1)
    turn('right')
    turn('right')
    stop(1)
    for count in range(2):
        move('forward block',1)
        stop(0.5)
except Exception as Argument:
    error_file = open('error_log.txt','a+')
    error_file.write(str(Argument))
    error_file.flush()
    print(Argument)
    stop(1)
    print("error")
    reset()





