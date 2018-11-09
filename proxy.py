import select, socket, queue
import time


def startProxy():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 10000)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind(('localhost', 50000))
    server.listen(5)
    inputs = [server]
    outputs = []
    message_queues = {}

    cache = {}

    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)
        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)
                message_queues[connection] = queue.Queue()
            else:
                print("Proxy receiving data from client!")
                data = s.recv(1024)
                if data:
                    if data in cache and cache[data][1] - time.time() < 60:
                        serverAnswer = cache[data][0]
                    else:
                        print("Proxy sending data to server!")
                        sock.sendto(data, server_address)
                        serverAnswer, _ = sock.recvfrom(1024)
                        print("Proxy receiving data from server!")
                        cache[data] = (serverAnswer, time.time())
                    message_queues[s].put(serverAnswer)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]
                    if len(inputs) == 1:
                        inputs.remove(server)

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                outputs.remove(s)
            else:
                print("Proxy sending data to client!")
                s.send(next_msg)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]
