from prometheus_client import start_http_server, Gauge
import time
import RPi.GPIO as GPIO

sensePath = "/sys/bus/w1/devices/28-012062361005/w1_slave"
refreshInterval = 0.5

prometheusTemperature = Gauge('temperature', 'currTemp')

P_RED = 18     # adapt to your wiring
P_GREEN = 12   # ditto
P_BLUE = 13    # ditto
fPWM = 50      # Hz (not higher with software PWM)

# init gpio shit
GPIO.cleanup()
GPIO.setmode (GPIO.BOARD)

# setup single LED
GPIO.setup (11, GPIO.OUT)
GPIO.setup(P_RED, GPIO.OUT)
GPIO.setup(P_GREEN, GPIO.OUT)
GPIO.setup(P_BLUE, GPIO.OUT)

GPIO.output(11, GPIO.LOW)

pwmR = GPIO.PWM(P_RED, fPWM)
pwmG = GPIO.PWM(P_GREEN, fPWM)
pwmB = GPIO.PWM(P_BLUE, fPWM)

pwmR.start(0)
pwmG.start(0)
pwmB.start(0)

def changeLightPerformance(light):
    pwmR.ChangeDutyCycle(light)
    pwmG.ChangeDutyCycle(light)
    pwmB.ChangeDutyCycle(light)

# für stetige
tempShould = 37000
tempMaxVolume = 45000

# für zwei-punkt
tempMin = 36000
tempMax = 38000

changeLightPerformance(100)
#Stetig
def controlRgbLED(temp):
    if int(temp) > tempShould:
        tempDiff = int(temp) - tempShould
        if tempDiff > tempMaxVolume:
            changeLightPerformance(0)
        else:
            changeLightPerformance(100 - (tempDiff * (100000/(tempMaxVolume/10)))/1000)
    else:
        changeLightPerformance(100)

#Zwei-Punkt
ledTurnedOn = False
def controlSingleLED(temp):
    global ledTurnedOn
    if ledTurnedOn is True and int(temp) < tempMin:
        GPIO.output(11, GPIO.LOW)
        ledTurnedOn = False

    # turn the led on
    if int(temp) > tempMax:
        GPIO.output(11, GPIO.HIGH)
        ledTurnedOn = True

def readTemperature():
    file = open(sensePath, "r")
    temperature = file.readlines()
    while temperature[0].strip()[-3:] != "YES":
        time.sleep(100)

    return temperature[1].split("=")[1]

def publishData(temp):
    prometheusTemperature.set(temp)

if __name__ == '__main__':
    start_http_server(9898, "127.0.0.1")
    while True:
        temp = readTemperature()
        controlSingleLED(temp)
        controlRgbLED(temp)
        publishData(temp)
        time.sleep(refreshInterval)
