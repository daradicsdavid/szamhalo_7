import random
import socket
import struct


def startClient():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 50000))
    sent = 0
    while sent < 50:
        s.sendall(createMessage())
        data = s.recv(1024)
        receivedData = struct.unpack("f", data)
        print('Received %d' % (receivedData[0]))
        sent += 1
    # s.close()


def createMessage():
    operator = randomOperator()
    number1 = randomInt()
    number2 = randomInt()
    print("Client sending data %c %d %d" % (operator, number1, number2))
    return struct.pack('!cii', operator.encode('ascii'), number1, number2)


def randomOperator():
    randomValue = random.randint(1, 4)
    if randomValue == 1:
        return '+'
    if randomValue == 2:
        return '-'
    if randomValue == 3:
        return '*'
    if randomValue == 4:
        return '/'


def randomInt():
    return random.randint(1, 5)
