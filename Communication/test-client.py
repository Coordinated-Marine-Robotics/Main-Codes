import socket, pickle

HOST = '192.168.0.18'
PORT = 5545
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
arr = ([1,2,3,4,5,6],[1,2,3,4,5,6])
data_string = pickle.dumps(arr)
s.send(data_string)

data = s.recv(4096)
data_arr = pickle.loads(data)
s.close()
print('Received', repr(data_arr))