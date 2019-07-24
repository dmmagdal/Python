# encryptDecrypt.py
# author: Diego Magdaleno
# This simple program explores the cryptography library as it generates
# keys, saves them, and uses them to encrypt and decrypt strings.
# Source: https://nitratine.net/blog/post/encryption-and-decryption-in-python/
# Python 3.6
# Linux


import cryptography
from cryptography.fernet import Fernet


def main():
	string = "He sells sea shells by the seashells by the seashore."
	print("String to encrypt: "+string)

	key = Fernet.generate_key()
	print("Key: "+str(key))

	keyFile = open("key.key", 'wb+')
	keyFile.write(key)
	keyFile.close()
	print("Key saved to file")

	message = string.encode()
	function = Fernet(key)
	encrypted = function.encrypt(message)
	print("String encrypted: "+str(encrypted))

	keyFile = open("key.key", 'rb')
	newKey = keyFile.read()
	keyFile.close()
	print("Key read from file: "+str(newKey))
	print("Read key matches generated key: "+str(newKey==key))

	decrypted = function.decrypt(encrypted)
	print("String decrypted: "+str(decrypted.decode()))


if __name__ == '__main__':
	main()
