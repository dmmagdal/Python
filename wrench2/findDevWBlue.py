# findDevWBlue.py
# Finds nearby bluetooth devices.
# Python 3.6
# Windows 10

import bluetooth

def main():
	target_name = "My Iphone"
	target_address = None

	nearby_devices = bluetooth.discover_devices()

	for bdadder in nearby_devices:
		if target_name == bluetooth.lookup_name(bdadder):
			target_address = bdadder
			break

	if target_address is not None:
		print("Found the target device with address ", target_address)
	else:
		print("Could not find target device.")


if __name__ == '__main__':
	main()
