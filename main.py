from threading import Thread
from time import sleep

from client import startClient
from proxy import startProxy
from server import startServer

if __name__ == '__main__':
    print("Starting server!")
    serverThread = Thread(target=startServer)
    serverThread.start()

    sleep(1)

    print("Starting proxy!")
    proxyThread = Thread(target=startProxy)
    proxyThread.start()

    sleep(1)

    print("Starting client!")
    clientThread = Thread(target=startClient)
    clientThread.start()

    clientThread.join()
    proxyThread.join()
    serverThread.join()
