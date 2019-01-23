# methodExtract.py
# author: Diego Magdaleno
# Lists all methods, submethods, classes, and subclasses in a py file.
# Potential future application in program that re-writes itself.
# Python 3.6
# Linux

import sys


def main():
	# If there isn't a target file given (Note: target file must be in
	# same directory as program) then give an error message and exit.
	if len(sys.argv) != 2:
		print("Error: Usage python methodExtract.py <targetfile>")
		exit(1)

	# Otherwise, load the file to memory.
	targetfile = sys.argv[1]
	ldFile = open(targetfile, "r")
	progLines = ldFile.readlines()
	ldFile.close()

	# Print the whole program for debug purposes.
	for line in progLines:
		print(line.strip("\n"))
	print("\n-----------------------\n")

	# Print functions and classes.
	printFuncClass(progLines)

	# Print if file uses spaces or tabs.
	spaceTabVar = spaceOrTabs(progLines)
	print("Spaces or Tabs: "+spaceTabVar)
	numSpaces = None

	# If the file uses spaces, find out how many 
	if spaceTabVar == "spaces":
		# Print number of spaces in an indentation.
		numSpaces = printIndentSpaces(progLines)

	print("\n-----------------------\n")

	# Create an outline of the program.
	outlineProgram(progLines, spaceTabVar, numSpaces)


# Print out all function and class headings in the program.
def printFuncClass(lines):
	# A list of method and class headers to be printed.
	printLines = []

	# Iterate through the lines of the file and find what lines are
	# method declarations and class declarations.
	for line in lines:
		# If the line is a comment line, then ignore the line,
		if commentLine(line):
			continue
		# If there is only a "\n" in the line, then ignore the line.
		elif line == "\n":
			continue
		# If there is the string "def " or "class " in the line, then
		# the line is declaring a function/method or a class.
		elif methodLine(line) or classLine(line):
			# Append the line.
			printLines.append(line)

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


# Determine if the line of code is a method declaration.
def methodLine(line):
	# Strip all whitespace on the leftmost part of the string.
	line = line.lstrip()
	# If "def " is the first character of the modified string, then the
	# line is a comment line.
	if "def " == line[:4]:
		return True
	return False


# Determine if the line of code is a class declaration.
def classLine(line):
	# Strip all whitespace on the leftmost part of the string.
	line = line.lstrip()
	# If "def " is the first character of the modified string, then the
	# line is a comment line.
	if "class " == line[:6]:
		return True
	return False


# Determine if the program uses spaces or tabs for indentation.
def spaceOrTabs(lines):
	# Return variable that details whether spaces or tabs are being
	# used.
	spacingVar = None
	# Iterate through the program lines.
	for line in lines:
		# Remove leading whitespace and store modified string to
		# temporary variable.
		linePrime = line.lstrip()
		# Compare the length of the two strings. If they differ, then
		# check the character in the first index of the original
		# string.
		if len(line) - len(linePrime) != 0:
			firstSpace = line[0]
			# If the first character in the string is a "\t", then set
			# the return variable to "tabs" and exit the loop.
			if firstSpace == "\t":
				spacingVar = "tabs"
				break
			# Otherwise, if the first character in the string is a " ",
			# then set the return variable to "spaces" and exit the
			# loop.
			elif firstSpace == " ":
				spacingVar = "spaces"
				break
	# Return the variable.
	return spacingVar


# Returns and prints the number of spaces being used for an indent
# (only needed for when spaces are being used instead of tabs).
def printIndentSpaces(lines):
	# Variable to store the lowest number of spaces used in an
	# indentation (Depending on conventions, should be 2, 3, or 4).
	numSpaces = None
	# Iterate through the program lines. 
	for line in lines:
		# Remove the leading whitespace and store the modified string.
		strippedLine = line.lstrip()
		# Subtract the length of the modified string from the length
		# of the orginal. This should tell how many (whitespace)
		# characters were in front of the string.
		diff = len(line) - len(strippedLine)
		# Establish boolean variables for the conditionals.
		cond1 = diff != 0 and numSpaces == None
		cond2 = diff != 0 and numSpaces != None
		cond3 = diff < numSpaces
		# If there is a difference between the modified string and the
		# original AND the numSpaces variable does not have a value.
		if cond1:
			# Set the numSpaces variable to that difference.
			numSpaces = diff
		# Otherwise, if there is a difference between the modified
		# string and the original AND the numSpaces variable has an
		# assigned value AND that difference is less than the current
		# assigned value of numSpaces.
		elif cond2 and cond3:
			# Replace the numSpaces value with the lower value.
			numSpaces = diff
	# Print out how many spaces there are in an indentation.
	spaceString = "The smallest number of spaces in and indentation are "
	print(spaceString+str(numSpaces))
	# Return the numSpaces variable.
	return numSpaces


# Prints out and outline of the program where the method and class
# declarations are listed.
def outlineProgram(lines, spaceTabVar, numSpaces):
	print("Program Outline:")
	# Iterate through the program lines.
	for line in lines:
		# If the line is a method or class declaration.
		if methodLine(line) or classLine(line):
			# Format the line accordingly.
			formatOutline(line, spaceTabVar, numSpaces)


# Format a line so that it represents an accurate outline of the
# program.
def formatOutline(line, spaceTabVar, numSpaces):
	# If the program uses tabs.
	if spaceTabVar == "tabs":
		# Replace all "\t" characters with "#" (should see only leading
		# tabs, otherwise the programmer is doing something weird). 
		print(line.replace("\t","#").strip("\n"))
	# Otherwise (uses spaces).
	else:
		# Create a string that represents our indentation spacing.
		space = numSpaces * " "
		# Replace all indent spacing represented by the string above
		# with "#" (should remove for all leading spaces, otherwise
		# the programmer is doing something weird).
		print(line.replace(space, "#"))


if __name__ == '__main__':
	main()
