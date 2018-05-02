import socket
import pickle
import threading
import sys
import ASV_Run2 as AR

class Server:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	connections = []
	data_list = []
	host = ''
	addr = 5545

	def __init__(self):
		self.sock.bind((self.host,self.addr))
		self.sock.listen(5)
		print("Server running..")


	#def handler(self, c, a):
	#	global connections
	#	while True:
	#		data = c.recv(4096)
	#		for connection in self.connections:
	#			connection.send(bytes(data))
	#		if not data:
	#			print(str(a[0]) + ':' + str(a[1]), "disconnected")
	#			self.connections.remove(c)
	#			c.close()
	#			break

	#def updateData(self):
	#	data = self.sock.recv(4096)
	#	data_arr = pickle.loads(data)
	#	for connection in self.connections:
	#		self.data_list.append(data_arr)
	#		connection.send(data_list)


	def dataTransfer(self, c, a):
		global connections
		while True:
			#c, a =self.sock.accept()
			data = c.recv(4096)	#Receive data
			data_arr = pickle.loads(data)
			self.data_list.append(data_arr)
			for connection in self.connections:
				connection.send(pickle.dumps(self.data_list))
			if not data:
				print(str(a[0]) + ':' + str(a[1]), "disconnected")
				self.connections.remove(c)
				c.close()
				break

	def run(self):
		while True:
			c, a = self.sock.accept()
			cThread = threading.Thread(target=self.dataTransfer, args=(c,a))
			cThread.daemon = True
			cThread.start()
			self.connections.append(c)
			print(str(a[0]) + ':' + str(a[1]), "connected")		# a[0], a[1] are the address and port
			print(a)



	#def sendPeers(self):
	#	p = ""
	#	for peer in self.peers:
	#		p = p + peer + ","
	#	for connection in self.connections:
	#		connection.send(b'\x11' + bytes(p, "utf-8"))


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
		#	if data[0:] == b'\x11':
		#		self.updatePeers(data[1:])
		#		print("Got peers ",self.peers)
			else:	
				print('Received', repr(data_arr))
				

	def sendMsg(self):
		ASV_Data = [AR.My_Data]
		data_string = pickle.dumps(ASV_Data)
		self.sock.send(data_string)
	
	#def updatePeers(self, peerData):
	#	p2p.peers = str(peerData, "utf-8").split(",")[:-1]

#class p2p:
#	peers = []

if (len(sys.argv) > 1):
	client = Client(sys.argv[1])
else:
	server = Server()
	server.run()