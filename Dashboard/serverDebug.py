# serverDebug.py
# author: Diego Magdaleno
# Not a part of the main dashboard program, this script tests the
# server's responses to requests, including invalid and valid requests.
# Python 3.6
# Linux


import requests
import unittest
import json


# Host variables
#defaultHost = '0.0.0.0'
defaultHost = 'localhost'
assignedHost = 'raspberrypi.local'

# User variables
username = None
password = None


class BasicServerTests(unittest.TestCase):
	# Test LoadHistoric requests.
	def test1_LoadHistoric(self):
		# Send get request to server.
		req1 = requests.get('http://'+defaultHost+':8888/historic/msft',
				json={'user': username, 'password': password})
		# Load json response.
		req1Response = req1.json()
		print(req1Response)
		print(req1.status_code)
		self.assertEqual(req1.status_code, 200)



if __name__ == '__main__':
	unittest.main()
