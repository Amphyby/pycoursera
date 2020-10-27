import time
import socket
import json

class ClientError(Exception):
    pass

class Client:
    def __init__(self, url, port, timeout):
        self.url = url
        self.port = port
        self.timeout = timeout
    def put(self, name, value, timestamp = None):
        timestamp = int(time.time()) if timestamp is None else timestamp
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.timeout)
            s.connect((self.url, self.port))
            s.sendall("put {} {} {}\n".format(name, value, timestamp).encode())
            response = s.recv(1024)
            print("put {} {} {}\n".format(name, value, timestamp))
            if 'ok\n\n' == response.decode():
                print ("got ok: ", repr(response))
            else:
                raise ClientError()

    def get(self, name):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.timeout)
            s.connect((self.url, self.port))
            s.sendall("get {}\n".format(name).encode())
            response = s.recv(1024)
            decoded_response = response.decode()
            current_response = {}
            if decoded_response == "ok\n\n":
                return {}
            try :
                if decoded_response[0 : 3] == "ok\n" and decoded_response[-2:] == "\n\n":
                    for line in decoded_response[3 : len(decoded_response)-2].split("\n"):
                        [name, value, timestamp] = line.split(" ")
                        """if not (type(name)==str):
                            raise SystemError("name")
                        if not (type(value) == float or type(value) == int):
                            raise SystemError("value")
                        if not (type(timestamp) == int):
                            raise SystemError("ts")"""
                        tempval = float(value)
                        tempts = int(timestamp)
                        current_response.setdefault(name, []).append((tempts, tempval))
                    for keyi in current_response:
                        current_response[keyi].sort(key=lambda x: x[0])
                    return current_response
            except:
                raise ClientError()
            raise ClientError()


