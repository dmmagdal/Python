# pdfDriveDownloader.py
# author: Diego Magdaleno
# Simple program that downloads the top trending pdf files on a given
# subject.
# Python 3.7
# Windows/MacOS/Linux


import time
import os
import sys
import zlib
import lzma
import json
import requests
from bs4 import BeautifulSoup as bsoup
from datetime import datetime


# Scan for all the top categories in the PDFDrive website.
# @param: takes no arguments.
# @return: returns a dictionary where the keys are the category numbers
#	and the values are the corresponding category names.
def get_categories():
	# Initialize a (constant) variable to store the highest possible
	# category value in the PDFDrive site.
	MAX_CATEGORY_VALUE = 100

	# Initialize the dictionary mapping category values to their
	# respective names/labels. For each category value (key), assign
	# an empty string (value).
	category_value_to_label = {key: "" for key in range(1, MAX_CATEGORY_VALUE + 1)}

	# Iterate over the range of possible category values, and scrape
	# the category strings that correspond to those values.
	for category_value in range(1, MAX_CATEGORY_VALUE + 1):
		# Send a request using the constructed PDFDrive url.
		url = "https://www.pdfdrive.com/category/" + str(category_value) + "/"
		response = requests.get(url)

		# Check the status code of the response. Exit early if the status
		# code is not 200 ("Success").
		if response.status_code != 200:
			continue

		# Load in the response content to BeautifulSoup and parse it.
		page_soup = bsoup(response.content, features="lxml")

		# Isolate and acquire the tag that contains text describing what
		# topic the category number maps to.
		topic_tag = page_soup.find("div", {"class": "collection-title"})
		if topic_tag == None:
			continue

		# Extract and clean the text containing the topic. Save the
		# value to the dictionary.
		topic_tag_text = topic_tag.text.replace("\n", "").rstrip(" ")
		TOPIC_HEADER_TEXT = "Trending eBooks about "
		category_name = topic_tag_text[len(TOPIC_HEADER_TEXT):]
		category_value_to_label[category_value] = category_name

	# Return the dictionary.
	return category_value_to_label


# Scan for all the top trending texts by category number in the
# PDFDrive website.
# @param: takes no arguments.
# @return: returns a dictionary where the keys are the category numbers
#	and the values are a list of top trending book names for those
#	corresponding category numbers.
def get_trending_by_category():
	# Initialize a (constant) variable to store the highest possible
	# category value in the PDFDrive site.
	MAX_CATEGORY_VALUE = 100

	# Initialize the dictionary mapping category values to their
	# respective lists of top trending books/texts. For each category
	# value (key), assign an empty list (value).
	category_value_to_texts = {key: [] for key in range(1, MAX_CATEGORY_VALUE + 1)}

	# Load in the mapping from all category values to their respective
	# topics. This should take about a minute. This will be used to
	# optimize the search.
	category_value_to_label = get_categories()

	# Iterate over the range of possible category values, and scrape
	# the category strings that correspond to those values.
	for category_value in range(1, MAX_CATEGORY_VALUE + 1):
		# Before even sending the request to PDFDrive, check the
		# dictionary mapping the category values to names. If the
		# category name is an empty string, scraping the site for that
		# category will provide nothing, so skip this category value.
		if category_value_to_label[category_value] == "":
			continue

		# Send a request using the constructed PDFDrive url.
		url = "https://www.pdfdrive.com/category/" + str(category_value) + "/"
		response = requests.get(url)

		# Check the status code of the response. Exit early if the status
		# code is not 200 ("Success").
		if response.status_code != 200:
			continue

		# Load in the response content to BeautifulSoup and parse it.
		page_soup = bsoup(response.content, features="lxml")

		# First, count the number of pages in the results page. Look at
		# the pagination tag for this information.
		pagination_tag = page_soup.find("div", {"class": "pagination"})
		if pagination_tag == None:
			continue
		
		# Check the number of li tags within the pagination tag. If
		# there are no li tags in the initial list, then there is only
		# one page to scrape from. Otherwise, look at the last li tag
		# after removing the ones containing the "Previous" and "Next"
		# values as text. That value will be used to count the number
		# of pages to scrape.
		page_links = pagination_tag.find_all("li")
		num_pages = 0
		if len(page_links) == 0:
			num_pages = 1
		else:
			page_links = page_links[1:-1]
			num_pages = int(page_links[-1].text)

		# Initialize the list to contain the titles of books/texts
		# found on the trending page(s).
		trending_titles = []

		# Iterate through the range of possible pages. Use the values
		# to create the url extensions for every page. Extract the
		# extensions to create new urls and scrape the tiles from each
		# page, appending them to the return list.
		for page_index in range(num_pages):
			# Create the url extension and append it to the parent url
			# used to access the initial trending page for this
			# category. Send the request with the new url.
			page_url = url + "p" + str(page_index + 1) + "/"
			response = requests.get(page_url)

			# Check the status code of the response. Exit early if the
			# status code is not 200 ("Success").
			if response.status_code != 200:
				continue

			# Load in the response content to BeautifulSoup and parse it.
			new_page_soup = bsoup(response.content, features="lxml")

			# Isolate the tags with the books. Extract only the titles
			# that are in English.
			row_tags = new_page_soup.find_all("div", {"class": "row"})
			for row_tag in row_tags:
				text_title = row_tag.find("h2").text.replace("\n", "")
				language_tag = row_tag.find("span", {"class": "fi-lang"})
				if language_tag != None:
					continue

				# Append all valid titles to the trending list.
				trending_titles.append(text_title)

		# Set the list of book/text titles as the value for the
		# category number in the dictionary.
		category_value_to_texts[category_value] = trending_titles

	# Return the dictionary.
	return category_value_to_texts


