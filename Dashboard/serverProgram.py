# serverProgram.py
# author: Diego Magdaleno
# Prototype of the server component of the dashboard. This is a simple
# server program that uses tcp protocol to communicate. Will test
# making a server with both the socket module and the socketserver
# module. Only handles one connenction at a time.
# Python 3.6
# Linux


import os
import sys
import socket
import socketserver
import select


class MyTCPHandler(socketserver.BaseRequestHandler):
	# This handler class inherits from the BaseRequestHandler class.
	def handle(self):
		# This is the client socket.
		self.data = self.request.recv(1024).strip()
		# self.client_address is the client detail ([0] is the ip
		# address and [1] is the port number).
		# Print the client data.
		print("{}:{} wrote:".format(self.client_address[0],
									 self.client_address[1]))
		print(self.data)
		# Send the data back to the client (this time in all caps).
		self.request.sendall(self.data.upper())



def main():
	# Check command line arguments.
	if invalidCMD():
		print("Error: Invalid command line arguments")
		print("Usage: python serverProgram.py <sock/sockserv/socksentdx>")
		exit(1)

	# Successful start of program.
	print("Server program running...")

	# Get the ip address of this machine. Will use this address for
	# both the client and the server (because we need to test this
	# locally before deploying).
	ip4 = socket.gethostbyname(socket.gethostname())
	#print("Ip address "+str(ip4))	# For debug.
	port = 5055
	serveraddr = (str(ip4), port)

	# Create a server based on the mode selected.
	mode = sys.argv[1]
	if mode == "sock":
		createSock(serveraddr)
	elif mode == "sockserv":
		createSockServer(serveraddr)
	else:
		createSockSentdex(serveraddr)
	#print("Running Server program at ")


# Check to see that the command line arguments are valid.
# @param, takes no arguments.
# @return, returns a boolean.
def invalidCMD():
	modeList = ["sock", "sockserv", "socksentdx"]
	# Check for length of the command line args.
	if len(sys.argv) != 2:
		return True
	# Check to see that the args for the mode are valid.
	elif sys.argv[1] not in modeList:
		return True
	else:
		return False


# Creates a server with the socket module.
# @param, serveraddr: the server address, which contains the ip address
#	and port number.
# @return, returns nothing.
def createSock(serveraddr):
	# Create a server object out of a socket.
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(serveraddr)
	server.listen()
	conn, addr = server.accept()
	with conn:
		print("Connected by "+str(addr))
		while True:
			data = conn.recv(1024)
			if not data:
				break
			print(data.decode("utf-8"))
			# Echo input from client.
			#conn.sendall(data)

			# Return data but with "!!!" at the end.
			newData = data.decode("utf-8")
			newData = newData + "!!!"
			conn.sendall(newData.encode("utf-8"))


# Create a server with the socketserver module.
# @param, serveraddr: the server address, which contains the ip address
#	and port number.
# @return, returns nothing.
def createSockServer(serveraddr):
	# Create a server object (TCPserver). Include the server address
	# (its host address and port) and the handler class (MyTCPHandler)
	server = socketserver.TCPServer(serveraddr, MyTCPHandler)
	# Run the server forever.
	server.serve_forever()


# Create a server with the socket module (sentdex tutorial).
# @param, serveraddr: the server address, which contains the ip address
#	and port number.
# @return, returns nothing.
def createSockSentdex(serveraddr):
	headerLength = 10
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Configure the server socket so that we don't have to reuse the
	# address with setsockopt(). Here, you have three options. The
	# thing you want to set. What you want to set in that thing, and
	# then you set the thing.
	# SOL_SOCKET means Socket Option Level Socket.
	# SO_REUSEADDR means Socket Option Reuse Address.
	# The 1 means true.
	# So this means that we're setting the reusability of the socket's
	# address to be true.
	# This allows us to reconnect to the server.
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# Bind the address and port
	server.bind(serveraddr)

	# Start listening.
	server.listen()

	# List of sockets (clients). Includes server socket.
	socketList = [server]

	# CLients dictionary (socket is key and user data is the value).
	clients = {}

	while True:
		# Select.select() takes three parameters. The readlist which is
		# what you want to read in. The writelist which (in this case)
		# are sockets we want to write. The errorlist which are the
		# sockets we want to error on.
		# Our main concern are the readlist.
		readSockets, _, exceptionSockets = select.select(socketList,
														[], socketList)

		for notifiedSocket in readSockets:
			if notifiedSocket == server:
				# This means that someone just connected, and we need
				# to accept this connection and we need to handle for
				# it.
				clientSocket, clientAddress = server.accept()
				user = recieveMessage(clientSocket, headerLength)

				# If a user disconnected, continue.
				if user is False:
					continue

				# Otherwise, append the client socket to the list.
				socketList.append(clientSocket)

				clients[clientSocket] = user

				#print(f"Accepted new connection from {clientAddress[0]}:{clientAddress[1]} username: {user[data].decode("utf-8")}")

			else:
				# Read in the message from the client.
				message = recieveMessage(notifiedSocket, headerLength)

				# If the message is false.
				if message is False:
					# Print a closed connection message.
					#print(f"Closed connection from {clients[notifiedSocket]["data"].decode("utf-8")}")
					# Remove the client socket from the list and the 
					# clients dictionary.
					socketList.remove(notifiedSocket)
					del clients[notifiedSocket]
					# Then continue with the program.
					continue

				# Otherwise, print out the message that the server recieved.
				user = clients[notifiedSocket]
				#print(f"Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}")




# Receive messages.
# @param, clientSocket: the client socket sending the message.
# @param, headerLength: the max size of a header message.
# @return, returns either false for when the client has closed the
#	connection or a dictionary containing the header and message data.
def recieveMessage(clientSocket, headerLength):
	try:
		# Recieve the message header.
		messageHeader = clientSocket.recv(headerLength)

		# If we don't get any data on the header (client closed the
		# connection).
		if not len(messageHeader):
			# Handle this.
			return False

		# Get the message length.
		messageLength = int(messageHeader.decode("utf-8"))

		# Return a dictionary containing the header and the message
		# data from the client.
		return {"header": messageHeader,
				"data": clientSocket.recv(messageLength)}
	except Exception as e:
		# You should only hit this exception if someone broke their
		# script.
		return False




if __name__ == '__main__':
	main()
