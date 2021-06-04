# fds_stylometry.py
# Source: https://fastdatascience.com/wp-content/uploads/2018/12/Forensic-Stylometry-for-Oxford.pdf


import nltk
import re
import string
import os
import json


def main():
	# Set the author to learn their fingerprints.
	author = ""

	# Load in document files (text samples) from one author.
	author_texts = load_documents(author)

	# Generate a fingerprint for each file. Each fingerprint includes
	# data such as word lengths, word frequencies, and word
	# co-occurences.
	author_fingerprints = {}
	for name, text in author_texts.items():
		# Initialize fingerprint datapoints for the document.
		frequencies = {}
		word_lengths = []
		word_cooccurences = []

		# Save fingerprint datapoints for the document.
		author_fingerprints[name] = {"frequencies": frequencies,
									"word_lengths": word_lengths,
									"word_cooccurences": word_cooccurences}

	# Save the fingerprint data.
	with open(author + "_document_fingerprints.json", "w+") as json_file:
		json.dump(author_fingerprints, json_file, indent=4)

	# For sylometry, consider Burrow's delta. Work out what percentage
	# of each author's corpus is taken up by each word. Compare this
	# statistic across authors.

	# Word occurances take word and character n-grams.

	# Exit the program.
	exit(0)


# Given an author, load all their texts from their respective directory
# into a dictionary, mapping the title of the document to its text.
# @param: author, (str) the name of the author and subsequently the 
#	directory that stores the respective documents.
# @return: returns a dictionary mapping the text names to their 
#	contents.
def load_documents(author):
	# If there is no folder for an author, just return an empty
	# dictionary.
	files_to_text = {}
	if not os.path.exists(author):
		return files_to_text

	# List all sample documents for an author from the folder.
	files = [file for file in os.listdir(author) 
			if os.path.isfile(author + "/" + file)]

	# Iterate through sample documents and load the texts into a
	# dictonary.
	for file in files:
		with open(author + "/" + file, "r") as open_file:
			files_to_text[file] = open_file.read()

	# Return the dictionary.
	return files_to_text


if __name__ == '__main__':
	main()