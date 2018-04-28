import socket

HOST = ''
PORT = 5545
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(3)
conn, addr = s.accept()
print('Connected by', addr)
while True:
    data = conn.recv(4096)
    if not data: break
    conn.send(data)
conn.close()