# Download the PDF given.
# @param: category, the (int) value of the category the text is
#	categorized under.
# @param: title, the (str) title of the text.
# @param: link, the (str) url extension to the download page for the
#	text.
# @param: session, the (str) session id that identifies the text within
#	the PDFDrive website.
# @return: returns whether the books is successfully downloaded and
#	saved or not (bool).
def download_text(category, title, link, session):
	# Check to see if the proper folder for the text exists. If it
	# doesn't, create it.
	folder_path = "./" + str(category)
	if not os.path.exists(folder_path):
		os.mkdir(str(category))

	# Extract the text id from the download url extension. This will be
	# used to construct the url link to actually download the text in
	# pdf form.
	text_id = link.split("-")[-1][1:].strip(".html")

	# Construct the download url and send a request to download the
	# text.
	download_url = "https://www.pdfdrive.com/download.pdf?id=" + text_id +\
					"&h=" + session + "&u=cache&ext=pdf"
	#print(download_url)
	response = requests.get(download_url, verify=False)
	#response = requests.get(download_url, stream=True)

	# Check the status code of the response. Exit early if the status
	# code is not 200 ("Success").
	if response.status_code != 200:
		return False

	# Save the response.
	#print(response.encoding)
	#print(response.headers)
	#saved_response = bytes(response.text, "utf-8")
	saved_response = response.content
	#print(sys.getsizeof(saved_response))
	#print(saved_response[-100:])
	# print(saved_response)

	# Save the pdf to the category's folder.
	title = title.replace("\"", "\'").replace("\\", "").replace("?", "")
	title = title.replace("/", "-")
	#print(folder_path + "/" + title + ".pdf")
	#print()
	file = open(folder_path + "/" + title + ".pdf", "wb")
	file.write(saved_response) 
	file.close()
	'''
	with open(folder_path + "/" + title + ".pdf", "wb") as file:
		for chunk in response.iter_content(1024):
			file.write(chunk)
	'''

	# Return True.
	return True


