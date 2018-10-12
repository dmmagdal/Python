# emailItrfc.py
# This module uses webscraping with selenium to read incoming emails
# and send new messages.
# python 3.6.5
# windows 10

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import smtplib
