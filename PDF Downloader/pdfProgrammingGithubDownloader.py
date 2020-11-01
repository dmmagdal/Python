# pdfProgrammingGithubDownloader.py
# author: Diego Magdaleno
# Simple program that downloads programming pdf files from a github
# repository.
# Python 3.7
# Windows/MacOS/Linux


import time
import os
import sys
import zlib
import lzma
import json
import base64
import argparse
import requests
from bs4 import BeautifulSoup as bsoup
from datetime import datetime
from PyPDF2 import PdfFileReader, PdfFileWriter


# Scan for all the programming categories/topics/langauges in the
# Github repository.
# @param: takes no arguments.
# @return: returns a list of all categories/topics/programming
#	languages found in the Github repository.
def get_categories():
	# Initialize a list to hold the list of catagories/topics/languages
	# in the repository.
	categories_list = []

	# Send a request to the Github url.
	url = "https://github.com/EbookFoundation/free-programming-books/blob/" +\
			"master/free-programming-books.md"
	response = requests.get(url)

	# Check the status code of the response. Exit early if the status
	# code is not 200 ("Success").
	if response.status_code != 200:
		return categories_list

	# Load in the response content to BeautifulSoup and parse it.
	page_soup = bsoup(response.content, features="lxml")

	# Find all the headers. These contain the categories/topics/
	# langauges in the repository.
	header_tags = page_soup.find_all("h3")

	# Iterate through the headers and extract the text. Append those
	# text to the categories list. Ignore the "Index" and "Meta-Lists"
	# as those categories are not relevant or actual categories to
	# scrape from. Everything after those headers are valid.
	for header in header_tags[5:]:
		header_text = header.text
		categories_list.append(header_text)

	# Return the categories list.
	return categories_list


# Scan for all the available (directly downloadable pdf) texts by
# category name in the Github repository.
# @param: category_name, the (str) name of a category/topic/language
#	whose PDF books are to be retrieved.
# @return: returns a list of all PDF texts found in a specified category.
def get_books_by_category(category_name):
	# Initialize a list to hold the list of PDF texts found in a
	# catagory/topic/language in the repository.
	text_list = []

	# Send a request to the Github url.
	url = "https://github.com/EbookFoundation/free-programming-books/blob/" +\
			"master/free-programming-books.md"
	response = requests.get(url)

	# Check the status code of the response. Exit early if the status
	# code is not 200 ("Success").
	if response.status_code != 200:
		return text_list

	# Load in the response content to BeautifulSoup and parse it.
	page_soup = bsoup(response.content, features="lxml")

	# Find the article where the headers and their elements are
	# located.
	article_class_obj = {"class": "markdown-body entry-content container-lg"}
	article_tag = page_soup.find("article", article_class_obj)
	header_tags = article_tag.find_all("h3")[2:]

	# Find the index of the category from the list of categories in the
	# repository. Use this to isolate the header tag that the category
	# belongs to.
	category_index = get_categories().index(category_name)
	category_header_tag = header_tags[category_index]

	# Find all h3 and ul tags within the article.
	all_tags = article_tag.find_all(["h3", "ul"])

	# Using the category's header tag, iterate through the list of h3
	# and ul tags. All ul tags in between the category's (h3) header
	# tag and the next one will be scraped for their entries.
	category_tag_index = all_tags.index(category_header_tag)
	if category_index == len(header_tags)-1:
		all_tags_slice = all_tags[category_tag_index + 1:]
	else:
		next_category_tag = header_tags[category_index + 1]
		next_category_tag_index = all_tags.index(next_category_tag)
		all_tags_slice = all_tags[category_tag_index + 1:next_category_tag_index]

	# Iterate through the (ul) tags in the slice.
	for tag in all_tags_slice:
		# Extract the individual li elements within every (ul) tag.
		# Iterate through the resulting list and extract the titles of
		# each book in the li element.
		book_elements = tag.find_all("li")
		for book in book_elements:
			if book.a["href"].endswith(".pdf"):
				text_list.append(book.a.text)

	# Return the list of texts.
	return text_list


