# miner.py

import block
import blockchain

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

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