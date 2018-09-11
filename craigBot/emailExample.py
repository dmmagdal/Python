# emailExample.py
# author: Diego Magdaleno
# This is practice for sending emails through python.

import smtplib

# create smtp object to connect to server.
server = smtplib.SMTP('smtp.gmail.com', 587)

#me = "maxm9450@gmail.com"
#ps = "Maxsam12"

me = "craigcarb1224@gmail.com"
ps = "1Dullahan"

#NOTE: Need to be logged in to account with webbrowser to work.

'''
# connect to server.
server.connect('smtp.gmail.com', 465)
'''
server.ehlo()
server.starttls()
server.ehlo()

# log into server.
server.login(me, ps)

# send email
msg = "This is a test for another program."
server.sendmail(me, "dmagdale@cisco.com", msg)
# first argument is source, second is target recipient.

# exit server.
server.quit()