# p2pEx.py
# This is a python script meant to understand a basic LAN p2p system.
# Python 2.7
# Windows

import socket
import struct
import threading
import time
import traceback


class Peer(object):
	def __init__(self, maxpeers, serverport, myid=None,
				 serverhost=None):
		self.debug = 0

		# Set the maximum number of peers the node will maintain.
		# Set the server port number that the node will listen for.
		self.maxpeers = int(maxpeers)
		self.serverport = int(serverport)

		# If not supplied, the host name/IP address will be determined
		# by attempting to connect to an internet host like Google.
		if serverhost:
			self.serverhost = serverhost
		else:
			self.__initserverhost()

		# If not supplied, the peer id will be composed of the host
		# address and port number.
		if myid:
			self.myid = myid
		else:
			self.myid = '%s:%d' % (self.serverhost, self.serverport)

		# List(dictionary/hash table) of known peers.
		self.peers = []

		# Used to stop the main loop.
		self.shutdown = False

		self.handlers = {}
		self.router = None


	def mainloop(self):
		# Continously accept connections to the. Upon an incoming
		# is accepted, the server will have a new socket object used to
		# send and recieve data on the connection.
		s = self.makeserversocket(self.serverport)
		s.settimeout(2)
		self.__debug("Server started: %s (%s:%d)"
						% (self.myid, self.serverhost, self.serverport))

		'''
		while 1:
			clientsock, clientaddr = s.accept()

			t = threading.Thread(target=self.__handlepeer, args=[clientsock])
			t.start()
		'''

		while not self.shutdown:
			try:
				self.__debug("Listening for connections... ")
				clientsock, clientaddr = s.accept()
				clientsock.settimeout(None)

				t = threading.Thread(target=self.__handlepeer, args=[clientsock])
				t.start()				
			except KeyboardInterrupt:
				# Handle Ctrl+c where user stops the mainloop.
				self.shutdown = True
				continue
			except:
				if self.debug:
					traceback.print_exec()
					continue

		self.__debug("Exiting Main Loop")
		s.close()


	def makeserversocket(self, port, backlog=5):
		# Create new socket object. This will be using IPv4 protocol
		# with TCP (SOCK_STREAM).
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Set the socket's options. By setting the SO_REUSEADDR option,
		# the port number the socket is now reusable after the socket
		# is closed.
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# Bind socket to a port to listen for connections.
		s.bind(('', port))
		# Listen for connections. The backlog parameter is used to
		# indicate how many incoming connections should be queued up.
		# The value 5 is usually used as convention but in a
		# multithreaded server (what this is) the parameter value is
		# not very significant.
		s.listen(backlog)
		return s

	def __handlepeer(self, clientsock):
		self.__debug("Connected " + str(clientsock.getpeername()))

		host, port = clientsock.getpeername()
		peerconn = PeerConnection(None, host, port, clientsock,
								  debug=False)

		try:
			msgtype, msgdata = peerconn.recvdata()
			if msgtype:
				msgtype = msgtype.upper()
			if msgtype not in self.handlers:
				self.__debug("Not handled: %s: %s" 
					% (msgtype, msgdata))
			else:
				self.
		except KeyboardInterrupt:
			raise
		except:
			if self.debug:
				traceback.print_exec()