# Get a dictionary containing the complete mapping of categories to
# their list of (directly downloadable pdf) texts.
# @param: takes no arguments.
# @return: returns a (dict) mapping where the key is the category/
#	topic/programming language and the value is a list of directly
#	downloadable PDFs in that category.
def get_categories_to_books():
	# Initialize a dictionary to hold the mapping of categories to
	# texts.
	text_map = {}

	# Get the list of all categories.
	categories_list = get_categories()

	# Iterate through each category and retrieve the list of available
	# (as described in the function description) PDF texts in the
	# category.
	for category in categories_list:
		text_map[category] = get_books_by_category(category)

	# return the dictionary.
	return text_map


# Download the PDF given.
# @param: category, the (int) value of the category the text is
#	categorized under.
# @param: title, the (str) title of the text.
# @param: link, the (str) url extension to download the pdf text.
# @param: category_name, the (str) name of a category/topic/language
#	under which the PDF book belongs to.
# @return: returns whether the books is successfully downloaded and
#	saved or not (bool).
def download_text(title, link, category_name):
	# Check to see if the proper folder for the text exists. If it
	# doesn't, create it.
	folder_path = "./" + category_name.replace("/", "-")
	if not os.path.exists(folder_path):
		os.mkdir(category_name.replace("/", "-"))

	# Extract the text id from the download url extension. This will be
	# used to construct the url link to actually download the text in
	# pdf form.
	text_id = link.split("-")[-1][1:].strip(".html")

	# Send a request to the url link. May have to disable SSL
	# verification which poses a security risk when downloading the
	# PDFs. In the event of a dead or problematic link, return False.
	try:
		#response = requests.get(link)
		response = requests.get(link, verify=False)
	except:
		return False
	else:
		# Check the status code of the response. Exit early if the status
		# code is not 200 ("Success").
		if response.status_code != 200:
			return False

		# Save the response.
		saved_response = response.content

		# Save the pdf to the category's folder.
		title = title.replace("\"", "\'").replace("\\", "").replace("?", "")
		title = title.replace("/", "-").replace(":", " ")
		file = open(folder_path + "/" + title + ".pdf", "wb")
		file.write(saved_response) 
		file.close()

	# Return True.
	return True


# Download the pdf texts available by category.
# @param: category_name, the (str) name of a category/topic/language
#	whose PDF books are to be retrieved.
# @return: returns whether the books from the scrape were successfully
#	saved or not (bool).
def download_from_category(category_name):
	# Load in the mapping from all categories to their respective
	# texts.
	text_list = get_books_by_category(category_name)

	# Send a request to the Github url.
	url = "https://github.com/EbookFoundation/free-programming-books/blob/" +\
			"master/free-programming-books.md"
	response = requests.get(url)

	# Check the status code of the response. Exit early if the status
	# code is not 200 ("Success").
	if response.status_code != 200:
		return False

	# Load in the response content to BeautifulSoup and parse it.
	page_soup = bsoup(response.content, features="lxml")

	# Find the article where the headers and their elements are
	# located. Then find all li tags in the article.
	article_class_obj = {"class": "markdown-body entry-content container-lg"}
	article_tag = page_soup.find("article", article_class_obj)
	li_tags = article_tag.find_all("li")

	# Iterate through the list of found li tags. If the tag matches the
	# title text, download the pdf.
	for li in li_tags:
		if li.a.text in text_list:
			# Download the PDf text.
			download_status = download_text(li.a.text, li.a["href"],
											category_name)

		# XXX-TODO: Scrape from links in the Github pages that
		# advertise a PDF file but leads to an intermediate website.
		# The PDF is right there on the site's page from the url link
		# on Github, but the best way to extract it would be to look
		# for any href extensions on that page that end with ".pdf".
		# -XXX

	# Return True
	return True


