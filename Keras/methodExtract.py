# methodExtract.py
# author: Diego Magdaleno
# Lists all methods, submethods, classes, and subclasses in a py file.
# Potential future application in program that re-writes itself.
# Python 3.6
# Linux

import sys


def main():
	# If there isn't a target file given (Note: target file must be in
	# same directory as program).
	if len(sys.argv) != 2:
		print("Error: Usage python methodExtract.py <targetfile>")
		exit(1)

	# Otherwise, load the file to memory.
	targetfile = sys.argv[1]
	ldFile = open(targetfile, "r")
	progLines = ldFile.readlines()
	ldFile.close()

	# Print lines for debug purposes.
	for line in progLines:
		print(line.strip("\n"))
	print("\n-----------------------\n")

	# Print functions and classes.
	printFuncClass(progLines)


def printFuncClass(lines):
	# A list of method and class headers to be printed.
	printLines = []

	# Iterate through the lines of the file.
	for line in lines:
		# If the line is a comment line, then ignore the line,
		if commentLine(line):
			continue
		# If there is only a "\n" in the line, then ignore the line.
		elif line == "\n":
			continue
		else:
			printLines.append(line)
		# 
		#if "def " in line:
		#else:
		#	line.split("")

	# Print the list of method and class headers.
	for header in printLines:
		print(header.strip("\n"))


# Determine if the line of code is a comment line (Not if it contains
# a comment).
def commentLine(line):
	# Strip all whitespace on the leftmost part of the string.
	line = line.lstrip()
	# If there is a "#" sign as the first character of the modified
	# string, then the line is a comment line.
	if len(line) > 0 and "#" in line[0]:
		return True
	return False


if __name__ == '__main__':
	main()