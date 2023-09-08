import socket
import threading

# Variable de bandera para controlar el servidor
server_running = True

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress
        print("Nueva conexión:", clientAddress)

    def run(self):
        print("Conexión desde:", self.clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg == 'fin':
                print("Cerrando la conexión con el cliente", self.clientAddress)
                break
            if msg == 'bye':
                break
            print("Desde el cliente:", msg)
            self.csocket.send(bytes(msg, 'UTF-8'))
        self.csocket.close()
        print("Cliente", self.clientAddress, "desconectado ...")

LOCALHOST = "127.0.0.1"
PORT = 1234
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Servicio iniciado ...")
print("Esperando solicitudes de conexión de clientes ...")
server.listen(1)

while server_running:
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()

server.close()
print("Servidor cerrado.")
