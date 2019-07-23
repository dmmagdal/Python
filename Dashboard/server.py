# server.py
# author: Diego Magdaleno
# Actual Flask app server used to handle requests from the desktop
# client and provide as much up to date info as possible.
# Python 3.6
# Linux


from flask import Flask, jsonify
from flask_restful import Resource, Api
from serverHelper import validTicker, validUser
import json


# Class to handle requests for historic data.
class LoadHistoric(Resource):
	def get(self, ticker):
		# See if the user is valid. If so, get their id hash.
		# 
		#userSearch = validUser()
		#if not userSearch:
		#	return jsonify({'message': 'Invalid user'})

		# See if ticker is valid. If so, what market is it associated
		# with? Store results to tickerSearch
		tickerSearch = validTicker(ticker)
		# return jsonify({'tickervalid': tickerSearch[0],
		# 				'market':tickerSearch[1]})
		# If the ticker is not valid, return this message.
		if not tickerSearch[0]:
			return jsonify({'message': 'Invalid ticker'})
		# Otherwise, send the csv containing the ticker's historic data.
		return jsonify({'message': 'Valid ticker'})

# Class to handle requests for current/live data.
class LoadCurrent(Resource):
	def get(self, ticker):
		pass

# Class to handle requests for prediction models.
class LoadPrediction(Resource):
	def get(self, ticker):
		pass

# Class to handle requests for orders.
class SendOrder(Resource):
	def put(self, orders):
		pass

	def delete(self, orders):
		pass


# Initialize app and api
app = Flask(__name__)
api = Api(app)

# Add resources directing to class.
api.add_resource(LoadHistoric, "/historic/<string:ticker>")
api.add_resource(LoadCurrent, "/current/<string:ticker>")
api.add_resource(LoadPrediction, "/prediction/<string:ticker>")
#api.add_resource(SendOrder, "/order/<dictionary:orders>")


if __name__ == '__main__':
	defaultHost = '0.0.0.0'
	assignedHost = 'raspberrypi.local'
	app.run(host=defaultHost, port = 8888, debug=True)
