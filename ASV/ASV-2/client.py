import socket
import pickle
import threading
import sys
import ASV_Functions as AF

class Client:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host = '192.168.0.18'
	addr = 5545

	def __init__(self):
		self.sock.connect((self.host,self.addr))

		iThread = threading.Thread(target=self.sendMsg)
		iThread.daemon = True	#So that it will close when we close the program
		iThread.start()

	def receive(self):
		while True:
			data = self.sock.recv(4096)
			data_arr = pickle.loads(data)
			if not data:
				break
		#	if data[0:] == b'\x11':
		#		self.updatePeers(data[1:])
		#		print("Got peers ",self.peers)
			#else:	
				#print('Received', data_arr)
			return data_arr
			
				

	def sendMsg(self):
		ASV_Data = [AF.My_Data]
		data_string = pickle.dumps(ASV_Data)
		self.sock.send(data_string)
