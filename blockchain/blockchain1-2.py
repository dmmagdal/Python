# blockchain.py
# program that creates a simple blockchain
# requires block.py module (no pip install available)
# source code : https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b

import block

# transaction data will be stored as a json object
# {
#		"to": "71238uqirbfh894-random-public-key-a-alkjdflakjfewn204ij",
#		"from": "93j4ivnqiopvh43-random-public-key-b-qjrgvnoeirbnferinfo"
#		"amount": 3
# }

# create blockchain/genesis block
b = block.Block
blockchain = [b.create_genesis_block("Starting block")]
previous_block = blockchain[0]

# number of blocks added to the chain after the genesis block
num_of_blocks_to_add = 20

# add blocks to chain
for i in range(num_of_blocks_to_add):
	block_to_add = b.next_block(previous_block, "I'm block number "+str(i))
	blockchain.append(block_to_add)
	previous_block = block_to_add

	# printing
	print("Block #{} has been added to the blockchain".format(block_to_add.index))
	print("Hash: {}\n".format(block_to_add.hash))

# added on myself. Not part of original code 
# iterate through to test to see if I can access the data in the blockchain
for j in range(len(blockchain)):
	print(blockchain[j].data)
	# appareblty, the data comes out as
	#		I'm block number 01
	#		I'm block number 12
	#		I'm block number 23
	#		I'm block number 34
	#		I'm block number 45
	#		...
	#		I'm block number 1920 <- this is the data (number) stored
	#						 /\
	#						 ||
	#						this is the index

# note: may have to find a way to parse data so that it doesn't come out merged like that