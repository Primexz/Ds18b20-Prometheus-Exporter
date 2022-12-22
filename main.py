from prometheus_client import start_http_server, Gauge
import time

sensePath = "/sys/bus/w1/devices/28-012062361005/w1_slave"
refreshInterval = 2

prometheusTemperature = Gauge('temperature', 'currTemp')

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
        publishData(temp)
        time.sleep(refreshInterval)
