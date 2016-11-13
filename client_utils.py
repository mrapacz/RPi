import re

import subprocess


def get_ip_from_arptable(MAC):
    stream = subprocess.Popen('ip neighbour show', shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+) .+? ' + MAC)

    result = re.search(pattern, stream)
    if result is not None:
        return result.groups()[0]
    else:
        return result


def get_mac_address(filename='rpi_mac.txt'):
    with open(filename) as mac_file:
        MAC = mac_file.readline().rstrip()
    return MAC


def ping_neighbours():
    devnull = open('/dev/null', 'w')
    subprocess.Popen('nmap -sn 192.168.1.101-110', shell=True, stdout=devnull).wait(timeout=5)
    return


def get_rpi_ip():
    MAC = get_mac_address()
    ip = get_ip_from_arptable(MAC)

    while ip is None:
        print("IP for the given MAC address not found, pinging neighbours...")
        ping_neighbours()
        ip = get_ip_from_arptable(MAC)

    print("Found {0} at {1}".format(MAC, ip))
    return ip
