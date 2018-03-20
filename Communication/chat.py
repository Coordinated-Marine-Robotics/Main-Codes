import socket
import threading

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


host = ''
addr = 5545

sock.bind((host,addr))

sock.listen(5)

connections = []

def handler(c, a):
	global connections
	while True:
		data = c.recv(1024)
		for connection in connections:
			connection.send(bytes(data))
		if not data:
			connections.remove(c)
			c.close()
			break

while True:
	c, a = sock.accept()
	cThread = threading.Thread(target=handler, args=(c,a))
	cThread.daemon = True
	cThread.start()
	connections.append(c)
	print(connections)