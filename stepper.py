import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

ENA_1 = 2
DIR_1 = 3
PUL_1 = 4
ENA_2 = 17
DIR_2 = 27
PUL_2 = 22

forward1 = True
forward2 = True

for pin in [ENA_1, DIR_1, PUL_1, ENA_2, DIR_2, PUL_2]:
    GPIO.setup(pin, GPIO.OUT)

GPIO.output(ENA_1, GPIO.LOW)
GPIO.output(ENA_2, GPIO.LOW)
GPIO.output(DIR_1, GPIO.HIGH if forward1 else GPIO.LOW)
GPIO.output(DIR_2, GPIO.HIGH if forward2 else GPIO.LOW)

# Does n steps with interval t (in s)
# motorNum: 1 -> big motor; 2 -> small motor
def doSteps(motorNum, n, t):
    pul_pin = PUL_1 if motorNum == 1 else PUL_2
    for i in range(n):
        GPIO.output(pul_pin, GPIO.HIGH)
        sleep(t / 2)
        GPIO.output(pul_pin, GPIO.LOW)
        sleep(t / 2)

def reverse(motorNum):
    global forward1
    global forward2
    dir_pin = DIR_1 if motorNum == 1 else DIR_2
    forward = forward1 if motorNum == 1 else forward2
    GPIO.output(dir_pin, GPIO.LOW if forward else GPIO.HIGH)
    if motorNum == 1:
        forward1 = not forward1
    else:
        forward2 = not forward2
    sleep(1)

if __name__ == '__main__':
    while True:
        print("Enter [motor number] [number of steps] [interval]: ")
        arr = input().split(' ')
        motorNum = int(arr[0])
        numSteps = int(arr[1])
        interval = float(arr[2])
        if numSteps < 0:
            reverse(motorNum)
        doSteps(motorNum, numSteps, interval)
        if numSteps < 0:
            reverse(motorNum)
