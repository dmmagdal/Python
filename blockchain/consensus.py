# consensus.py

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