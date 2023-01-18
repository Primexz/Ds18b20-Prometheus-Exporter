from prometheus_client import start_http_server, Gauge
import time

sens_path = "/sys/bus/w1/devices/28-012062361005/w1_slave"
interval = 2000

prometheus_temp = Gauge('temperature', 'currTemp')

def read_temp():
    file = open(sens_path, "r")
    temperature = file.readlines()
    while temperature[0].strip()[-3:] != "YES":
        time.sleep(100)

    return temperature[1].split("=")[1]

def publish_data(temp):
    prometheus_temp.set(temp)

if __name__ == '__main__':
    start_http_server(9898, "127.0.0.1")
    while True:
        temp = read_temp()
        publish_data(temp)
        time.sleep(interval)
