import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

ENA_1 = 2
DIR_1 = 3
PUL_1 = 4
ENA_2 = 17
DIR_2 = 27
PUL_2 = 22

for pin in [ENA_1, DIR_1, PUL_1, ENA_2, DIR_2, PUL_2]:
    GPIO.setup(pin, GPIO.OUT)

GPIO.output(ENA_1, GPIO.LOW)
GPIO.output(ENA_2, GPIO.LOW)
GPIO.output(DIR_1, GPIO.HIGH)
GPIO.output(DIR_2, GPIO.HIGH)

# Does n steps with interval t (in s)
# motorNum: 1 -> big motor; 2 -> small motor
# n < 0 --> backwards movement
def doSteps(motorNum, n, t):
    ena_pin = ENA_1 if motorNum == 1 else ENA_2
    dir_pin = DIR_1 if motorNum == 1 else DIR_2
    pul_pin = PUL_1 if motorNum == 1 else PUL_2
    numSteps = n if n > 0 else -n

    if n < 0:
        GPIO.output(dir_pin, GPIO.LOW)
        sleep(0.5)
    GPIO.output(ena_pin, GPIO.HIGH)

    for i in range(numSteps):
        GPIO.output(pul_pin, GPIO.HIGH)
        sleep(t / 2)
        GPIO.output(pul_pin, GPIO.LOW)
        sleep(t / 2)

    GPIO.output(ena_pin, GPIO.LOW)
    if n < 0:
        GPIO.output(dir_pin, GPIO.HIGH)
        sleep(0.5)

if __name__ == '__main__':
    while True:
        print("Enter [motor number] [number of steps] [interval]: ")
        arr = input().split(' ')
        doSteps(int(arr[0]), int(arr[1]), float(arr[2]))
