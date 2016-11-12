import os
import re

LOCATION = '/sys/bus/w1/devices/28-8000001ea518/'
FILENAME = 'w1_slave'


def get_temperature():
    with open(os.path.join(LOCATION, FILENAME)) as file:
        file.readline()
        line = file.readline()
        pattern = re.compile('t=(\d+)')
        temperature = re.search(pattern, line).groups()[0]
    return temperature


orders = {
    'get_temperature': get_temperature
}
