import os
import socket
import sys


if os.name != "nt":
    import fcntl
    import struct

    def getInterfaceIp(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s'.encode('ascii'), ifname[:15].encode('ascii')))[20:24])

def getLocalIp():
    if sys.platform == 'win32':
        addresses = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]

        for i in addresses:
            if not i.startswith('192.'):
                continue

            comps = i.split('.')

            if comps[-2] != '1':
                continue

            return i

    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = getInterfaceIp(ifname)
                break
            except IOError:
                pass
    return ip
