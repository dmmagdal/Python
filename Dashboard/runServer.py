# runServer.py
# author: Diego Magdaleno
# This program starts up both the web scraper and the web app fo the
# dashboard. While the scraper runs constantly, querying and updating
# the written info, the app runs as well, reading from the files the
# scraper writes to. This is just one strategy I'm using to have a
# 'live' dashboard without needing another language or service.
# Python 3.6
# Linux


import sys
import os
import subprocess
from subprocess import Popen


def main():
	# os.subprocess("python scraper.py")
	# os.subprocess("python server.py")
	#subprocess.run("python scraper.py")
	#subprocess.run("python server.py")
	commands = ["python scraper.py", "python server.py"]
	processes = [Popen(cmd) for cmd in commands]
	for process in processes:
		process.wait()



if __name__ == '__main__':
	main()