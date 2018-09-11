# bcServer.py
# full blockchain "snakecoin" server code

from flask import flask
from flask import request
import json
import requests
import hashlib as hasher
import datetime as date

# define block class
class Block:
	def __init__(self, index, timestamp, data, previous_hash):
		# block will store its index, a timestamp, data, and the previous hash
		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.previous_hash = previous_hash
		self.hash = self.hash_block()

	def hash_block(self):
		# function to hash a block (using sha256)
		sha = hasher.sha256()
		update = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
		#sha.update(str(self.index) + 
		#			str(self.timestamp) + 
		#			str(self.data) + 
		#			str(self.previous_hash))
		sha.update(update.encode("utf-8"))
		return sha.hexdigest()

	'''
	def create_genesis_block(first_data):
		# function to manually create a genesis (first) block in the blockchain
		# takes first_data as the argument to store the data in the block (must be a str)
		return Block(0, date.datetime.now(), first_data, "0")
	'''
	def create_genesis_block():
		return Block(0, date.datetime.now(), {
			"proof-of-work": 9,
			"transactions": None,
		}, "0")

	def next_block(last_block, new_data):
		# function that adds block to the blockchain
		this_index = last_block.index + 1
		this_timestamp = date.datetime.now()
		this_data = new_data + str(this_index)
		this_hash = last_block.hash
		return Block(this_index, this_timestamp, this_data, this_hash)

# completely random address of the owner of this node
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
# this node's blockchain copy
blockchain = []
blockchain.append(Block.create_genesis_block())
# store transactions that this node has in a list
this_nodes_transactions = []
# store url of every other node in the network so that we can 
# communicate with them
peer_nodes = []
# a variable that decides if we're mining or not
mining = True

@node.route('/txion', methods = ['POST'])
def transaction():
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
	# we then let the client know that it workedout
	return "Transaction submission successful\n"

def proof_of_work(last_proof):
	# create a variable that we will use to find our next proof of work
	incrementer = last_proof + 1
	# keep incrementing the incrementer until it is equal to a number 
	# divisible by 9 and the proof of work of the previous block in the
	# chain
	while not (incrementer % 9 == 0 and incrementer % last_proof == 0):
		incrementer += 1
	# once that number is found, we can store it as a proof of our work
	return incrementer

@node.route('/blocks', methods = ['GET'])
def get_blocks():
	chain_to_send = blockchain
	# convert our blocks into dictionaries so we can send them as json 
	# objects later
	for i in range(len(chain_to_send)):
		block = chain_to_send[i]
		block_index = str(block.index)
		block_timestamp = str(block.timestamp)
		block_data = str(block.data)
		block_hash = block.hash
		block = {
			"index": block_index,
			"timestamp": block_timestamp,
			"data": block_data,
			"hash": block_hash
		}
	# send our chain to whomever reqested it
	chain_to_send = json.dumps(chain_to_send)
	return chain_to_send

def find_new_chains():
	# get the blockchains of every other node
	other_chains = []
	for node_url in peer_nodes:
		# get their chains using a GET request
		block = requests.get(node_url + "/blocks")
		# convert the json object to a python dict
		block = json.loads(block)
		# add it to our list
		other_chains.append(block)
	return other_chains

def consensus():
	# get the blocks from the other nodes
	other_chains = find_new_chains()
	# if our chain isn't the longest, then we store the longest chain
	longest_chain = blockchain
	for chain in other_chains:
		if (len(longest_chain) < len(chain)):
			longest_chain = chain
	# if the longest chain wasn't ours, then we set our chain to the 
	# longest 
	blockchain = longest_chain

def proof_of_work(last_proof):
	# create a variable that we will use to find our next proof of work
	incrementer = last_proof + 1
	# keep incrementing the incrementer until it is equal to a number 
	# divisible by 9 and the proof of work of the previous block in the
	# chain
	while not (incrementer % 9 == 0 and incrementer % last_proof == 0):
		incrementer += 1
	# once that number is found, we can store it as a proof of our work
	return incrementer

@node.route('/mine', methods = ['GET'])
def mine():
	# get last proof of work
	last_block = blockchain[len(blockchain) - 1]
	last_proof = last_block.data['proof_of_work']
	# find proof of work for the current block being mined
	# note: the program will hang here until a new proof of work is 
	# found
	proof = proof_of_work(last_proof)
	# once we find a valid proof of work, we know we can mine a block 
	# or so we reward the miner by adding a transaction
	this_nodes_transactions.append(
		{"from": "network", "to": miner_address, "amount": 1}
	)
	# Now we can gather the data needed to create the new block
	new_block_data = {
		"proof-of-work": proof,
		"transactions": list(this_nodes_transactions)
	}
	new_block_index = last_block.index + 1
	new_block_timestamp = this_timestamp = date.datetime.now()
	last_block_hash = last_block.hash
	# empty transaction list
	this_nodes_transactions[:] = []
	# now create the new block
	mined_block = Block(
		new_block_index,
		new_block_timestamp,
		new_block_data,
		last_block_hash
	)
	blockchain.append(mined_block)
	# Let the client know we mined a block
	return json.dumps({
		"index": new_block_index,
		"timestamp": str(new_block_timestamp),
		"data": new_block_data,
		"hash": last_block_hash
	}) + "\n"