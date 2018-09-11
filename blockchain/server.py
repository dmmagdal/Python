# server.py
# program creates a simple http server to let blockchain nodes know
# that a transaction has occured. It will be able to accept that a post
# request with a transaction as the request body (hence why the 
# transactions are json formatted)
# requires block.py and blockchain(1-1, 1-3).py
# source code: https://medium.com/crypto-currently/lets-make-the-tiniest-blockchain-bigger-ac360a328f4d

from flask import Flask
from flask import request

# store transaction that this node has in a list
this_nodes_transactions = []

@node.route('/txion', methods = ['POST'])
def transaction():
	if request.method == 'POST':
		# on each new POST request, we extract the tranaction data
		new_txion = request.get_json()
		# then add the transaction to the list
		this_nodes_transactions.append(new_txion)
		# because new transaction was successfully submitted, we log it
		# to our console
		print("New transaction")
		print("FROM: {}".format(new_txion['from']))
		print("TO: {}".format(new_txion['to']))
		print("AMOUNT: {}".format(new_txion['amount']))
		# we then let the client know that we worked it out
		return "Transaction submission successful\n"

node.run()