import socket
from pickle import dumps, loads

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(header, params=[]):
    req = {'header': header, 'params': params}
    client_socket.sendall(dumps(req))
    
    
def recv(BUF_SIZE=4096):
    data = b''
    while True:
        part = client_socket.recv(BUF_SIZE)
        data += part    
        if len(part) < BUF_SIZE:
            break
    return loads(data)


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
        send('shutdown')

    def req_get_screenshot(self):
        send('getscreenshot')
        res = recv()
        return res['data']

    def req_process_start(self, process_name):
        send('process-start', [process_name])
        res = recv()
        return res['ok']

    def req_process_kill(self, pid):
        send('process-kill', [pid])
        res = recv()
        return res['ok']

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

    def req_lock_keyboard(self):
        data = dumps('lock-keyboard')
        client_socket.sendall(data)

    def req_unlock_keyboard(self):
        data = dumps('unlock-keyboard')
        client_socket.sendall(data)    

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