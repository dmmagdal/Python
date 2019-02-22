# methodExtractRefined.py
# author: Diego Magdaleno
# Refined version of methodExtract.py
# Lists all methods, submethods, classes, and subclasses in a py file.
# Potential future application in program that re-writes itself.
# Only looks at a single py file.
# Python 3.6
# Linux


import sys
import os


def main():
	# If there isn't a target file given (Note: target file must be in
	# same directory as program) then give an error message and exit.
	if len(sys.argv) != 2:
		print("Error: Usage python methodExtract.py <targetfile>")
		exit(1)

	# Determine if file exists and is python file.
	if not validInput(sys.argv[1]):
		print("Error: Please use a valide file (path)")
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

	# Good for debuging.
	# Print functions and classes.
	#printFuncClass(progLines)

	# Print if file uses spaces or tabs.
	spaceTabVar = spaceOrTabs(progLines)
	print("Spaces or Tabs: "+spaceTabVar)
	numSpaces = 0

	# If the file uses spaces, find out how many 
	if spaceTabVar == "spaces":
		# Print number of spaces in an indentation.
		numSpaces = printIndentSpaces(progLines)

	print("\n-----------------------\n")

	# Create an outline of the program.
	outlineProgram(progLines, spaceTabVar, numSpaces)


# Determine if file exists and is python file.
# @param, file: the file (path) given by the user in the command
#	arguments.
# @return, returns whether a file exists, it is a file, and if the file
#	is a py file.
def validInput(file):
	# Does the file exist.
	cond1 = os.path.exists(file)
	# Is the file a file.
	cond2 = os.path.isfile(file)
	# Is the file a py file.
	cond3 = ".py" == file[len(file)-3:]
	return cond1 and cond2 and cond3


# Print out all function and class headings in the program.
# @param, lines: the list of lines contained by the py file.
# @return, returns nothing.
def printFuncClass(lines):
	# A list of method and class headers to be printed.
	printLines = []

	# Iterate through the lines of the file and find what lines are
	# method declarations and class declarations.
	for line in lines:
		# If there is the string "def " or "class " in the line, then
		# the line is declaring a function/method or a class.
		if methodLine(line) or classLine(line):
			# Append the line.
			printLines.append(line)
		# Otherwise, ignore all other lines. Note: we are assuming that
		# the method and class declaration lines are all done in the
		# same line.

	# Print the list of method and class headers.
	for header in printLines:
		print(header.strip("\n"))


# Determine if the line of code is a method declaration.
# @param, line: the (method or class declaration) line that is to be
# 	parsed by the method.
# @return, returns whether or not a line is a method declaration.
def methodLine(line):
	# Strip all whitespace on the leftmost part of the string.
	line = line.lstrip()
	# If "def " is the first character of the modified string, then the
	# line is a comment line.
	return "def " == line[:4]


# Determine if the line of code is a class declaration.
# @param, line: the (method or class declaration) line that is to be
# 	parsed by the method.
# @return, returns whether or not a line is a class declaration.
def classLine(line):
	# Strip all whitespace on the leftmost part of the string.
	line = line.lstrip()
	# If "def " is the first character of the modified string, then the
	# line is a comment line.
	return "class " == line[:6]


