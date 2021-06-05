from socket import AF_INET, socket, SOCK_STREAM
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
        self.server.bind(self.address)
        self.server.listen(self.backlog)
        self.clientWindow.addText("<System> Starting server...")
        self.acceptIncomingConnectionsThread = Thread(target=self.acceptIncomingConnections, daemon=True)
        self.acceptIncomingConnectionsThread.start()
        self.clientWindow.addText("<System> The server is now live.")
        # self.acceptIncomingConnectionsThread.join() #blocks the calling thread, we might not need/want this

    def shutdownServer(self):
        self.server.close()

    def acceptIncomingConnections(self):
        while True:
            client, client_address = self.server.accept()
            print(str(client_address) + " has connected.")
            client.send(bytes("<System> Type your name and press enter!", "utf8"))
            self.connectedAddresses[client] = client_address
            Thread(target=self.handleClient, args=(client,)).start()

    def handleClient(self, client):
        name = client.recv(self.bufferSize).decode("utf8")
        welcome = "<System> Welcome %s! Type !quit at any time to exit." % name
        client.send(bytes(welcome, "utf8"))
        msg = "<System> %s connected." % name
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name

        while True:
            msg = client.recv(self.bufferSize)
            if msg != bytes("!quit", "utf8"):
                self.broadcast(msg, "<" + name + "> ")
            else:
                client.send(bytes("!quit", "utf8"))
                client.close()
                del self.clients[client]
                self.broadcast(bytes("<System> %s disconnected." % name, "utf8"))
                break

    def broadcast(self, msg, prefix=""):
        print(prefix + str(msg.decode("utf-8")))
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)
