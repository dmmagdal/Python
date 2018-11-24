# commsTest2.py

import socket
import sys
from _thread import *

host = '10.0.0.132'
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((host, port))
except socket.error as e:
	print(str(e))

s.listen(5)

print("Waiting for a sign")

#conn, addr = s.accept()
#print("connected to %s" % addr)

def threaded_client(conn):
	conn.send(str.encode("Welcome. Type info\n"))

	while True:
		data = conn.recv(2048)
		reply = "Server output: " + data.decode('utf-8')

		if not data:
			break
		conn.sendall(str.encode(reply))

	conn.close()

while True:
	conn, addr = s.accept()
	print("connected to %s" % addr)

	start_new_thread(threaded_client, (conn, ))