# Download all readily available PDF texts from selected categories in
# the Github repository.
# @param: categories_list, a (list) of (valid) categories (str) that
#	are to have their respective collection of readily available texts
#	downloaded/saved. Default is None which downloads from all
#	categories.
# @return: returns whether the books from the scrape were successfully
#	saved or not (bool).
def download_from_categories(categories_list=None):
	# If the categories_list argument passed in was None (default
	# value), use that to signal that the function is to download from
	# all categories.
	if categories_list == None:
		categories_list = get_categories()

	# Verify that the categories_list is valid. Invalid categories
	# return False along with an error message being printed out.
	for topic in categories_list:
		if topic not in get_categories():
			print("Invalid category " + topic + " was entered.")
			return False

	# Iterate through the categories_list, downloading all readily
	# available texts from each category.
	for topic in categories_list:
		download_status = download_from_category(topic)

		# In the event a download was unsuccessful, return False and
		# print an error message.
		if not download_status:
			error_text = "Failed to download all readily available PDfs from "
			print(error_text + topic)
			return False

	# Return True.
	return True


# Compress a PDF file down to a XZ file.
# @param: file_name, the (str) path to a PDF file.
# @return: Returns a (bool) status as to whether the function was
#	successfully able to compress the file or not.
def compress_file(file_name):
	# Validate whether the file exists and that the file is a PDF.
	# Return False if it does not exist or is not a PDF and be sure to
	# print an error message.
	if not os.path.exists(file_name) or not file_name.endswith(".pdf"):
		print("File " + file_name + " is not a valid PDF file.")
		return False

	# Read from the file.
	old_file = open(file_name, "rb")
	data = old_file.read()
	old_file.close()

	# Change the filename so that it has the new file extension for
	# XZ file.
	new_file_name = file_name[:-4] + ".xz"

	# Compress the data. You can come back and change the compression
	# level (See Python docs for zlib.compress/.compressobj)
	COMPRESSION_LEVEL = 9
	compressed_data = base64.b64encode(zlib.compress(data, COMPRESSION_LEVEL))
	#compressed_data = lzma.LZMACompressor.compress(data, 
	#												preset=COMPRESSION_LEVEL)

	# Write to the new file.
	new_file = open(new_file_name, "wb")
	new_file.write(compressed_data)
	new_file.close()
	#new_file = lzma.LZMAFile(new_file_name, "wb")
	#new_file.write(compressed_data)
	#new_file.close()
	
	# Return True.
	return True


# Deompress a XZ file down to a PDF file.
# @param: file_name, the (str) path to a XZ file.
# @return: Returns a (bool) status as to whether the function was
#	successfully able to decompress the file or not.
def decompress_file(file_name):
	# Validate whether the file exists and that the file is a XZ file.
	# Return False if it does not exist or is not a XZ file and be sure
	# to print an error message.
	if not os.path.exists(file_name) or not file_name.endswith(".xz"):
		print("File " + file_name + " is not a valid xz file.")
		return False

	# Read from the file.
	old_file = open(file_name, "rb")
	data = old_file.read()
	old_file.close()
	#new_file = lzma.LZMAFile(old_file, "rb")
	#data = new_file.read()
	#new_file.close()

	# Change the filename so that it has the new file extension for
	# compressed file.
	new_file_name = file_name[:-3] + ".pdf"

	# Decompress the data. See Python docs for zlib.decompress/
	# .decompressobj)
	decompressed_data = zlib.decompress(base64.b64decode(data))
	#decompressed_data = lzma.LZMADecompressor.decompress(data)

	# Write to the new file.
	new_file = open(new_file_name, "wb")
	new_file.write(decompressed_data)
	new_file.close()
	
	# Return True.
	return True


# Extract the text from the PDF file. Note that the text will most
# likely be formatted properly so that it reads cleanly, but it is
# close enough to a clean format since these are "textbook" style
# books.
# @param: file_name, the (str) path to a PDF file.
# @return: returns the (str) text found in the file.
def get_text_from_pdf(file_name):
	# Initialize an empty string to hold all the file text and
	# return at the end of the function.
	file_text = ""

	# Validate whether the file exists and that the file is a PDF.
	# Return the empty string if it does not exist or is not a PDF and
	# be sure to print an error message.
	if not os.path.exists(file_name) or not file_name.endswith(".pdf"):
		print("File " + file_name + " is not a valid PDF file.")
		return file_text

	# Read from the file and get the number of pages that are in it.
	file = PdfFileReader(file_name)
	number_of_pages = file.getNumPages()

	# Iterate through each page. Create a page object based on the page
	# number index and extract the text from that page object. Append
	# that text to the once empty string that is going to be returned.
	for page_number in range(number_of_pages):
		page_obj = file.getPage(page_number)
		page_text = page_obj.extractText()
		file_text += page_text

	# Return the string containing the file text.
	return file_text


