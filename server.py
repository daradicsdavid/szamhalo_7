import socket
import struct


def startServer():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 10000))
    sock.listen(1)
    connection, client_address = sock.accept()
    while True:
        # Wait for a connection
        data = connection.recv(1024)
        if data:
            answer = generateAnswer(data)
            message = struct.pack('f', answer)
            connection.sendall(message)
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
