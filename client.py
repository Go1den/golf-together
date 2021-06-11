from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from tkinter import NORMAL, DISABLED

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
                if msg.startswith("!setgame"):
                    self.clientWindow.addText("<System> Host sets game to " + msg[9:])
                elif msg.startswith("!setcourse"):
                    splitMessage = msg[10:].split('[')
                    self.clientWindow.addText("<System> Host sets course to" + splitMessage[0])
                    self.clientWindow.setPars(splitMessage[1].rstrip("]"))
                elif msg.startswith("!startgame"):
                    self.clientWindow.addText("<System> Host starts game.")
                    self.clientWindow.highlightCurrentHole()
                    self.clientWindow.setStateOfAllScoreButtons(NORMAL)
                    self.clientWindow.players = []
                elif msg.startswith("!endgame"):
                    self.clientWindow.addText("<System> Host ends game.")
                    self.clientWindow.setStateOfAllScoreButtons(DISABLED)
                    self.clientWindow.resetGame()
                elif msg.startswith("!setscore"):
                    self.clientWindow.updatePlayerScore(msg)
                elif msg.startswith("!quit"):
                    pass
                else:
                    self.clientWindow.addText(msg)
            except OSError:
                break

    def send(self, msg):
        self.clientSocket.send(bytes(msg, "utf8"))
        if msg == "!quit":
            self.clientWindow.resetGame()
            self.clientWindow.resetOnLogoff()
            self.clientSocket.close()
            self.clientWindow.addText("<System> You have left the lobby.")

    def closeConnection(self, event=None):
        self.send("!quit")
