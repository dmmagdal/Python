# clientProgram.py
# author: Diego Magdaleno
# Client counter part to the prototype of the server component of the
# dashboard.
# Python 3.6
# Linux


import os
import sys
import socket
import requests


def main():
	# Get machine's ip address.
	ip4 = socket.gethostbyname(socket.gethostname())
	# Port used by the server.
	port = 5055
	serveraddr = (str(ip4), port)

	serverClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverClient.connect(serveraddr)
	serverClient.sendall(b'Hello there')
	data = serverClient.recv(1024)
	print("Recieved "+str(repr(data)))
	#serverClient.sendall(b'General Kenobi')
	#data = serverClient.recv(1024)
	#print("Recieved "+str(repr(data)))
	#serverClient.sendall(b'You are a bold one')
	#data = serverClient.recv(1024)
	#print("Recieved "+str(repr(data)))
	


if __name__ == '__main__':
	main()
