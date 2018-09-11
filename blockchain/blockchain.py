# blockchain.py
# program that creates a simple blockchain
# requires block.py module (no pip install available)
# source code : https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b

import block

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