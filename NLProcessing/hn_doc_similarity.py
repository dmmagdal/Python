# hn_doc_similarity
# Source: https://hackernoon.com/compare-documents-similarity-using-python-or-nlp-0u3032eo


import string
import re
import json


def main():
	# Open documents.
	with open("", "r") as file1:
		file1_contents = file1.readlines()
	with open("", "r") as file2:
		file2_contents = file2.readlines()

	# Clean file lines:
	clean_f1_contents = []
	clean_f2_contents = []
	for line in file1_contents:
		clean_f1_contents.append(tokenize_line(line))
	for line in file2_contents:
		clean_f2_contents.append(tokenize_line(line))

	# Create a dictionary mapping words/tokens to a token id and their
	# respective frequency in both documents.
	# key: str(token), value: list(token_id, freq_doc1, freq_doc2)
	bag_of_words = {}
	token_id = 0
	for line in clean_f1_contents:
		for word in line:
			if word not in bag_of_words:
				bag_of_words[word] = [token_id, 0, 0]
				token_id += 1
			bag_of_words[word][1] += 1

	for line in clean_f2_contents: 
		for word in line:
			if word not in bag_of_words:
				bag_of_words[word] = [token_id, 0, 0]
				token_id += 1
			bag_of_words[word][2] += 1

	# Save bag of words.
	with open("bag_of_words_analysis.json", "w+") as json_file:
		json.dump(bag_of_words, json_file, indent=4)
	'''
	# Create a dictionary of token ids (map word -> unique id).
	token_ids = {}
	id_value = 0
	for line in clean_f1_contents + clean_f2_contents:
		for word in line:
			if word not in token_ids:
				token_ids[word] = id_value
				id_value += 1

	# Create a bag of words (dictionary mapping word id -> frequency
	# for each document).
	for token in token_ids:
		token_ids[token] = [0, 0]
	for line in clean_f1_contents:
		for word in line:
			token_ids[word][0] += 1
	for line in clean_f2_contents:
		for word in line:
			token_ids[word][1] += 1
	'''

	# Exit the program.
	exit(0)


def tokenize_line(line):
	# Tokenize a line of code (remove all whitespace and punctuation).
	regex = re.compile("[%s]" % re.escape(string.punctuation))
	new_line = regex.sub(" ", line).split()
	while "" in new_line:
		new_line.remove("")
	return new_line


if __name__ == '__main__':
	main()