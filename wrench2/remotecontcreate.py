# remotecontcreate.py
# author: Diego Magdaleno
# A program to remote control the Create2 bot from a laptop (Master).
# Some snippets from Hacker House Turret project.
# Python 3.6
# Linux

from pycreate2 import Create2
import sys
import socket

# TODO: Format later into a comprehensive GUI.
def main():
	# Robot will use tank controls (ie turning turns the robot in
	# place).
	print("To move robot, use w,a,s,d. To quit, press q.")
	with raw_mode(sys.stdin):
		try:
			# Infinite loop to constantly read from command line.
			while True:
				# Load input as variable chara.
				chara = sys.stdin.read(1)

				# If the chara is not valid or 'q', break the loop
				# (end program).
				if not chara or chara == "q":
					break

				# Otherwise, handle all other control cases.
				if chara == "w":
					pass
				elif chara == "a":
					pass
				elif chara == "s":
					pass
				elif chara == "d":
					pass
				elif chara == "c":
					# Special character to return robot to charging
					# dock.
					pass
		except (KeyboardInterrupt, EOFError):
			pass

if __name__ == '__main__':
	main()
