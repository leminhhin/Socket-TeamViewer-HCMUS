import os
from client import Client

def test_client():
    c = Client()
    c.host = 'LAPTOP-4B0IVBB0'
    c.port = 10000
    c.connect()
    
    print(
        c.req_dirtree_client2server(
            r"C:\Users\chibi\Desktop\aaa.txt",
            r"C:\Users\chibi\Desktop\a"
        )
    )
    
    print(
        c.req_dirtree_server2client(
            r"C:\Users\chibi\Desktop\img.jpeg",
            r"C:\Users\chibi\Desktop\a"
        )
    )
    
    print(
        c.req_dirtree_server2server(
            r"C:\Users\chibi\Desktop\xxx.txt",
            r"C:\Users\chibi\Desktop"
        )
    )
    
    print(
        c.req_dirtree_server2server(
            r"C:\Users\chibi\Desktop\xxx.txt",
            r"C:\Users\chibi\Desktop\a"
        )
    )

test_client()