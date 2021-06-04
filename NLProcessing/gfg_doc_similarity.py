# gfg_doc_similarity
# Source: https://www.geeksforgeeks.org/measuring-the-document-similarity-in-python/


import math
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

	# Create a dictionary mapping words/tokens to the respective word
	# frequency in both documents.
	# key: str(token), value: list(freq_doc1, freq_doc2)
	bag_of_words = {}
	for line in clean_f1_contents:
		for word in line:
			if word not in bag_of_words:
				bag_of_words[word] = [0, 0]
			bag_of_words[word][0] += 1

	for line in clean_f2_contents: 
		for word in line:
			if word not in bag_of_words:
				bag_of_words[word] = [0, 0]
			bag_of_words[word][1] += 1

	# Calculate dot product to get the document distance.
	sum_val = 0.0
	for key in bag_of_words:
		if bag_of_words[key][0] != 0 and bag_of_words[key][1] != 0:
			sum_val += (bag_of_words[key][0] * bag_of_words[key][1])

	# Calculate the angle (in radians) between the document vectors.
	numerator = sum_val # dot product of the two document vectors.
	denominator = math.sqrt(sum_val * sum_val)
	angle = math.acos(numerator / denominator)

	print("Document 1: ")
	print("Number of lines in document: {}".format(len(clean_f1_contents)))
	print("Number of original words in document: {}".format(len([key for key in bag_of_words if bag_of_words[key][0] != 0])))
	print("Number of words unique to document: {}".format(len([key for key in bag_of_words if bag_of_words[key][0] != 0 and bag_of_words[key][1] == 0])))
	print("Document 2: ")
	print("Number of lines in document: {}".format(len(clean_f2_contents)))
	print("Number of original words in document: {}".format(len([key for key in bag_of_words if bag_of_words[key][0] != 0])))
	print("Number of words unique to document: {}".format(len([key for key in bag_of_words if bag_of_words[key][1] != 0 and bag_of_words[key][0] == 0])))
	print("The distance between documents %0.6f (radians) " % angle)

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