from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from tkinter import NORMAL, DISABLED

from messageConstants import MESSAGE_SUFFIX, QUIT, START_GAME, SET_GAME, SET_COURSE, END_GAME, SET_SCORE, SET_PLAYERS

class Client:
    def __init__(self, host: str = '', port: int = 33000, bufferSize: int = 1024, clientWindow=None):
        self.host = host
        self.port = port
        self.bufferSize = bufferSize
        self.clientWindow = clientWindow
        self.address = (self.host, self.port)

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(self.address)
        self.buffer = ""

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while True:
            try:
                self.buffer += self.clientSocket.recv(self.bufferSize).decode("utf8")
                while MESSAGE_SUFFIX in self.buffer:
                    msg, self.buffer = self.buffer.split(MESSAGE_SUFFIX, 1)
                    if msg.startswith(SET_GAME):
                        self.clientWindow.addText("<System> Host sets game to " + msg[9:])
                    elif msg.startswith(SET_COURSE):
                        splitMessage = msg[10:].split('[')
                        self.clientWindow.addText("<System> Host sets course to" + splitMessage[0])
                        self.clientWindow.setPars(splitMessage[1].rstrip("]"))
                    elif msg.startswith(START_GAME):
                        self.clientWindow.addText("<System> Host starts game.")
                        self.clientWindow.highlightCurrentHole()
                        self.clientWindow.setStateOfAllScoreButtons(NORMAL)
                        self.clientWindow.players = []
                    elif msg.startswith(END_GAME):
                        self.clientWindow.addText("<System> Host ends game.")
                        self.clientWindow.setStateOfAllScoreButtons(DISABLED)
                        self.clientWindow.resetGame()
                    elif msg.startswith(SET_SCORE):
                        self.clientWindow.updatePlayerScore(msg)
                    elif msg.startswith(SET_PLAYERS):
                        self.clientWindow.setPlayerListbox(msg[12:].split())
                    elif msg.startswith(QUIT):
                        pass
                    else:
                        self.clientWindow.addText(msg)
            except OSError:
                break

    def send(self, msg):
        try:
            self.clientSocket.send(bytes(msg + MESSAGE_SUFFIX, "utf8"))
        except ConnectionResetError:
            self.clientWindow.resetGame()
            self.clientWindow.resetOnLogoff()
            self.clientSocket.close()
            self.clientWindow.addText("<System> The lobby was closed by the host.")
        if msg == QUIT:
            self.clientWindow.resetGame()
            self.clientWindow.resetOnLogoff()
            self.clientSocket.close()
            self.clientWindow.addText("<System> You have left the lobby.")

    def closeConnection(self, event=None):
        self.send(QUIT)
