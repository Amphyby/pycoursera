import socket
import asyncio
import time
import json
from select import select

class Server:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((address, port))
        self.sock.listen()
        self.data = {}
        self.to_monitor = []
        self.to_monitor.append(self.sock)
    def notify_error(self, client_sock):
        client_sock.send("error\nwrong command\n\n".encode())
        #print ("sent error")
    def notify_ok(self, client_sock):
        client_sock.send("ok\n\n".encode())
    def create_output_for_dictlisttuple(self, dict_data):
        result = "ok"
        for key, value in dict_data.items():
            for pair in value:
                current = f"\n{key} {pair[1]} {pair[0]}"
                result += current
        result += "\n\n"
        return result
    def process_put(self, request, client_sock):
        try:
            splitted = request.split()
            name = splitted[1]
            value = float(splitted[2])
            timestamp = int(splitted[3])
            self.data.setdefault(name, {})[timestamp] = value
            self.notify_ok(client_sock)
        except Exception:
            self.notify_error(client_sock)
    def process_get(self, request, client_sock):
        try:
            splitted = request.split()
            name = splitted[1]
            result = {}
            if name == "*":
                for key, value in self.data.items():
                    result[key] = list(value.items())
            elif name in self.data:
                result[name] = list(self.data[name].items())
            client_sock.send(self.create_output_for_dictlisttuple(result).encode())
        except Exception:
            self.notify_error(client_sock)

    def process_connection(self, client_sock):
        request = client_sock.recv(1024)
        if not request:
            return
        request = request.decode()[0:-1]
        try:
            cmd = request.split(" ")[0]
            if cmd == "put":
                if len(request.split(" ")) > 4:
                    self.notify_error(client_sock)
                else:
                    self.process_put(request, client_sock)
            elif cmd == "get":
                if len(request.split(" ")) > 2:
                    self.notify_error(client_sock)
                else:
                    self.process_get(request, client_sock)
            else:
                self.notify_error(client_sock)
        except Exception:
            self.notify_error(client_sock)
    def run(self):
        while True:
            ready_to_read, _, _ = select(self.to_monitor, [], [])
            for sock in ready_to_read:
                if sock is self.sock:
                    client_sock, addr = self.sock.accept()
                    self.to_monitor.append(client_sock)
                else:
                    if sock.fileno() == -1:
                        self.to_monitor.remove(sock)
                        continue
                    self.process_connection(sock)

def run_server(addr, port):
    s = Server(addr, port)
    s.run()
if __name__ == "__main__":
    run_server("127.0.0.1", 8889)