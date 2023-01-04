import socket
import sys

if len(sys.argv) != 3:
    print("Run like : python3 server.py <arg1:server ip:this system IP 192.168.1.6> <arg2:server port:4444 >")
    exit(1)

HOST = sys.argv[1]  
PORT = int(sys.argv[2])  

for i in range(1,1000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world")
        data = s.recv(1024)