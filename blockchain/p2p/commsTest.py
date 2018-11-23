# commsTest.py
# author: Diego Magdaleno
# Simple program that uses sockets to check and see if two devices can
# talk to eachother on the same network given their ip addresses.

import sys
import socket


def main():
	# Check to make sure there are correct number of arguments.
	if len(sys.argv) != 2:
		print("Usage: python commsTest.py <-s,c>")
		exit(1)

	# If user typed in -s for server mode, launch server method.
	if sys.argv[1] == "-s":
		beginServer()
	# If user typed in -c for client mode, launch client method.
	elif sys.argv[1] == "-c":
		beginClient()
	# Else, send error message and close program.
	else:
		print("Usage: python commsTest.py <-s,c>")
		exit(1)


def beginServer():
	# Create socket and use bind() to associate with the server's
	# address. localhost is server's current address, port is 10000.
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_addr = ('localhost', 10000)
	print("Starting server on %s port %s" %server_addr)
	socket.bind(server_addr)

	# Put server into listen mode with listen() and accept incoming
	# connections with accept(). The accept() method returns an open
	# connection between the server and client, along iwth the address
	# of the client. The connection is actually a different socket on
	# another port assigned by the kernel. 
	s.listen(1)
	while True:
		print("Waiting for a connection.")
		connection, client_addr = s.accept()

		try:
			print("Connection from %s" client_addr)

			# Data is read from the connection with recv() and
			# transmitted with sendall().
			while True:
				data = connection.recv(16)
				print("Recieved %s" %data)
				if data:
					print("Sending data back to the client")
					connection.sendall(data)
				else:
					print("No more data from", client_addr)
					break
		finally:
			connection.close()
	# When communication with the client is finished, connections
	# need to be cleaned up with close()


def beginClient():
	# Socket for client is set up differently, instead attaching to
	# the socket directly to the remote address with connect().
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv_addr = str(input("Enter the server's address: "))
	port = str(input("Enter the port number: "))
	server_addr = (serv_addr, port)
	print("Connecting to %s port %s" % server_addr)

	try:
		# After connection is established, data can be sent through
		# the socket with sendall() and recieved with recv() just as in
		# the server.
		message = "This is a message. It will be repeated."
		print("Sending %s" % message)
		s.sendall(message)

		# Look for response.
		amount_recvd = 0
		amount_exptd = len(message)

		while amount_recvd < amount_exptd:
			data = s.recv(16)
			amount_recvd += len(data)
			print("Recieved %s" % data)
	finally:
		print("Closing socket")
		s.close()


if __name__ == '__main__':
 	main() 