import socket
import struct


def startServer():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 10000))
    while True:
        # Wait for a connection
        data, address = sock.recvfrom(1024)
        if data:
            answer = generateAnswer(data)
            message = struct.pack('f', answer)
            sock.sendto(message, address)
        else:
            break


def generateAnswer(data):
    receivedData = struct.unpack("!cii", data)
    operator = receivedData[0].decode('ascii')
    number1 = receivedData[1]
    number2 = receivedData[2]
    if operator == '+':
        return number1 + number2
    if operator == '-':
        return number1 - number2
    if operator == '*':
        return number1 * number2
    if operator == '/':
        return number1 / number2
