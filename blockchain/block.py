# Block.py
# simple block class for blockchain
# used with blockchain.py (for example)
# source code : https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b


# module for hashing
import hashlib as hasher
import block, datetime as date

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

	def create_genesis_block(first_data):
		# function to manually create a genesis (first) block in the blockchain
		# takes first_data as the argument to store the data in the block (must be a str)
		return Block(0, date.datetime.now(), first_data, "0")

	def next_block(last_block, new_data):
		# function that adds block to the blockchain
		this_index = last_block.index + 1
		this_timestamp = date.datetime.now()
		this_data = new_data + str(this_index)
		this_hash = last_block.hash
		return Block(this_index, this_timestamp, this_data, this_hash)