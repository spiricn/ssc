import socket


def getLocalIp():
    addresses = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]


    for i in addresses:
        if not i.startswith('192.'):
            continue

        comps = i.split('.')

        if comps[-2] != '1':
            continue

        return i