# Test all basic functions of the program.
# @param: test_list, a (list) of (valid) tests (str) to run. Default is
#	None which runs all tests.
# @return: returns nothing.
def test_functions(test_list=None):
	# Initialize a list containing the valid test names.
	valid_tests = ["Get categories", "Get category titles",
					"Get category to titles map", "Download a category",
					"Download all categories", "Compress file",
					"Decompress file"]

	# Check to see if the test_list is None. If it is, set the test
	# list to the list of valid test names.
	if test_list == None:
		test_list = valid_tests

	# Iterate through the test list and validate the test names. Any
	# invalid names result in an error being printed and the function
	# returning without any tests running.
	for test in test_list:
		if test not in valid_tests:
			print("Invalid test name " + test)
			print("Cancelling all tests...")
			return

	# Take note of when the tests start.
	program_start = datetime.now()
	print("Starting tests...")

	if "Get categories" in test_list:
		# Get a list of all categories/topics/languages found in this
		# repository.
		start = datetime.now()
		categories_list = get_categories()
		end = datetime.now()
		print("Category scan finished in {}".format(end - start))
		print("Number of categories in repository " +\
				str(len(categories_list)))
		print("Category values in list:")
		print(json.dumps(categories_list, indent=4))
		print()

	if "Get category titles" in test_list:
		# Get a list of all PDF books available found in select
		# category.
		start = datetime.now()
		TEST_CATEGORY = "Language Agnostic"
		text_list = get_books_by_category(TEST_CATEGORY)
		end = datetime.now()
		print("Trending-by-Category scan finished in {}".format(end - start))
		print("Number of readily available pdftexts in repository " +\
				str(len(text_list)))
		print("Book titles for Category:")
		print(json.dumps(text_list, indent=4))
		print()

	if "Get category to titles map" in test_list:
		# Create a mapping of each category to available book titles
		# per category.
		start = datetime.now()
		text_map = get_categories_to_books()
		end = datetime.now()
		print("Category-to-text mapping finished in {}".format(end - start))
		print("Category value to book name dictionary:")
		print(json.dumps(text_map, indent=4))
		print()

	if "Download a category" in test_list:
		# Download all texts from a category.
		start = datetime.now()
		TEST_CATEGORY = "C++"
		download_status = download_from_category(TEST_CATEGORY)
		end = datetime.now()
		print("Download-by-category finished in {}".format(end - start))
		print("Download-by-category status: {}"\
				.format("Success" if download_status else "Failed"))
		print()

	if "Download all categories" in test_list:
		# Download all texts for all categories.
		start = datetime.now()
		download_status = download_from_categories()
		end = datetime.now()
		print("Download-all-categories finished in {}".format(end - start))
		print("Download-all-categories status: {}"\
				.format("Success" if download_status else "Failed"))
		print()

	if "Compress file" in test_list:
		# Compress a selected PDF file.
		start = datetime.now()
		TEST_FILE = "./Ada/Ada Distilled.pdf"
		compression_status = compress_file("./Ada/Ada Distilled.pdf")
		end = datetime.now()
		print("File Compression finished in {}".format(end - start))
		print("File Compression status: {}"\
				.format("Success" if compression_status else "Failed"))
		print()

	if "Decompress file" in test_list:
		# Decompress a selected XZ file.
		start = datetime.now()
		TEST_FILE = "./Ada/Ada Distilled.xz"
		decompression_status = decompress_file("./Ada/Ada Distilled.xz")
		end = datetime.now()
		print("File Decompression finished in {}".format(end - start))
		print("File Decompression status: {}"\
				.format("Success" if decompression_status else "Failed"))
		print()

	# Take note of when these tests ended.
	program_end = datetime.now()
	print("Tests completed.")
	print("\nTests completed in {}\n".format(program_end - program_start))

	# Return the function.
	return


