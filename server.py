from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread

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
        name = client.recv(self.bufferSize).decode("utf8")
        welcome = "<System> Welcome %s! Type !quit at any time to exit." % name
        client.send(bytes(welcome, "utf8"))
        msg = "<System> %s connected." % name
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name
        self.broadcast(bytes("!setplayers %s" % self.getSpaceDelineatedListOfConnectedPlayers(), "utf8"))

        while True:
            msg = client.recv(self.bufferSize)
            if msg == bytes("!quit", "utf8"):
                client.close()
                del self.clients[client]
                self.broadcast(bytes("<System> %s disconnected." % name, "utf8"))
                break
            elif msg == bytes("!startgame", "utf8") or msg == bytes("!endgame", "utf8") or msg.startswith(bytes("!setscore", "utf8")):
                self.broadcast(bytes(msg))
            else:
                self.broadcast(msg, "<" + name + "> ")
            self.broadcast(bytes("!setplayers %s" % self.getSpaceDelineatedListOfConnectedPlayers(), "utf8"))

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
