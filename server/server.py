import os
from pickle import loads, dumps
import socket
import threading
import utils, process, keystroke, registry, lock_keyboard

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
    conn.sendall(dumps(res))


def recv(conn, BUF_SIZE=4096):
    data = b''
    while True:
        part = conn.recv(BUF_SIZE)
        data += part    
        if len(part) < BUF_SIZE:
            break
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
        except EOFError:
            break
        except Exception as e:
            raise e
            
        if header == 'shutdown':
            try:
                utils.shutdown()
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
            data = dumps(process.get_running_processes())
            connection.sendall(data)
            
        elif header == 'process-getallapp':
            data = dumps(process.get_running_applications())
            connection.sendall(data)

        elif header == 'keystroke-hook':
            data = dumps(keystroke_detector.start_listening())
            connection.sendall(data)

        elif header == 'keystroke-unhook':
            data = dumps(keystroke_detector.end_listening())
            connection.sendall(data)

        elif header == 'keystroke-get':
            data = dumps(keystroke_detector.get_keys())
            connection.sendall(data)

        elif header == 'lock-keyboard':
            data = dumps(lock_keyboard.enable())
            connection.sendall(data)

        elif header == 'unlock-keyboard':
            data = dumps(lock_keyboard.disable())
            connection.sendall(data)

        elif header == 'reg-getvalue':
            path, value_name = params
            path = norm_path(path)
            data = dumps(registry.get_value(path, value_name))
            connection.sendall(data)

        elif header == 'reg-setvalue':
            path, value_name, dtype, value = params
            path = norm_path(path)
            data = dumps(registry.set_value(path, value_name, dtype, value))
            connection.sendall(data)

        elif header == 'reg-deletevalue':
            path, value_name = params
            path = norm_path(path)
            data = dumps(registry.delete_value(path, value_name))
            connection.sendall(data)

        elif header == 'reg-createkey':
            path, = params
            path = norm_path(path)
            data = dumps(registry.create_key(path))
            connection.sendall(data)

        elif header == 'reg-deletekey':
            path, = params
            path = norm_path(path)
            data = dumps(registry.delete_key(path))
            connection.sendall(data)

        elif header == 'reg-import':
            content, = params
            data = dumps(registry.import_reg(content))
            connection.sendall(data)
        
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