# Remove all directories and files that have been downloaded by the
# program.
# @param: takes no arguments.
# @return: returns nothing.
def clean():
	print("Cleaning files of downloaded content...")

	# Get the list of valid categories.
	valid_categories = get_categories()

	# List the contents of the current directory.
	current_directory = os.listdir()

	# Iterate through the list of valid categories.
	for topic in valid_categories:
		# If a category appears in the contents of the current
		# directory, remove all files inside the subdirectory and
		# delete the directory.
		if topic.replace("/", "-") in current_directory:
			subdir_contents = os.listdir("./" + topic.replace("/", "-"))
			for file in subdir_contents:
				os.remove("./" + topic.replace("/", "-") + "/" + file)
			os.rmdir("./" + topic.replace("/", "-"))

	print("Cleaining finished.")

	# Return the function.
	return


# Main program. Download and compress all readily available PDF files
# in the Github repository. Content downloaded may vary depending on
# arguments passed in. By default (no arguments), all content is
# downloaded.
# @param: takes no arguments.
# @return: returns nothing.
def main():
	# Initialize an argument parser.
	parser = argparse.ArgumentParser(conflict_handler="resolve")
	help_text = "This program downloads all readily available PDF files on" +\
				" programming from the Github repository https://github." +\
				"com/EbookFoundation/free-programming-books/blob/master/" +\
				"free-programming-books.md."
	test_text = "Run program tests. NOTE: All currently existing folders" +\
				" and files downloaded from the Github repository link will" +\
				" be removed after the test. Please move any content you" +\
				" wish to save in a temporary directory until after the" +\
				" program tests have been completed."
	download_text = "Download all readily available PDFs from select" +\
					" categories."
	categories_text = "Retrieve the list of all categories/topics/" +\
						"langauges covered in the Github repository."
	compress_text = "Compress a PDF file."
	decompress_text = "Decompress a XZ file."
	clean_text = "Remove all content downloaded from the Github repository"
	parser.add_argument("-h", "--help", help=help_text, action="help")
	#parser.add_argument("-T", "--test", help=test_text, action="store_true")
	parser.add_argument("-T", "--test", help=test_text, type=str, nargs="*", default=None)
	parser.add_argument("-C", "--categories", help=categories_text, action="store_true")
	parser.add_argument("-D", "--download", help=download_text, type=str, nargs="*", default=None)
	parser.add_argument("-c", "--compress", help=compress_text, type=str, default="")
	parser.add_argument("-d", "--decompress", help=decompress_text, type=str, default="")
	parser.add_argument("-F", "--clean", help=clean_text, action="store_true")
	args = parser.parse_args()

	# Check the command line arguments.
	if args.test != None:
		# Run a test of all the functions, then clean the file system.
		if args.test == []:
			test_functions()
		else:
			test_functions(args.test)
		clean()
	if args.categories:
		# Print out the list of all valid categories/topics/languages.
		print("Programming categories/topics/languages found:")
		print(json.dumps(get_categories(), indent=4))
	if args.download != None:
		# Download all the selected content from the repository.
		if args.download == []:
			args.download = None
		start = datetime.now()
		download_status = download_from_categories(args.download)
		end = datetime.now()
		print("Download finished in {}".format(end - start))
		print("Download status: {}"\
				.format("Success" if download_status else "Failed"))
	if args.compress != "":
		# Compress the file and remove its original.
		compression_status = compress_file(args.compress)
		print("File compression status: {}"\
				.format("Success" if compression_status else "Failed"))
		if compression_status:
			os.remove(args.compress)
	if args.decompress != "":
		# Decompress the file and removed the old compressed file.
		decompression_status = decompress_file(args.decompress)
		print("File decompression status: {}"\
				.format("Success" if decompression_status else "Failed"))
		if decompression_status:
			os.remove(args.decompress)
	if args.clean:
		# Clean the file system.
		clean()

	# Return the function.
	return


if __name__ == '__main__':
	# Run the main function.
	main()

	# Exit the program.
	exit(0)