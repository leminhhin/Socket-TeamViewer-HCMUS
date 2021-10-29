import os
from pickle import loads, dumps
import socket
import threading
import utils, process, keystroke, registry
import tkinter.messagebox as msbx

HOST = socket.gethostname()
PORT = 10000

def norm_path(path):
    return os.path.normpath(path).replace('\\', '/')


def connection_handler(connection, address):
    print(f'{address[0]}:{address[1]} connected')
    keystroke_detector = keystroke.KeystrokeDetector()
    while True:
        try:
            recv_data = loads(connection.recv(2**16))
            print("Receiving data")
            if not recv_data: break
        except:
            break
        if isinstance(recv_data, str):
            req = recv_data
            print("Client request: " + req)
            
        else:
            req = recv_data[0]
            params = recv_data[1:]
            print("Client request: " + req)       
            
        if req == 'shutdown':
            data = dumps(utils.shutdown())
            connection.sendall(data)

        elif req == 'logout':
            data = dumps(utils.logout())
            connection.sendall(data)

        elif req == 'getscreenshot':
            data = dumps(utils.get_screenshot())
            connection.sendall(data)

        elif req == 'process-start':
            process_name, = params
            data = dumps(process.start(process_name))
            connection.sendall(data)

        elif req == 'process-kill':
            pid, = params
            data = dumps(process.kill(pid))
            connection.sendall(data)

        elif req == 'process-getall':
            data = dumps(process.get_running_processes())
            connection.sendall(data)
            
        elif req == 'process-getallapp':
            data = dumps(process.get_running_applications())
            connection.sendall(data)

        elif req == 'keystroke-hook':
            data = dumps(keystroke_detector.start_listening())
            connection.sendall(data)

        elif req == 'keystroke-unhook':
            data = dumps(keystroke_detector.end_listening())
            connection.sendall(data)

        elif req == 'keystroke-get':
            data = dumps(keystroke_detector.get_keys())
            connection.sendall(data)

        elif req == 'reg-getvalue':
            path, value_name = params
            path = norm_path(path)
            data = dumps(registry.get_value(path, value_name))
            connection.sendall(data)

        elif req == 'reg-setvalue':
            path, value_name, dtype, value = params
            path = norm_path(path)
            data = dumps(registry.set_value(path, value_name, dtype, value))
            connection.sendall(data)

        elif req == 'reg-deletevalue':
            path, value_name = params
            path = norm_path(path)
            data = dumps(registry.delete_value(path, value_name))
            connection.sendall(data)

        elif req == 'reg-createkey':
            path, = params
            path = norm_path(path)
            data = dumps(registry.create_key(path))
            connection.sendall(data)

        elif req == 'reg-deletekey':
            path, = params
            path = norm_path(path)
            data = dumps(registry.delete_key(path))
            connection.sendall(data)

        elif req == 'reg-import':
            content, = params
            data = dumps(registry.import_reg(content))
            connection.sendall(data)
        
        else:
            data = dumps('Invalid')
            connection.sendall(data)
    
    connection.close()
    print(f'{address[0]}:{address[1]} disconnected')
    exit(0)

def open_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    conn, addr = server_socket.accept()
    t = threading.Thread(target=connection_handler, args=[conn, addr])
    t.start()
    server_socket.close()
    return None

