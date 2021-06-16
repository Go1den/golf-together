from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread

from messageConstants import MESSAGE_SUFFIX, SET_PLAYERS, SYSTEM, QUIT, START_GAME, END_GAME, SET_SCORE

class Server:
    def __init__(self, host: str = '', port: int = 33000, bufferSize: int = 1024, backlog: int = 128, clientWindow=None):
        self.host = host
        self.port = port
        self.bufferSize = bufferSize
        self.backlog = backlog
        self.clientWindow = clientWindow
        self.address = (self.host, self.port)
        self.clients = {}
        self.connectedAddresses = {}
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.bind(self.address)
        self.server.listen(self.backlog)
        self.clientWindow.addText("<System> Starting server...")
        self.acceptIncomingConnectionsThread = Thread(target=self.acceptIncomingConnections, daemon=True)
        self.acceptIncomingConnectionsThread.start()
        self.clientWindow.addText("<System> The server is now live.")

    def shutdownServer(self):
        self.server.close()

    def acceptIncomingConnections(self):
        try:
            while True:
                client, client_address = self.server.accept()
                print(str(client_address) + " has connected.")
                self.connectedAddresses[client] = client_address
                Thread(target=self.handleClient, args=(client,)).start()
        except:
            self.shutdownServer()

    def handleClient(self, client):
        name = client.recv(self.bufferSize).decode("utf8").split(MESSAGE_SUFFIX)[0]
        welcome = SYSTEM + " Welcome, " + name + "! Type !quit at any time to exit." + MESSAGE_SUFFIX
        client.send(bytes(welcome, "utf8"))
        msg = SYSTEM + " " + name + " connected." + MESSAGE_SUFFIX
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name
        self.setPlayersMessage()
        buffer = ""

        while True:
            buffer += client.recv(self.bufferSize).decode("utf8")
            while MESSAGE_SUFFIX in buffer:
                msg, buffer = buffer.split(MESSAGE_SUFFIX, 1)
                if msg == QUIT:
                    client.close()
                    del self.clients[client]
                    disconnectMsg = SYSTEM + " " + name + " disconnected." + MESSAGE_SUFFIX
                    self.broadcast(bytes(disconnectMsg, "utf8"))
                    break
                elif msg == START_GAME or msg == END_GAME or msg.startswith(SET_SCORE):
                    self.broadcast(bytes(msg + MESSAGE_SUFFIX, "utf8"))
                else:
                    self.broadcast(bytes(msg + MESSAGE_SUFFIX, "utf8"), "<" + name + "> ")
                self.setPlayersMessage()

    def setPlayersMessage(self):
        setPlayersMsg = SET_PLAYERS + " " + self.getSpaceDelineatedListOfConnectedPlayers() + MESSAGE_SUFFIX
        self.broadcast(bytes(setPlayersMsg, "utf8"))

    def broadcast(self, msg, prefix=""):
        print(prefix + str(msg.decode("utf-8")))
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)

    def closeAllConnections(self):
        for client in self.clients:
            client.close()
        self.clients = {}

    def getSpaceDelineatedListOfConnectedPlayers(self):
        result = ""
        for name in self.clients.values():
            result += name + " "
        return result.rstrip()
