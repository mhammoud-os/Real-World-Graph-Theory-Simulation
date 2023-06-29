from machine import Pin, PWM
from time import sleep, sleep_us
file = open("error_log.txt", "a+")

sensors = {'forward':Pin(0, Pin.IN),
           'right':Pin(1, Pin.IN),
           'left':Pin(2, Pin.IN),
           'down':Pin(3, Pin.IN)
           }
motor1={
    "in1 pin": Pin(15, Pin.OUT),
    "in2 pin": Pin(14, Pin.OUT),
    "pwm": PWM(Pin(12))    
}
motor1["pwm"].deinit()
motor1["pwm"].freq(110)

motor2={
    "in1 pin": Pin(17, Pin.OUT),
    "in2 pin": Pin(16, Pin.OUT),
    "pwm": PWM(Pin(22))
}
motor2["pwm"].deinit()
motor2["pwm"].freq(110)



#The absolute top speed is 65535
adjust = 0
speed = 55535

start_speed = {'left':speed,'right':speed-adjust}
#direction 0 = forward
def drive(direction1, speed1, direction2, speed2, sleep_sec):
    if direction1:
        motor1["in1 pin"].value(1)
        motor1["in2 pin"].value(0)
    else:
        motor1["in1 pin"].value(0)
        motor1["in2 pin"].value(1)
    
    if direction2:
        motor2["in1 pin"].value(1)
        motor2["in2 pin"].value(0)
    else:
        motor2["in1 pin"].value(0)
        motor2["in2 pin"].value(1)
        
    motor1["pwm"].duty_u16(speed1)
    motor2["pwm"].duty_u16(speed2)
    sleep(sleep_sec)
    
def stop(sec):
    drive(1,0,1,0,0)
    sleep(sec)

def turn(direction):
    speed_time = float(open('config.txt','r').readline())
    open('config.txt','r').close()
    wait_time = speed_time*100/(1e+6)
    if direction == "right":
        drive(1,0,0,speed, wait_time)
    elif direction == "left":
        drive(0, speed,1,0, wait_time)
    elif direction == "right sharp":
        drive(1,speed,0,speed, wait_time/2)
    elif direction == "left sharp":
        drive(0, speed,1,speed, wait_time/2)
    elif direction == "back":
        move('forward',140)
        stop(1)
        move('backward',200)
        stop(1)
        drive(0, start_speed['left']-3000,0,start_speed['right']+10000, 200*speed_time/1e+6)
        stop(0.5)
        drive(1,0,1,speed, wait_time)
        drive(1,0,1,speed, wait_time)
        drive(1,0,1,speed, wait_time)
        stop(0.5)
        move('backward',100)
        stop(0.5)
        drive(0, speed,1,0, wait_time)
        drive(0, speed,1,0, wait_time)

stop(1)
def move(direction,amount:int = 1):
    speed_time = float(open('config.txt','r').readline())
    open('config.txt','r').close()
    if direction == 'forward':
        drive(0, start_speed['left'],0,start_speed['right'], amount*speed_time/1e+6)
    elif direction == 'forward block':
        drive(0, start_speed['left'],0,start_speed['right'], amount*149*speed_time/1e+6)
    elif direction == 'backward':
        drive(1, start_speed['left'],1,start_speed['right'], amount*speed_time/1e+6)
    elif direction == 'backward block':
        drive(1, start_speed['left'],1,start_speed['right'], 149*amount*speed_time/1e+6)
    else:
        pass

def reset():
    motor1["pwm"].deinit()
    motor2["pwm"].deinit()
