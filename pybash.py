# Simple program to show how to run system calls (on windows bash)
# via os.system. This program executes a command to save the 
# DNS cache in a txt file

import os

os.system("ipconfig /displaydns>output.txt") 