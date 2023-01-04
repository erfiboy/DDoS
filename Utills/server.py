import sys
import socket
import selectors
import types

if len(sys.argv) != 3:
    print("Run like : python3 server.py <arg1:server ip:this system IP 192.168.1.6> <arg2:server port:4444 >")
    exit(1)

sel = selectors.DefaultSelector()

HOST = sys.argv[1]  # Standard loopback interface address (localhost)
PORT = int(sys.argv[2])  # Port to listen on (non-privileged ports are > 1023)

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
print(f"Listening on {(HOST, PORT)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)