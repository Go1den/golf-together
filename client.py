from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

class Client:
    def __init__(self, host: str = '', port: int = 33000, bufferSize: int = 1024, clientWindow=None):
        self.host = host
        self.port = port
        self.bufferSize = bufferSize
        self.clientWindow = clientWindow
        self.address = (self.host, self.port)

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(self.address)

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while True:
            try:
                msg = self.clientSocket.recv(self.bufferSize).decode("utf8")
                self.clientWindow.addText(msg)
            except OSError:  # Possibly client has left the chat.
                break

    def send(self, msg):  # event is passed by binders.
        self.clientSocket.send(bytes(msg, "utf8"))
        if msg == "!quit":
            self.clientSocket.close()

    def closeConnection(self, event=None):
        self.send("!quit")
