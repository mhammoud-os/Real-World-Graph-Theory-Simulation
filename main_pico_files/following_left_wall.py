from driving_functions import *
from time import sleep, sleep_us, ticks_us,sleep_ms, ticks_diff
import math
led_onboard = machine.Pin(25, Pin.OUT)
led_onboard.value(1)
stop(1)
led_onboard.value(0)
passiveBuzzer = PWM(Pin(7))
passiveBuzzer.freq(5000)
passiveBuzzer.duty_u16(0)
def move_of_wall(wall):
    move('backward',30)
    if sensors['left'].value() and sensors['right'].value():
        return
    if wall == 'left':
        drive(1, start_speed['left'],1,0, 0.23)
    elif wall == 'right':
        drive(0, 0,1,start_speed['right'], 0.23)
    move('forward',75)
    move('backward',30)
    stop(0.5)
try:
    while True:
        drive(0, start_speed['left'],0,start_speed['right'], 0.15)
        if not sensors['down'].value():
            stop(0.3)
            if not sensors['down'].value():
                start = ticks_us()
                print('buss')
                while True:
                    current = ticks_us()
                    timer = ticks_diff(current, start)
                    if timer>8e6:
                        break
                    passiveBuzzer.duty_u16(8092)
                    for x in range(0, 36):
                        sinVal  = math.sin(x * 31.4 / 180)
                        toneVal = 2000+int(sinVal*700)
                        passiveBuzzer.freq(toneVal)
                        passiveBuzzer.duty_u16((1000+int(sinVal*900))*30)
                        sleep_ms(10)
                passiveBuzzer.duty_u16(0)
                break
        elif sensors['left'].value() and not sensors['forward'].value():
            stop(0.1)
            move('forward',50)
            move_of_wall('right')
            turn('left sharp')
            move('forward',20)
            continue
        elif sensors['left'].value():
            stop(0.5)
            move('forward',45)
            stop(0.1)
            if not sensors['forward'].value():
                move_of_wall('right')
                stop(0.1)
                turn('left')
                move('forward',20)
                continue
            else:
                move_of_wall('right')
                turn('left')
                move('forward',20)
                continue
        elif not sensors['forward'].value() and not sensors['right'].value() and not sensors['left'].value():
            stop(0.5)
            turn('back')
            continue
        elif not sensors['forward'].value():
            move_of_wall('left')
            stop(0.1)
            turn('right')
            move('forward',20)
            continue
        sleep(0.1)
except Exception as e:
    stop(1)
    file.write(str(e))
    print(e)
    file.flush()
    stop(1)
    print("error")
    motor1["pwm"].deinit()
    motor2["pwm"].deinit()
    passiveBuzzer.deinit()














