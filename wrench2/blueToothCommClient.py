# blueToothCommClient.py
# Acts as a reciever for bluetooth device.
# Python 3.6
# Windows 10

import bluetooth

def main():
	bd_addr = "01:23:45:67:89:AB"

	port = 1

	sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	sock.connect((bd_addr, port))

	sock.send("hello!!")

	sock.close()


if __name__ == '__main__':
	main()
