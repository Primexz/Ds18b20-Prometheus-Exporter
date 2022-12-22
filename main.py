from prometheus_client import start_http_server, Gauge
import time

sensePath = "/sys/bus/w1/devices/28-012062361005/w1_slave"
readInterval = 10

prom_Temp = Gauge('temperature', 'currTemp')

def readTemperature():
    file = open(sensePath, "r")
    temperature = file.readlines()
    print(temperature)
    return temperature[1].split("=")[1]

def process_request(temp):
    prom_Temp.set(temp)

if __name__ == '__main__':
    start_http_server(9898)
    while True:
        temp = readTemperature()
        process_request(temp)
        time.sleep(readInterval)
