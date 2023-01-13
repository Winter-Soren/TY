def affine_encrypt(text, key):
	# C = (a*P + b) % 26

    encrypted_text = ''

    for t in text:
        if t!= " ":
            if t.islower():
                char = ((key[0]*(ord(t) - ord('a')) + key[1]) % 26) + ord('a')
                encrypted_text+= chr(char)
            elif t.isupper():
                char = ((key[0]*(ord(t) - ord('A')) + key[1]) % 26) + ord('A')
                encrypted_text+= chr(char)
        elif t==" ":
            encrypted_text+=" "
    
    return encrypted_text


# affine cipher decryption function
def affine_decrypt(cipher, key):
	# P = (a^-1 * (C - b)) % 26


    decrypted_text = ''

    key_inv = 0

    for i in range(26):
        flag = (key[0]* i) % 26

        if (flag == 1):
            key_inv = i
    

    for t in cipher:
        if t!= " ":
            if t.islower():
                char = (key_inv*(ord(t) - ord('a') - key[1]) % 26) + ord('a')
                decrypted_text+= chr(char)
            elif t.isupper():
                char = (key_inv*(ord(t) - ord('A') - key[1]) % 26) + ord('A')
                decrypted_text+= chr(char)
        elif t==" ":
            decrypted_text+=" "

    return decrypted_text


def main():

    print("Affine Cipher")
    text = input("Enter the text: ")
    k1 = int(input("Enter first key: "))
    k2 = int(input("Enter second key: "))
    key = [k1, k2]

    affine_encrypted_text = affine_encrypt(text, key)

    print('Encrypted Text: '+ affine_encrypted_text)
    print('Decrypted Text: '+ affine_decrypt(affine_encrypted_text, key))

main()