# Determine if the program uses spaces or tabs for indentation.
# @param, lines: the list of (method or class declaration) lines that
# 	are to be parsed by the method.
# @return, returns a string flag that details whether the py file is
#	using spaces or tabs.
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
# @param, lines: the list of (method or class declaration) lines that
# 	are to be parsed by the method.
# @return, returns number of spaces (int) being used for an indent.
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
# @param, lines: the list of (method or class declaration) lines that
# 	are to be formated according to the method.
# @param, spaceTabVar: the string that tells if the py file was using
#	spaces or tabs.
# @param, numSpaces: if the py file was using spaces, this variable
#	shows how many spaces they were using (either 2, 3, or 4 usually).
# @return, returns nothing.
def outlineProgram(lines, spaceTabVar, numSpaces):
	print("Program Outline:")
	# List of all lines containing method or class declarations.
	declarationList = []
	# Iterate through the program lines, storing the method and class
	# declarations to the above list.
	# Format (line, line index, number of indents, end of declaration
	# index).
	for i in range(len(lines)):
		line = lines[i]
		# If the line is a method or class declaration.
		if methodLine(line) or classLine(line):
			# Count the number of indents
			numIndent = countIndents(line, spaceTabVar, numSpaces)
			# Append line and relavent information to the list.
			declarationList.append([line, i+1, numIndent, 0])

	# Iterate through one more time. This time, find the value of the
	# ending index of each declaration line.
	for dec in declarationList:
		# The starting index of the declaration line (is actually the
		# line after when looking at the lines list).
		start = dec[1]
		# Iterate through the original list of lines starting from that
		# index going to the end.
		for j in range(start, len(lines)):
			# Get the number of indentations for the line.
			lineIndent = countIndents(lines[j], spaceTabVar, numSpaces)
			# If that number is less than or equal to the number of 
			# indentations in the declaration line.
			if lineIndent <= dec[2] and lines[j] != "\n":
				# Set the declaration line's ending index to be the
				# current index (this is actually the line before the
				# referenced line in the actual file).
				dec[3] = j
				break

	# We have all "necessary" information now. Print and format the data.
	for heading in declarationList:
		# Format the line accordingly.
		formatOutline(heading, spaceTabVar, numSpaces)


# Count how many indents were used in the line given the spaceTabVar.
# @param, line: the (method or class declaration) line that is to be
# 	parsed the method.
# @param, spaceTabVar: the string that tells if the py file was using
#	spaces or tabs.
# @param, numSpaces: if the spaceTabVar is spaces, this is the number
#	of spaces used in an indent.
# @return returns the number (int) of indents used in the given line.
def countIndents(line, spaceTabVar, numSpaces):
	# Number of indents.
	indentsNum = 0
	# Indent string.
	indentStr = ""
	# If tabs were used to indent.
	if spaceTabVar == "tabs":
		indentStr = "\t"
	# Otherwise, spaces were used.
	else:
		indentStr = " " * numSpaces
	# Split the line string.
	lineList = line.split(indentStr)
	# Iterate through the list created by the split. Increment counter
	# until encountering a non-blank string.
	for string in lineList:
		if string != "":
			break
		else:
			indentsNum += 1
	# Return the number of indents.
	return indentsNum


# Format a line so that it represents an accurate outline of the
# program.
# @param, heading: contains all the data from the (method or class 
#	declaration) line that is to be formated according to the method.
# @param, spaceTabVar: the string that tells if the py file was using
#	spaces or tabs.
# @param, numSpaces: if the py file was using spaces, this variable
#	shows how many spaces they were using (either 2, 3, or 4 usually).
# @return, returns nothing.
def formatOutline(heading, spaceTabVar, numSpaces):
	# Store the string of the line in the variable line.
	line = heading[0]
	# Store the beginning and ending index of the line.
	start = str(heading[1])
	end = str(heading[3])
	# String attachment to print statement below.
	attach = "\tLines "+start+" to "+end
	# If the program uses tabs.
	if spaceTabVar == "tabs":
		# Replace all "\t" characters with "#" (should see only leading
		# tabs, otherwise the programmer is doing something weird). 
		print(line.replace("\t","---").strip("\n"))
	# Otherwise (uses spaces).
	else:
		# Create a string that represents our indentation spacing.
		space = numSpaces * " "
		# Replace all indent spacing represented by the string above
		# with "#" (should remove for all leading spaces, otherwise
		# the programmer is doing something weird).
		print(line.replace(space, "---").strip("\n"))
	#print(attach)


if __name__ == '__main__':
	main()