# Download the top trending books from a category.
# @param: category, a valid category (int) from the dictionary mapping
#	a category's number value to its name.
# @return: returns whether the books from the scrape were successfully
#	saved or not (bool).
def download_trending_from_category(category):
	# Load in the mapping from all category values to their respective
	# topics. This should take about a minute. This will be used to
	# optimize the search.
	category_value_to_label = get_categories()

	# Before even sending the request to PDFDrive, check the
	# dictionary mapping the category values to names. If the
	# category name is an empty string, scraping the site for that
	# category will provide nothing, so skip this category value.
	if category_value_to_label[category] == "":
		return False

	# Send a request using the constructed PDFDrive url.
	url = "https://www.pdfdrive.com/category/" + str(category) + "/"
	response = requests.get(url)

	# Check the status code of the response. Exit early if the status
	# code is not 200 ("Success").
	if response.status_code != 200:
		return False

	# Load in the response content to BeautifulSoup and parse it.
	page_soup = bsoup(response.content, features="lxml")

	# First, count the number of pages in the results page. Look at
	# the pagination tag for this information.
	pagination_tag = page_soup.find("div", {"class": "pagination"})
	if pagination_tag == None:
		return False
	
	# Check the number of li tags within the pagination tag. If
	# there are no li tags in the initial list, then there is only
	# one page to scrape from. Otherwise, look at the last li tag
	# after removing the ones containing the "Previous" and "Next"
	# values as text. That value will be used to count the number
	# of pages to scrape.
	page_links = pagination_tag.find_all("li")
	num_pages = 0
	if len(page_links) == 0:
		num_pages = 1
	else:
		page_links = page_links[1:-1]
		num_pages = int(page_links[-1].text)

	# Iterate through the range of possible pages. Use the values
	# to create the url extensions for every page. Extract the
	# extensions to create new urls and scrape the tiles from each
	# page, appending them to the return list.
	for page_index in range(num_pages):
		# Create the url extension and append it to the parent url
		# used to access the initial trending page for this
		# category. Send the request with the new url.
		page_url = url + "p" + str(page_index + 1) + "/"
		response = requests.get(page_url)

		# Check the status code of the response. Exit early if the
		# status code is not 200 ("Success").
		if response.status_code != 200:
			continue

		# Load in the response content to BeautifulSoup and parse it.
		new_page_soup = bsoup(response.content, features="lxml")

		# Isolate the tags with the books. Extract only the titles
		# that are in English.
		row_tags = new_page_soup.find_all("div", {"class": "row"})
		for row_tag in row_tags:
			text_title = row_tag.find("h2").text.replace("\n", "")
			language_tag = row_tag.find("span", {"class": "fi-lang"})
			if language_tag != None:
				continue

			#print(text_title)

			# Find the book's download link extension.
			download_link = row_tag.find("a")["href"]
			split_link = download_link.split("-")
			split_link[-1] = split_link[-1].replace("e", "d")
			new_download_link = "-".join(split_link)

			# Send a request to the initial download link to extract
			# the session id required to download the text.
			page_url = "https://www.pdfdrive.com" + download_link
			response = requests.get(page_url)

			# Check the status code of the response. Exit early if the
			# status code is not 200 ("Success").
			if response.status_code != 200:
				continue

			# Load in the response content to BeautifulSoup and parse it.
			ebook_page_soup = bsoup(response.content, features="lxml")

			# Extract the ebook button from the page.
			ebook_button = ebook_page_soup.find("button", {"id": "previewButtonMain"})
			if ebook_button == None:
				continue

			# Extract the session id.
			ebook_preview = ebook_button["data-preview"]
			DATA_PREVIEW_TEXT = "/ebook/preview?"
			session_id = ebook_preview[len(DATA_PREVIEW_TEXT):].split("session=")[-1]

			# Download the text as pdf.
			download_status = download_text(category, text_title,
											download_link, session_id)

			# If the download was not successful, break from the loop
			# and return False.
			#if not download_status:
			#	return download_status
			#if row_tags.index(row_tag) == 2:
			#	break

			# Give a pause between requests.
			time.sleep(15)
		time.sleep(60)

	# Return True
	return True


# Download the books from a search.
# @param: search, a (str) query that is a topic or category name.
# @return: returns whether the books from the scrape were successfully
#	saved or not (bool).
def download_search_results(search):
	pass


def compress_file(file_name):
	if not os.path.exists(file_name):
		return False

	# Read from the file.
	old_file = open(file_name, "rb")
	data = old_file.read()
	old_file.close()

	# Change the filename so that it has the new file extension for
	# pdf file.
	new_file_name = file_name.strip(".xz") + ".df"

	# Write to the new file.
	new_file = lzma.open(new_file_name, "wb")
	new_file.write(data)
	new_file.close()
	
	return True


def decompress_file(file_name):
	if not os.path.exists(file_name):
		return False

	# Read from the file.
	old_file = open(file_name, "rb")
	data = old_file.read()
	old_file.close()

	# Change the filename so that it has the new file extension for
	# compressed file.
	new_file_name = file_name.strip(".pdf") + ".xz"

	# Write to the new file.
	new_file = lzma.open(new_file_name, "wb")
	new_file.write(data)
	new_file.close()
	
	return True


if __name__ == '__main__':
	#main()

	'''
	# Get a mapping from all category values to their respective
	# topics. This should take about a minute.
	start = datetime.now()
	cate_map = get_categories()
	end = datetime.now()
	print("Category scan finished in {}".format(end - start))
	print("Category value to name dictionary:")
	print(json.dumps(cate_map, indent=4))
	#print("Number of values in dictionary " + str(len(list(cate_map.keys()))))
	'''

	'''
	# Retrieve all the books found in the top trending of a category.
	# This should take about 5 minutes.
	start = datetime.now()
	trend_map = get_trending_by_category()
	end = datetime.now()
	print("Trending-by-Category scan finished in {}".format(end - start))
	print("Category value to book name dictionary:")
	print(json.dumps(trend_map, indent=4))
	'''

	'''
	# Download all the top trending books from a category.
	start = datetime.now()
	download_status = download_trending_from_category(86)
	end = datetime.now()
	print("Download all trending from category 86 finished in {}".format(end - start))
	print("Download status " + str(download_status))
	'''

	category_map = get_categories()
	for key in category_map.keys():
		download_trending_from_category(key)
		time.sleep(900)