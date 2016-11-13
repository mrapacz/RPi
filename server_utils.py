import os
import re

import subprocess
from time import sleep

LOCATION = '/sys/bus/w1/devices/28-8000001ea518/'
FILENAME = 'w1_slave'


def trigger_measuring(filepath):
    """Used to trigger temperature measuring in sensor module"""
    with open(filepath):
        pass


def get_temperature():
    filepath = os.path.join(LOCATION, FILENAME)

    trigger_measuring(filepath)
    with open(filepath) as file:
        file.readline()
        line = file.readline()
        pattern = re.compile('t=(\d+)')
        temperature = re.search(pattern, line).groups()[0]
    return temperature


orders = {
    'get_temperature': get_temperature
}


def get_host_ip(max_fail_count=60):
    ip = None
    fail_count = 0
    while ip is None and fail_count < max_fail_count:
        ip = subprocess.Popen("hostname -I", shell=True, stdout=subprocess.PIPE).stdout.read().decode().rstrip()
        fail_count += 1
        sleep(1)
    if ip is None:
        raise ConnectionError("No internet connection")
    return ip
