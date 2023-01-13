# Vigenere Cipher

def keyGenerationFunc(text, key):
	key = list(key)
	if len(text) == len(key):
		return key
	else:
		for i in range(len(text) - len(key)):
			key.append(key[i % len(key)])
	return "".join(key)
	
def vignere_encrypt(text, key):
	cipherText = []
	for i in range(len(text)):
		temp = ((ord(text[i]) + ord(key[i])) % 26) + 65
		cipherText.append(chr(temp))

	return "".join(cipherText)
	
def vignere_decrypt(cipherText, key):
	originalText = []
	for i in range(len(cipherText)):
		x = ((ord(cipherText[i]) - ord(key[i]) + 26) % 26) + 65
		originalText.append(chr(x))
	return("" . join(originalText))
	
print("Vignere Cipher")
text = input("Enter text: ").upper()
keyword = input("Enter Key: ")
key = keyGenerationFunc(text, keyword)
cipherText = vignere_encrypt(text,key)
print("Cipher text :", cipherText)
print("Decrypted Text :",vignere_decrypt(cipherText, key))
