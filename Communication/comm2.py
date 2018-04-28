import socket
import pickle
import threading
import sys

class Server:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	connections = []
	peers = []
	host = ''
	addr = 5545

	def __init__(self):
		self.sock.bind((self.host,self.addr))
		self.sock.listen(5)
		print("Server running..")


	def handler(self, c, a):
		global connections
		while True:
			data = c.recv(4096)
			for connection in self.connections:
				connection.send(bytes(data))
			if not data:
				print(str(a[0]) + ':' + str(a[1]), "disconnected")
				self.connections.remove(c)
				self.peers.remove(a[0])
				c.close()
				self.sendPeers()
				break

	def run(self):
		while True:
			c, a = self.sock.accept()
			cThread = threading.Thread(target=self.handler, args=(c,a))
			cThread.daemon = True
			cThread.start()
			self.connections.append(c)
			self.peers.append(a[0])	
			print(str(a[0]) + ':' + str(a[1]), "connected")		# a[0], a[1] are the address and port
			self.sendPeers()

	def sendPeer():
		p = ""
		for peer in self.peers:
			p = p + peer + ","

		for connection in self.connections:
			connection.send(b'\x11' + bytes(p,"utf-8"))

	#def sendCon(self):
	#	while True:
	#		connData = pickle.dumps(self.connections)
	#		self.sock.send(connData)

class Client:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host = ''
	addr = 5545

	def __init__(self, address):
		self.sock.connect((address,self.addr))

		iThread = threading.Thread(target=self.sendMsg)
		iThread.daemon = True	#So that it will close when we close the program
		iThread.start()

		while True:
			data = self.sock.recv(4096)
			data_arr = pickle.loads(data)
			if not data:
				break
			if data[0:1] == b'\x11':
				print("Got peers")
			else:
				print('Received', repr(data_arr))

	def sendMsg(self):
		data_string = pickle.dumps([1,2,3])
		self.sock.send(data_string)

	

if (len(sys.argv) > 1):
	client = Client(sys.argv[1])
else:
	server = Server()
	server.run()