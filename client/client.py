import socket
from pickle import dumps, loads

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Client:
    def __init__(self):
        self.host = '';
        self.port = 0;

    def connect(self):
        try:
            client_socket.connect((self.host, self.port))
            return True
        except:
            return False

    def disconnect(self):
        client_socket.close()

    def req_shutdown(self):
        data = dumps('shutdown')
        client_socket.sendall(data)

    def req_get_screenshot(self):
        data = dumps('getscreenshot')
        client_socket.sendall(data)
        res = loads(client_socket.recv(7220907))
        return res

    def req_process_start(self, process_name):
        data = dumps(('process-start', process_name))
        client_socket.sendall(data)
        res = loads(client_socket.recv(1024))
        return res

    def req_process_kill(self, pid):
        data = dumps(('process-kill', pid))
        client_socket.sendall(data)
        res = loads(client_socket.recv(1024))
        return res

    def req_process_getall(self):
        data = dumps('process-getall')
        client_socket.sendall(data)
        res = loads(client_socket.recv(2**16))
        return res

    def req_process_getallapp(self):
        data = dumps('process-getallapp')
        client_socket.sendall(data)
        res = loads(client_socket.recv(2**16))
        return res

    def req_keystroke_hook(self):
        data = dumps('keystroke-hook')
        client_socket.sendall(data)
    
    def req_keystroke_unhook(self):
        data = dumps('keystroke-unhook')
        client_socket.sendall(data)
    
    def req_keystroke_get(self):
        data = dumps('keystroke-get')
        client_socket.sendall(data)
        res = loads(client_socket.recv(2**10))
        return res

    def req_reg_getvalue(self, path, value_name):
        data = dumps(('reg-getvalue', path, value_name))
        client_socket.sendall(data)
        res = loads(client_socket.recv(2**16))
        return res

    def req_reg_setvalue(self, path, value_name, dtype, value):
        data = dumps(('reg-setvalue', path, value_name, dtype, value))
        client_socket.sendall(data)
        res = loads(client_socket.recv(1024))
        return res

    def req_reg_deletevalue(self, path, value_name):
        data = dumps(('reg-deletevalue', path, value_name))
        client_socket.sendall(data)
        res = loads(client_socket.recv(1024))
        return res

    def req_reg_createkey(self, path):
        data = dumps(('reg-createkey', path))
        client_socket.sendall(data)
        res = loads(client_socket.recv(1024))
        return res

    def req_reg_deletekey(self, path):
        data = dumps(('reg-deletekey', path))
        client_socket.sendall(data)
        res = loads(client_socket.recv(1024))
        return res

    def req_reg_import(self, content):
        data = dumps(('reg-import', content))
        client_socket.sendall(data)
        res = loads(client_socket.recv(1024))
        return res